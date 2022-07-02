# A program to automatically control my home router ( whitelist or blacklist few ruled IP Addresses )
import pandas as pd
from selenium import webdriver
from controller import loginRouter, logoutRouter, updateRouting


# Driver Code
if __name__ == "__main__":
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    # webdriver ( better start from your C:\ or D:\ or etc system if want to use a task scheduler
    driver = webdriver.Chrome('driver/chromedriver_win32/chromedriver.exe', options=op)  # Using Chrome to access web, option need to be removed if want to see the browser
    df = pd.read_csv('input file/routing data.csv')

    # get current router status
    currentStatus = df['currentStatus'][0]
    if currentStatus != "forced_on_or_off":
        statusForRuledMac = df['statusForRuledMac'][0]
        loginRouter(driver)
        if statusForRuledMac == "off":
            updateRouting(driver, df, "on")
        else:
            updateRouting(driver, df, "off")
        logoutRouter(driver)
        driver.close()

# check time and current time range and current status, so that laptop or PC does not need to always on
# configure python3.10.exe