import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
## General SET UP
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

## function
def climate_data(link, name):
    driver.get(link)
    search_res = driver.find_elements(By.CSS_SELECTOR, '#climateTable .climate-month') 
    results = []
    for res in search_res:
        month = res.get_attribute('class').split("--")[1]

        if month == 'allyear':
            continue

        all_inf = res.find_elements(By.CSS_SELECTOR, 'div.four.columns')
  
        temperature_e = all_inf[0].find_elements(By.CSS_SELECTOR, 'p')
        temperature = []
        for a in temperature_e:
            temperature.append(a.get_attribute("textContent"))

        phd_e = all_inf[1].find_elements(By.CSS_SELECTOR, 'p')
        phd = []
        for a in phd_e:
            phd.append(a.get_attribute("textContent"))

        wpv_e = all_inf[2].find_elements(By.CSS_SELECTOR, 'p')
        wpv = []
        for a in wpv_e:
            wpv.append(a.get_attribute("textContent"))
    
        df_res = {
            'month': month,
            'high_temp_f':int(temperature[0].split(':')[1].replace('°F','').strip()),
            'low_tem_f':int(temperature[1].split(':')[1].replace('°F','').strip()),
            'avg_temp_f':int(temperature[2].split(':')[1].replace('°F','').strip()),
            'precipitation_inch':float(phd[0].split(':')[1].replace('"','').strip()),
            'humidity':int(phd[1].split(':')[1].replace('%','').strip()),
            'dew_point_f':int(phd[2].split(':')[1].replace('°F','').strip()),
            'wind_mph':int(wpv[0].split(':')[1].replace('mph','').strip()),
            'pressure_hg':float(wpv[1].split(':')[1].replace('"Hg','').strip()),
            'visibility_mi':int(wpv[2].split(':')[1].replace('mi','').strip())
        }
        results.append(df_res)

    df = pd.DataFrame(results) 
    df.to_csv(f'{name}.csv', index= False)

#Import everything to csv
climate_data('https://www.timeanddate.com/weather/usa/new-york/climate','new_york')
climate_data('https://www.timeanddate.com/weather/usa/miami/climate','miami')
climate_data('https://www.timeanddate.com/weather/usa/houston/climate','houston')
climate_data('https://www.timeanddate.com/weather/usa/los-angeles/climate','los_angeles')
climate_data('https://www.timeanddate.com/weather/usa/seattle/climate','seattle')
driver.quit()