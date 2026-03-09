import sqlite3
import os
import csv
import pandas as pd

#Importing everything into 1 csv file
with  sqlite3.connect("weather.db") as conn:
    cursor = conn.cursor()

    for file in os.listdir("."):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            df = pd.read_csv(file)
            df.to_sql(name, conn, index=False,if_exists="replace")
