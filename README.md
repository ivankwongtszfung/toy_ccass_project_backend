
# CCASS Plotter
 
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
### For Window
```bat
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate.bat 
pip install -r requirement.txt
uvicorn app.app_file:app --reload --reload-dir app --port 5000
// serves at http://127.0.0.1:5000/docs
```
### For Linux & MacOS
```bat
pip install virtualenv
virtualenv venv
. venv/bin/activate.bat 
pip install -r requirement.txt
uvicorn app.app_file:app --reload --reload-dir app --port 5000
// serves at http://127.0.0.1:5000/docs
```
### it also support Docker, reference the documentation for more information
