import logging

logging.basicConfig(
    filename="app.log", format="%(name)s - %(levelname)s - %(message)s", level=logging.INFO 
)
logger = logging.getLogger()