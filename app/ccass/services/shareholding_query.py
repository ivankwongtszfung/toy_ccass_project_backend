from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional
import concurrent
import time

from bs4 import BeautifulSoup
from requests_html import HTMLSession, HTMLResponse
import pandas as pd
import numpy as np

from app.logging import logger


class PayloadBuilder:
    def __init__(self, stock_code: str, date_str: Optional[str] = None):
        self.stock_code = stock_code
        self.date_str = date_str or datetime.today().strftime("%Y/%m/%d")

    def execute(self):
        return {
            "__EVENTTARGET": "btnSearch",
            "__EVENTARGUMENT": "",
            **self._get_param(),
            **self._get_sorting(),
        }

    def _get_param(self):
        return {
            "txtShareholdingDate": self.date_str,
            "txtStockCode": self.stock_code.zfill(5),
        }

    def _get_sorting(self):
        return {
            "sortBy": "shareholding",
            "sortDirection": "desc",
        }


CCACC_URL = "https://www.hkexnews.hk/sdw/search/searchsdw.aspx"


class CCASSHttpRequest:
    @lru_cache(maxsize=None)
    def post(self, stock_code: str, date_str: str):
        url = CCACC_URL
        data = PayloadBuilder(stock_code, date_str).execute()
        with HTMLSession() as session:
            res = session.post(url, data)
            return res, date_str


def p2f(x):
    return float(x.strip("%")) / 100


class CCASSResponseParser:
    @staticmethod
    def parse(response: HTMLResponse) -> pd.DataFrame:
        soup = BeautifulSoup(response.content, "html.parser")
        table_headers = soup.findAll("th")
        headers = [th.attrs.get("data-column-class")[4:] for th in table_headers]
        data = [i.text for i in soup.findAll("div", {"class": "mobile-list-body"})]
        data_matrix = np.reshape(data, (-1, 5))
        df = pd.DataFrame(data_matrix, columns=headers)
        df["shareholding-percent"] = pd.to_numeric(
            df["shareholding-percent"].str.strip("%")
        )
        return df


class CCASSHttpService:
    def __init__(self, stock_code, start_date, end_date):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.date_span = (self.end_date - self.start_date).days + 1

    def execute(self):
        result = {}
        httpRequest = CCASSHttpRequest()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for span in range(self.date_span):
                date = self._get_date(span)
                futures.append(
                    executor.submit(
                        httpRequest.post, self.stock_code, date.strftime("%Y/%m/%d")
                    )
                )

            for future in concurrent.futures.as_completed(futures):
                try:
                    response, date_str = future.result()
                    self._check_response_sucess(response, date_str)
                    result[date_str] = response
                except Exception as e:
                    logger.error(str(e))
                    raise Exception(response.text)
        return result

    def _check_response_sucess(self, response, date_str):
        if not response.ok:
            raise Exception(response.text)
        logger.info(f"{date_str} {response.status_code}")

    def _get_date(self, span):
        return self.start_date + timedelta(span)


class ShareHoldingService:
    def __init__(self, stock_code, start_date, end_date):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date

    def execute(self):
        response_dict = CCASSHttpService(
            stock_code=self.stock_code,
            start_date=self.start_date,
            end_date=self.end_date,
        ).execute()
        return {key: self._parse_first_ten(df) for key, df in response_dict.items()}

    def _parse_first_ten(self, response):
        temp_result = CCASSResponseParser.parse(response)
        return temp_result.head(10).to_dict("records")


class TransactionService:
    def __init__(
        self,
        stock_code: str,
        start_date: datetime,
        end_date: datetime,
        threshold: float,
    ):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.threshold = threshold

    def execute(self):
        response = CCASSHttpService(
            stock_code=self.stock_code,
            start_date=self.start_date,
            end_date=self.end_date,
        ).execute()
        parse_response = {
            key: CCASSResponseParser.parse(df) for key, df in response.items()
        }
        return self._larger_than_threshold(parse_response)

    def _larger_than_threshold(self, response):
        result = {}
        list_of_date = list(response.keys())
        list_of_date.sort(key=lambda x: datetime.strptime(x, "%Y/%m/%d"))
        for idx, curr_date in enumerate(list_of_date):
            if idx == 0:
                continue
            # current date - yesterday
            prev_date = list_of_date[idx - 1]
            prev_holding = self._get_shareholding_percent(response[prev_date])
            curr_holding = self._get_shareholding_percent(response[curr_date])
            result[curr_date] = self._get_diff_holding(prev_holding, curr_holding)
        return result

    def _get_shareholding_percent(self, df):
        result = df.set_index("participant-id")
        return result["shareholding-percent"]

    def _get_diff_holding(self, prev_df, curr_df):
        diff_holding = Counter(curr_df.to_dict()) - Counter(prev_df.to_dict())
        return {
            id: round(amount, 2)
            for id, amount in diff_holding.items()
            if round(amount, 2) >= self.threshold
        }
