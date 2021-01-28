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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions

# programmer defined libraries
import ClientViews.StaticVars as svBot

class BotInitiation:
    # chips array
    chipsArray = [10000, 1000, 500, 100, 25, 5, 1]

    # constructor to install chromedriver
    def __init__(self):
        # make sure chrome browser is available
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        # Betting set
        multiple = 1
        self.setx = [1 * multiple, 2 * multiple, 3 * multiple, 5 * multiple, 7 * multiple, 10 * multiple,
               15 * multiple, 22 * multiple, 33 * multiple, 48 * multiple, 72 * multiple]

    # Parse through iframes to get to the tables
    def initiateTables(self):
        try:
            parentIframe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, svBot.StaticVars.IFRAME_1)))
            self.driver.switch_to.frame(parentIframe)
            childIframe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, svBot.StaticVars.IFRAME_2)))
            self.driver.switch_to.frame(childIframe)
            grandchildIframe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, svBot.StaticVars.IFRAME_3)))
            self.driver.switch_to.frame(grandchildIframe)

            WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".TableName--2WO05")))
            return self.driver.find_elements_by_css_selector(svBot.StaticVars.TABLES)
        except:
            return False



    # Read potential tables to read their present gamecounts
    def lookForTables(self, tableStatusParam, tablesParam):
        tableStatus = tableStatusParam
        tables = tablesParam

        for idx, t in enumerate(tables):
            try:
                b = self.driver.find_elements_by_css_selector(svBot.StaticVars.TABLES)
            except:
                return False
            if (len(b) == 0):
                b = False
                while (b == False):
                    b = self.initiateTables()
            try:
                for tls in b:
                    if tls.text == t:
                        # get overflown tables into view as they might not be initially clicable
                        tls.location_once_scrolled_into_view
                        tls.click()
                        time.sleep(15)

                        # get the count of hands played in this table
                        counterDivs = WebDriverWait(self.driver, 60).until(
                            EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                        tableStatus[idx] = counterDivs.text
                        # if int(counterDivs.text) >= 60:
                        #     return [tableStatus, tables]
                        print(tableStatus)
                        self.driver.back()
                        time.sleep(20)
                        break
            except:
                return False
        return [tableStatus, tables]

    # Loop through tables to select one
    def loopTables(self, b, selectedTable):
        try:
            for tlsS in b:
                if tlsS.text == selectedTable:
                    tlsS.location_once_scrolled_into_view
                    tlsS.click()
                    time.sleep(25)
                    self.operateTable()
                    break
            return True
        except:
            return False

    # Start operationg on the selected table
    def operateTable(self):
        # stop waiting for beginnign of table (remove later)
        counterDivs = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
        print(counterDivs.text)

        whenStarted = counterDivs.text

        # wait until table restarts
        while whenStarted != '0':
            try:
                l = self.driver.find_element_by_css_selector("div[class*='clickable--3IFrf']")
                l.click()
                time.sleep(5)
                counterDivs = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                whenStarted = counterDivs.text
                print(whenStarted)
            # NoSuchElementException thrown if not present
            except NoSuchElementException:
                time.sleep(20)
                counterDivs = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                whenStarted = counterDivs.text
                print(whenStarted)
            if whenStarted == '0':
                break

    def bettingMethod(self):
        # max try counter
        counter = 0
        b = self.initiateTables()
        while b is False:
            if counter >= svBot.StaticVars.maxTry:
                return False
            b = self.initiateTables()
            counter += 1


        # initiated tables display
        print(len(b))

        tableStatus = [0, 0, 0, 0, 0]
        tables = [
            "スピードバカラ A",
            "スピードバカラ B",
            "バカラ A",
            "バカラ B",
            "バカラ C"
        ]

        # max try counter
        counter = 0
        tablesSearch = False
        while tablesSearch is False:
            if counter >= svBot.StaticVars.maxTry:
                return False
            tablesSearch = self.lookForTables(tableStatus, tables)
            counter += 1

        tableStatus = tablesSearch[0]
        tables = tablesSearch[1]

        # convert string array to int array
        tableStatus = list(map(int, tableStatus))

        # display all table statuses
        print("tables")
        print(tableStatus)

        # get to table list again
        maxVal = tableStatus.index(max(tableStatus))

        # get selected table name
        selectedTable = tables[maxVal]

        # walk through iframes to get to tables again
        # max try counter
        counter = 0
        b = False
        while (b is False):
            if counter >= svBot.StaticVars.maxTry:
                return False
            b = self.initiateTables()
            counter += 1

        # get into selected table
        counter = 0  # max try counter
        targetTable = False
        while targetTable is False:
            if counter >= svBot.StaticVars.maxTry:
                return False
            targetTable = self.loopTables(b, selectedTable)
            counter += 1

        print("Successfully reached beginning of table.")

        print("Table started")
        # get game, player, banker count
        counter = 0  # max try counter
        threeCounts = False
        while threeCounts is False:
            if counter >= svBot.StaticVars.maxTry:
                return False
            threeCounts = True
            try:
                GameCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                playerWinCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.PLAYERWINS)))
                bankerWinCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.BANKERWINS)))
            except:
                threeCounts = False
                counter += 1

        print("initial game count: " + GameCount.text)
        print("initial banker count: " + bankerWinCount.text)
        print("initial player count: " + playerWinCount.text)

        # Here some notations will be used. they are as follows:
        # P: Player
        # B: Banker
        # Y: Yes
        # N: No
        # 3: Result doesn't exist
        # 4: Draw

        # set tracking values of game, player and banker
        lastGame = int(GameCount.text)
        lastPlayer = int(bankerWinCount.text)
        lastBanker = int(playerWinCount.text)

        # queue to keep track of winners
        qWinner = []

        # queue to keep track of prediction results
        qPrediction = ['NONE']
        prediction = 100

        iteration = 0

        # Yes/No track
        Y = 0
        N = 0

        # waiting games track
        waitingForGame = 0

        # bet start flag
        betFlag = False

        # consecutive win track
        consWins = 0

        # infinite loop to monitor the table
        while True:
            time.sleep(1)
            # ignored exception array
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

            # get total game situation
            counter = 0  # max try counter
            k = False
            while k is False:
                if counter >= svBot.StaticVars.maxTry:
                    return False
                k = True
                try:
                    stateGame = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                    latestGame = int(stateGame.text)
                except StaleElementReferenceException:
                    k = False
                    counter += 1

            # get player situation
            counter = 0  # max try counter
            j = False
            while j is False:
                if counter >= svBot.StaticVars.maxTry:
                    return False
                j = True
                try:
                    statePlayer = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.PLAYERWINS)))
                    latestPlayer = int(statePlayer.text)
                except StaleElementReferenceException:
                    j = False
                    counter += 1

            # get banker situation
            counter = 0  # max try counter
            i = False
            while i is False:
                if counter >= svBot.StaticVars.maxTry:
                    return False
                i = True
                try:
                    stateBanker = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.BANKERWINS)))
                    latestBanker = int(stateBanker.text)
                except StaleElementReferenceException:
                    i = False
                    counter += 1


            # No new game played
            if (lastGame == latestGame):
                continue
            # New game played, result analysis
            else:
                iteration += 1

                # update latest game tracker
                lastGame = latestGame

                # player won last game, now what do i do?
                if lastPlayer < latestPlayer:
                    qWinner.append('P')
                    print(qWinner)
                    lastPlayer = latestPlayer
                    if prediction == 100:
                        prediction = 'B'
                    else:
                        if prediction == 'P':
                            prediction = 'B'
                            qPrediction.append('YES')
                            if iteration >= 5:
                                Y += 1
                                if qPrediction[len(qPrediction) - 2] == 'YES':
                                    if betFlag is True:
                                        return False
                                    else:
                                        N = 0
                        elif prediction == 'B':
                            prediction = 'B'
                            qPrediction.append('NO')
                            if iteration >= 5:
                                N += 1

                # Banker won last game, now what do I do?
                elif lastBanker < latestBanker:
                    qWinner.append('B')
                    print(qWinner)
                    lastBanker = latestBanker
                    if prediction == 100:
                        prediction = 'P'
                    else:
                        if prediction == 'B':
                            prediction = 'P'
                            qPrediction.append('YES')
                            if iteration >= 5:
                                Y += 1
                                if qPrediction[len(qPrediction) - 2] == 'YES':
                                    if betFlag is True:
                                        return False
                                    else:
                                        N = 0
                        elif prediction == 'P':
                            prediction = 'P'
                            qPrediction.append('NO')
                            if iteration >= 5:
                                N += 1

            # start betting when value of N reaches 4
            # if N >= 4:
            # Dummy prints to monitor bet activities
            print("iteration:")
            print(iteration)
            print(qWinner)
            print(qPrediction)
            # Temporary N value reduction
            print("value of N")
            print(N)
            if N >= 1:
                betFlag = True
                betSuccess = self.bet(prediction)
                if betSuccess is False:
                    return False
            else:
                waitingForGame += 1
            if waitingForGame == svBot.StaticVars.maxCount:
                return False

    # Master method
    def start(self):
        print("automation initiated")

        try:
            l = self.driver.find_element_by_css_selector(svBot.StaticVars.BALANCEDIV)
        except:
            # maximize browser window
            # driver.maximize_window()

            # initialize verajohn web
            okFlag = 0
            while okFlag == 0:
                try:
                    l = self.driver.find_element_by_css_selector(svBot.StaticVars.MAILINPUT)
                    print("found")
                    okFlag = 1
                # NoSuchElementException thrown if not present
                except NoSuchElementException:
                    print("looking")
                    self.driver.get(svBot.StaticVars.home)

            # grab username and password field
            try:
                username = self.driver.find_element_by_css_selector(svBot.StaticVars.MAILINPUT)
                password = self.driver.find_element_by_css_selector(svBot.StaticVars.PASSINPUT)
            except NoSuchElementException:
                # login fields grabing failed
                return False


            # Flood username and password field with values from static class
            userid = svBot.StaticVars.userId
            userpass = svBot.StaticVars.userPass

            # Account without balance
            # username.send_keys(svBot.StaticVars.userIdWithoutBalance)
            # password.send_keys(svBot.StaticVars.userPassWithoutBalance)

            # Account with balance
            username.send_keys(svBot.StaticVars.userIdWithBalance)
            password.send_keys(svBot.StaticVars.userPassWithBalance)
            time.sleep(2)

            try:
                # Press submit
                submitbtn = self.driver.find_element_by_css_selector(svBot.StaticVars.LOGINBUTTON)
                submitbtn.send_keys(Keys.ENTER)
            except NoSuchElementException:
                # login fields grabing failed
                return False
        l = self.driver.find_element_by_css_selector(svBot.StaticVars.BALANCEDIV)
        print(l.text)
        # driver.get("https://www.verajohn.com/ja/myaccount/overview")
        # elem = driver.find_element_by_xpath('//span[@class="cta_button cta_primary cookie-disclaimer-close"]').click()
        time.sleep(3)
        try:
            self.driver.get(svBot.StaticVars.lobby)
        except:
            return False

        isBetting = self.bettingMethod()
        if isBetting is False:
            return False
        else:
            return True



    def bet(self, prediction):
        # print("bet started")
        # print(prediction + " will win this time!")

        # Get betting amount and push it at the back of the queue
        bet = self.setx.pop(0)
        bettocalculate = bet
        self.setx.append(bet)
        print("betting $" + str(bet))
        print (self.chipsArray)
        chipcount = [0, 0, 0, 0, 0, 0, 0]
        index = 0
        while index < 7:
            if self.chipsArray[index] <= bettocalculate:
                bettocalculate -= self.chipsArray[index]
                chipcount[index] = chipcount[index] + 1
                if self.chipsArray[index] > bettocalculate:
                    index += 1
                else:
                    continue
            index += 1


        # candidateDivs = WebDriverWait(self.driver, 120).until(EC.presence_of_elements_located((By.XPATH, "//div[contains(@class,'title--3u2Hb')]")))

        # grab betting window indicator
        signalDiv = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'status--3gU3H green--365dR landscape--WzE3k animate--2TXsg desktop-theme--T-jLf')]")))

        # Get the two divs that contain player and banker portal
        counter = 0  # max try counter
        k = False
        while k is False:
            if counter >= svBot.StaticVars.maxTry:
                return False
            k = True
            try:
                candidateDivs = self.driver.find_elements_by_css_selector(svBot.StaticVars.PLAYERBANKERCANDIDATEDIVS)
            except:
                k = False
                counter += 1

        for i in candidateDivs:
            try:
                try:
                    print("working with chips")
                    chips = self.driver.find_elements_by_css_selector(svBot.StaticVars.CHIPS)
                    if (prediction == 'P' and i.text == 'プレイヤー') or (prediction == 'B' and i.text == 'バンカー'):
                        for x in chips:
                            value = int(x.text)
                            indx = self.chipsArray.index(value)
                            if chipcount[indx] > 0:
                                result = self.actionChainBet(chipcount[indx], x)
                                if result is False:
                                    return False
                except:
                    return False
                if prediction == 'P' and i.text == 'プレイヤー':
                        print("betting for player")
                        player = self.driver.find_element_by_css_selector(svBot.StaticVars.PLAYERBET)
                        player.click()

                elif prediction == 'B' and i.text == 'バンカー':
                        print("betting for banker")
                        banker = self.driver.find_element_by_css_selector(svBot.StaticVars.BANKERBET)
                        banker.click()

            except:
                continue

    def actionChainBet(self, count, x):
        # get double button
        try:
            # actionchain to click chips
            actions = ActionChains(self.driver)
            actions.move_to_element(x)
            actions.click(x)
            actions.perform()

            # action chain to click double button
            doubleButton = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.XPATH, svBot.StaticVars.DOUBLEBUTTON)))
            actions = ActionChains(self.driver)
            actions.move_to_element(doubleButton)
            actions.click(doubleButton)
            actions.perform()
            # for i in range(count):
        except:
            print("actionchain failed, do something!")
            return False




