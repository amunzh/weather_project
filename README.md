# Weather Project
The project explores climate factors in New York, Miami, Houston, Seattle, and Los Angeles.
## Dataset
| Dataset | Table
| :------ | :----
| New York | new_york
| Miami | miami
| Houston | houston
|Los Angeles | los_angeles
|Seattle | seattle

## Programs
### 1. Scraper - scraping_climat.py
Program to scrape the climate data from the website using Selenium and save the csv files. 

Output: `{city name}.csv`

### 2. Database - sql_database.py
Taking all csv files and adding it to the weather database.

Output `weather.db`

### 3. Query query.py
Interactive menu for querying `weather.db`

Menu: 

    1. Get the average temperature for each month in NY, LA, Houston, Miami, or Seattle
    2. Comparing hottes or coldest month for every 5 cities with temperature
    3. Compare wind speed in each month for 2 cities of your choice(JOIN)
    4. Get average Relative Humidity for all 5 cities(JOIN)
    5. Look at all cities' annual precipitation(JOIN)
    0. Exit
  
### 4. Dashboard - myapp.py
Interactive dashboards made with Dash.

Graphs:
1. Heatmap for each Month by City
2. Precipitation for each city
3. Monthly Climate by City

## Project Structure

```
weather_project/
├── scraping_climat.py   # Selenium scraper → CSV files
├── sql_database.py      # CSV files → SQLite database
├── query.py             # CLI menu query tool
├── myapp.py             # Dash dashboard
├── weather.db           # SQLite database
├── new_york.csv         # Datasets:
├── los_angeles.csv
├── miami.csv
├── seattle.csv
├── houston.csv
├── requirements.txt
├── .gitignore
└── README.md
```
