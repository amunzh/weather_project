import sqlite3

#Connecting to the database
try: 
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
except sqlite3.DatabaseError as e:
    print("Error:", e)

menu = '''
        ----- Weather Query Tool -----
    1. Get the average temperature for each month in NY,LA, Houston, Miami, or Seattle
    2. Comparing hottes or coldest month for each 5 cities with temperature
    3. Compare wind speed in each month for 2 cities of your choice(JOIN)
    4. Get average Relative Humidity for all 5 cities(JOIN)
    5. Look at all cities' annual precipitation(JOIN)
    0. Exit
'''

#Order for all cities
city_index = {
    1: 'new_york',
    2: 'los_angeles',
    3: 'houston',
    4: 'miami',
    5: 'seattle'
}

#1st query
def q1_cityinf(city1):
    print('Which city you would like to look at?')

    for num, city in city_index.items():
        print(num, "-", city)

    while True: 
        try: 
            city_choice = int(input("Enter the number of the city (1-5): ")) 
            if city_choice in city_index:
                break 
            else:
                print('Enter a number between 1-5')
        except (ValueError, KeyError): 
            print("Please enter a number between 1-5.")
    city = city_index[city_choice]
    query = f'''
    SELECT month, avg_temp_f FROM {city}; 
    '''
    cursor.execute(query)
    print(cursor.fetchall())

#2nd query
def q2_hc(city1):

    while True:
        try: 
            temp_choice = int(input("Please enter a number below(1-hottest, 2-coldest):")) 
            if temp_choice in {1,2}:
                break 
            else:
                print('Choose 1-hottest or 2-coldest:')
        except (ValueError, KeyError): 
            print("Choose 1-hottest or 2-coldest:")

    
    if temp_choice == 1:
        query = '''SELECT * FROM (
        SELECT 'New York' as city, month, high_temp_f FROM new_york ORDER BY high_temp_f DESC LIMIT 1)
        UNION  SELECT * FROM (SELECT 'Los Angeles' as city, month, high_temp_f FROM los_angeles ORDER BY high_temp_f DESC LIMIT 1)
        UNION SELECT * FROM (SELECT 'Houston' as city, month, high_temp_f FROM houston ORDER BY high_temp_f DESC LIMIT 1)
        UNION SELECT * FROM (SELECT 'Miami' as city, month, high_temp_f FROM miami ORDER BY high_temp_f DESC LIMIT 1)
        UNION SELECT * FROM (SELECT 'Seattle' as city, month, high_temp_f FROM seattle ORDER BY high_temp_f DESC LIMIT 1)
        ORDER BY high_temp_f DESC;'''
        cursor.execute(query)
        print(cursor.fetchall())
    elif temp_choice == 2:
        query = '''SELECT * FROM (
        SELECT 'New York' as city, month, low_tem_f FROM new_york ORDER BY low_tem_f ASC LIMIT 1)
        UNION  SELECT * FROM (SELECT 'Los Angeles' as city, month, low_tem_f FROM los_angeles ORDER BY low_tem_f ASC LIMIT 1)
        UNION SELECT * FROM (SELECT 'Houston' as city, month, low_tem_f FROM houston ORDER BY low_tem_f ASC LIMIT 1)
        UNION SELECT * FROM (SELECT 'Miami' as city, month, low_tem_f FROM miami ORDER BY low_tem_f ASC LIMIT 1)
        UNION SELECT * FROM (SELECT 'Seattle' as city, month, low_tem_f FROM seattle ORDER BY low_tem_f ASC LIMIT 1)
        ORDER BY low_tem_f ASC;'''
        cursor.execute(query)
        print(cursor.fetchall())
    else:
        print("  Invalid option — you should have entered 1 or 2.\n")

#3rd query
def q3_wind(c1):
    print('Which city you would like to look at?')
    for num, city in city_index.items():
        print(num, "-", city)
    while True:
        try:
            city_choice1 = int(input("Please enter a FIRST city:"))
            city_choice2 = int(input("Please enter a SECOND city:"))
            if city_choice1 in city_index and city_choice2 in city_index:
                break
            else:
                print("Invalid number for city. Please enter a number between 1-5")
        except (ValueError, KeyError): 
            print("Please enter a number between 1-5.")
    city1 = city_index.get(city_choice1)
    city2 = city_index.get(city_choice2)

    query = f'''SELECT {city1}.month, '{city1}' AS city1, {city1}.wind_mph AS {city1}_wind, '{city2}' AS city2,
                    {city2}.wind_mph AS {city2}_wind,'Difference:', 
                    ({city1}.wind_mph - {city2}.wind_mph) AS wind_difference
                FROM {city1} JOIN {city2} ON {city1}.month = {city2}.month'''
    cursor.execute(query)
    print(cursor.fetchall())

#4th query
def q4_humidity(c1):
    query = ''' SELECT 'new_york', AVG(n.humidity) as new_york_hum,
    'los_angeles',AVG(l.humidity) as los_angeles_hum, AVG(h.humidity) as houston_hum,
    AVG(m.humidity) as miami_hum, AVG(s.humidity) as seattle_hum 
    FROM new_york as n
    JOIN los_angeles AS l ON n.month = l.month
    JOIN houston AS h ON n.month = h.month
    JOIN miami AS m ON n.month = m.month
    JOIN seattle AS s ON n.month = s.month
    '''
    cursor.execute(query)
    print(cursor.fetchall())

#5th query
def q5_precipitation(c1):
    query = '''SELECT 'new_yourk', SUM(n.precipitation_inch) as new_york_p,'los_angeles',
    SUM(l.precipitation_inch) as los_angeles_p, 'houston',SUM(h.precipitation_inch) as houston_p,
    'miami', SUM(m.precipitation_inch) as miami_p, 'seattle',SUM(s.precipitation_inch) as seattle_p
    FROM new_york as n
    JOIN los_angeles AS l ON n.month = l.month
    JOIN houston AS h ON n.month = h.month
    JOIN miami AS m ON n.month = m.month
    JOIN seattle AS s ON n.month = s.month'''
    cursor.execute(query)
    print(cursor.fetchall())





main_choices = {
    '1':q1_cityinf,
    '2': q2_hc,
    '3':q3_wind,
    '4':q4_humidity,
    '5':q5_precipitation
}

def main():
    
    print('\n ----- Weather Query Tool -----')

    while True:
        print(menu)
        choice = input("Select option (0–5): ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        elif choice in main_choices:
            try:
                main_choices[choice](conn)
            except KeyboardInterrupt:
                print("\n  (query cancelled)")
        else:
            print("  Invalid option — please enter 0–5.\n")

    conn.close()

if __name__ == "__main__":
    main()