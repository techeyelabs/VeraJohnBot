import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions

# programmer defined libraries
import ClientViews.StaticVars as svBot

class BotInitiation:
    # constructor to install chromedriver
    def __init__(self):
        print("hellox")
        # make sure chrome browser is available
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    # Parse through iframes to get to the tables
    def initiateTables(self):
        parentIframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'/game/baccarat-lobby-paris/frame')]")))
        self.driver.switch_to.frame(parentIframe)
        childIframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@name,'innergame')]")))
        self.driver.switch_to.frame(childIframe)
        grandchildIframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@name,'EVO_GAME')]")))
        self.driver.switch_to.frame(grandchildIframe)

        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".TableName--1Watn")))
        return self.driver.find_elements_by_css_selector("div[class*='TableName--1Watn']")


    # Read potential tables to read their present gamecounts
    def lookForTables(self, tableStatusParam, tablesParam):
        tableStatus = tableStatusParam
        tables = tablesParam

        for idx, t in enumerate(tables):
            print("outer")
            b = self.driver.find_elements_by_css_selector("div[class*='TableName--1Watn']")
            if (len(b) == 0):
                b = self.initiateTables()
            print(len(b))
            for tls in b:
                print("inner")
                print(t)
                print(tls.text)
                if tls.text == t:
                    # get overflown tables into view as they might not be initially clicable
                    tls.location_once_scrolled_into_view
                    tls.click()
                    time.sleep(15)

                    # get the count of hands played in this table
                    counterDivs = WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'gameCount')]")))
                    tableStatus[idx] = counterDivs.text
                    self.driver.back()
                    time.sleep(20)
                    break
        return [tableStatus, tables]

    # Loop through tables to select one
    def loopTables(self, b, selectedTable):
        for tlsS in b:
            if tlsS.text == selectedTable:
                tlsS.location_once_scrolled_into_view
                tlsS.click()
                time.sleep(25)
                self.operateTable()
                break

    # Start operationg on the selected table
    def operateTable(self):
        counterDivs = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'gameCount')]")))
        print(counterDivs.text)

        whenStarted = counterDivs.text

        # wait until table restarts
        while whenStarted != '0':
            try:
                l = self.driver.find_element_by_css_selector("div[class*='clickable--3IFrf']")
                l.click()
                time.sleep(5)
                counterDivs = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'gameCount')]")))
                whenStarted = counterDivs.text
                print(whenStarted)
            # NoSuchElementException thrown if not present
            except NoSuchElementException:
                time.sleep(20)
                counterDivs = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'gameCount')]")))
                whenStarted = counterDivs.text
                print(whenStarted)
            if whenStarted == '0':
                break

    # Master method
    def start(self):
        print("automation initiated")

        # maximize browser window
        # driver.maximize_window()

        # initialize verajohn web
        okFlag = 0
        while okFlag == 0:
            try:
                l = self.driver.find_element_by_css_selector("input[class*='form-text required'][id='signin-mail']")
                print("found")
                okFlag = 1
            # NoSuchElementException thrown if not present
            except NoSuchElementException:
                print("looking")
                self.driver.get("https://verajohn.com/ja")



        time.sleep(10)
        # grab username and password field
        username = self.driver.find_element_by_css_selector("input[class*='form-text required'][id='signin-mail']")
        password = self.driver.find_element_by_css_selector("input[class*='form-text required'][id='signin-pass']")


        # Flood username and password field with values from static class
        userid = svBot.StaticVars.userId
        userpass = svBot.StaticVars.userPass
        time.sleep(5)
        username.send_keys("coginc2009@gmail.com")
        password.send_keys("!rQzzz2JHEDdP9G")
        time.sleep(5)

        # Press submit
        submitbtn = self.driver.find_element_by_css_selector(".button[class*='button form-submit'][id='edit-submit-signin']")
        submitbtn.send_keys(Keys.ENTER)

        time.sleep(3)
        # driver.get("https://www.verajohn.com/ja/myaccount/overview")
        # elem = driver.find_element_by_xpath('//span[@class="cta_button cta_primary cookie-disclaimer-close"]').click()
        time.sleep(3)
        self.driver.get("https://www.verajohn.com/ja/game/baccarat-lobby-paris")
        # driver.get("https://www.verajohn.com/ja/game/baccarat-lobby-paris/frame")
        time.sleep(13)

        b = self.initiateTables()


        print(len(b))
        # return
        tableStatus = [0, 0, 0, 0, 0]
        tables = [
            "スピードバカラ A",
            "スピードバカラ B",
            "バカラ A",
            "バカラ B",
            "バカラ C"
        ]

        tablesSearch = self.lookForTables(tableStatus, tables)
        tableStatus = tablesSearch[0]
        tables = tablesSearch[1]

        # convert string array to int array
        tableStatus = list(map(int, tableStatus))

        # display all table statuses
        print(tableStatus)

        # get to table list again
        maxVal = tableStatus.index(max(tableStatus))

        # get selected table name
        selectedTable = tables[maxVal]

        # walk through iframes to get to tables again
        b = self.initiateTables()

        # get into selected table
        self.loopTables(b, selectedTable)
        print("Successfully reached beginning of table.")

        print("Table started")
        GameCount = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'gameCount')]")))
        playerWinCount = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'playerWins')]")))
        bankerWinCount = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'bankerWins')]")))

        print("initial game count: " + GameCount.text)
        print("initial banker count: " + bankerWinCount.text)
        print("initial player count: " + playerWinCount.text)

        # Here some notations will be used. they are as follows:
        # 1: Player
        # 2: Banker
        # 10: Yes
        # 20: No

        # set tracking values of game, player and banker
        lastGame = int(GameCount.text)
        lastPlayer = int(bankerWinCount.text)
        lastBanker = int(playerWinCount.text)
        qWinner = []
        qPrediction = [0]
        while True:
            print("hello")
            state = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@data-type,'gameCount')]")))
            latest = int(state.text)
            if (last == latest):
                continue
            else:
                last = int(latest)



