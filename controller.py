from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import pandas as pd


def loginRouter(driver):
    driver.get('http://192.168.0.1/index.html#entry')  # your router IP address
    driver.maximize_window()  # For maximizing window
    driver.implicitly_wait(20)  # gives an implicit wait for 20 seconds
    pass_box = driver.find_element(By.ID, "password container ID")
    pass_box.send_keys('router password here')
    driver.implicitly_wait(20)
    login_button = driver.find_element(By.ID, "btnLogin")  # Find login button
    login_button.click()  # Click login
    try:
        driver.implicitly_wait(2000)
        textbox = driver.find_element(By.ID, "okbtn")
        textbox.click()
    finally:
        driver.implicitly_wait(200)
        setting_btn = driver.find_element(By.ID, "menuQuickSet")
        setting_btn.click()


def logoutRouter(driver):
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"logoutlink\"]"))))
    driver.implicitly_wait(20)
    yesBtn = driver.find_element(By.ID, "yesbtn")
    yesBtn.click()


def updateMaxStationNumber(driver, maxStation):
    driver.implicitly_wait(2000)
    # to SSID section
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"accordion\"]/li[3]/ul/li[1]/a"))))
    driver.implicitly_wait(2000)
    # to max station input
    select = Select(driver.find_element(By.XPATH, '//*[@id="maxStation"]'))
    select.select_by_visible_text(str(maxStation))
    driver.implicitly_wait(2000)
    # apply button
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ssid1_apply\"]"))))
    driver.implicitly_wait(2000)
    # yes button
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"yesbtn\"]"))))
    driver.implicitly_wait(2000)


def updateStatusForRuledMac(routingData, Stat):
    routingData['statusForRuledMac'][0] = Stat
    routingData.to_csv("input file/routing data.csv", index=False)  # routing data file


def updateRouterWhitelist(driver, routingData, to_X_Stat):
    driver.implicitly_wait(20)
    wlan_setting_btn = driver.find_element(By.XPATH, "// *[ @ id = \"accordion\"] / li[3] / div")
    wlan_setting_btn.click()
    driver.implicitly_wait(20)
    wlan_mac_filter_btn = driver.find_element(By.XPATH, "//*[@id=\"accordion\"]/li[3]/ul/li[6]/a")
    wlan_mac_filter_btn.click()
    # mac_X where 1 <= X <= 10
    Y = 0
    for X in range(len(routingData["ruleless mac address"])):
        if pd.isna(routingData["ruleless mac address"][X]) is False:
            id = "mac_" + str(X + 1)
            driver.implicitly_wait(20)
            whitelist = driver.find_element(By.ID, id)
            whitelist.clear()
            whitelist.send_keys(routingData["ruleless mac address"][X])
        Y = X
    pointer = Y + 1

    if to_X_Stat == 'on':
        for x in range(len(routingData["ruled mac address"])):
            if pointer != 10 and pd.isna(routingData["ruled mac address"][x]) is False:
                id = "mac_" + str(pointer + 1)
                driver.implicitly_wait(20)
                whitelist = driver.find_element(By.ID, id)
                whitelist.clear()
                whitelist.send_keys(routingData["ruled mac address"][x])
            else:
                break
            pointer += 1
    else:
        for x in range(pointer, 10):
            id = "mac_" + str(x + 1)
            driver.implicitly_wait(20)
            whitelist = driver.find_element(By.ID, id)
            whitelist.clear()

    apply_btn = driver.find_element(By.XPATH, "//*[@id=\"mac_filter_form\"]/div/div[2]/input")
    apply_btn.click()
    driver.implicitly_wait(50)


def updateRouting(driver, routingData, to_X_Stat):
    if to_X_Stat == "on":
        updateRouterWhitelist(driver, routingData, to_X_Stat)
        numberOfRulelessMac = [x for x in routingData["ruleless mac address"] if pd.isna(x) is False]
        numberOfRuledMac = [x for x in routingData["ruled mac address"] if pd.isna(x) is False]
        maxStation = numberOfRulelessMac + numberOfRuledMac
        updateMaxStationNumber(driver, len(maxStation))
        updateStatusForRuledMac(routingData, "on")
    else:
        updateRouterWhitelist(driver, routingData, to_X_Stat)
        maxStation = [x for x in routingData["ruleless mac address"] if pd.isna(x) is False]
        updateMaxStationNumber(driver, len(maxStation))
        updateStatusForRuledMac(routingData, "off")
        # reportDailyDataUsage()

# def reportDailyDataUsage():
#     # session 1(8am - 11am),session 2, total
#
#
# def updateRemainingdata():
#
#
# def forceOff():
#
#
# def forceOn():
#
#
# def updateDailyLimit(dailyLimit):
#
#
# def addRulelessMac(user, macAdd):
#
#
# def addRuledMac(user, macAdd):
#
#
# def removeMac(user):
#
#
# def displayDailyStatistic():
#
#
# def displayUsedData():
#
#
# def updateLastSubscriptionDate(day, month, year):
