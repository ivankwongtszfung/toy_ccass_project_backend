
# Interview Project - CCASS Plotter
## To be completed by Wednesday 3 Feburary

By getting the underlying data from the link below, build a single page web app using Python and JavaScript. If you can build it solely in Python, that's fine too.
 
https://www.hkexnews.hk/sdw/search/searchsdw.aspx
 
## Duration: 1 week from this spec is sent.
Deploy the app onto an AWS free-tier
Commit the code to a public Github repo
Pass us the app URL and the Github link
 
## Tab 1 - trend plot
### Input
- Stock code
- Start date
- End date
 
### Output
- Plot the "Shareholding" of the top 10 participant as of the end date
- Display the data in a table with filter
 
## Tab 2 - transaction finder
### Input
- Stock code
- Start date
- End date
- Threshold % of total number of shares
 
There could be transaction between two participants and we would like to detect them. The % threshold input the minimum % of the shares exchanged, e.g. if it's set to 1%, please find the participants who increases or decreases >1% of the shares in a day, and list out the participant ID/names who possibly exchange their shares on which day.


## To start the project
```bat
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate.bat
pip install -r requirement.txt
uvicorn app.app_file:app --reload --reload-dir app
// serves at http://127.0.0.1:8000/docs
```
