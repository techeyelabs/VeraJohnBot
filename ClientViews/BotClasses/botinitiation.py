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
        self.emptyQueue = False
        self.multiple = 1
        self.setx = [1 * self.multiple, 2 * self.multiple, 3 * self.multiple, 5 * self.multiple, 7 * self.multiple, 10 * self.multiple,
               15 * self.multiple, 22 * self.multiple, 33 * self.multiple, 48 * self.multiple, 72 * self.multiple]

    # check if game has paused
    def pauseCheck(self):
        try:
            l = self.driver.find_element_by_css_selector(svBot.StaticVars.CLICABLEPAUSEOVERLAY)
            l.click()
        except:
            abc = "ok"
        return True

    # check if irritating popups has come up
    def modalCheck(self):
        try:
            l = self.driver.find_element_by_css_selector(svBot.StaticVars.IRRITATING_POPUPS)
            l.click()
        except:
            abc = "ok"
        return True

        # check if irritating popups has come up

    def sessionLogoutCheck(self):
        try:
            l = self.driver.find_element_by_css_selector(svBot.StaticVars.SESSION_LOGOUT_DIV)
            if l.text is not None:
                print(l.text)
                l.click()
                return False
            print("hello there, session logged out.")
        except:
            return True
        return True

    # check if 60 mins popup has come
    def popUpCheck(self):
        try:
            prompt = self.driver.find_element_by_css_selector(svBot.StaticVars.PROMPT)
            prompt.click()
        except NoSuchElementException:
            abc = "ok"
        return True

    # Parse through iframes to get to the tables
    def initiateTables(self):
        check = self.pauseCheck()  # Check if game has paused
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
            print("line 50")
            return False



    # Read potential tables to read their present gamecounts
    def lookForTables(self, tableStatusParam, tablesParam):
        check = self.pauseCheck()
        tableStatus = tableStatusParam
        tables = tablesParam

        for idx, t in enumerate(tables):
            try:
                b = self.driver.find_elements_by_css_selector(svBot.StaticVars.TABLES)
            except:
                print("line 63")
                return False
            if (len(b) == 0):
                b = False
                while (b == False):
                    b = self.initiateTables()
                    if b is False:
                        print("line 100")
                        return False
            try:
                for tls in b:
                    if tls.text == t:
                        # get overflown tables into view as they might not be initially clicable
                        tls.location_once_scrolled_into_view
                        try:
                            tls.click()
                            time.sleep(15)
                            # get the count of hands played in this table
                            counterDivs = WebDriverWait(self.driver, 4).until(
                                EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                            tableStatus[idx] = counterDivs.text
                        except:
                            tableStatus[idx] = '0'
                        # if int(counterDivs.text) >= 60:
                        #     return [tableStatus, tables]
                        print(tableStatus)
                        self.driver.back()
                        time.sleep(20)
                        break
            except:
                print("line 89")
                return False
        return [tableStatus, tables]

    # Loop through tables to select one
    def loopTables(self, b, selectedTable):
        check = self.pauseCheck()
        try:
            for tlsS in b:
                if tlsS.text == selectedTable:
                    tlsS.location_once_scrolled_into_view
                    tlsS.click()
                    time.sleep(25)
                    answer = self.operateTable()
                    if answer is False:
                        print("line 152")
                        return False
                    break
            return True
        except:
            print("line 105")
            return False

    # Start operationg on the selected table
    def operateTable(self):
        check = self.pauseCheck()
        checkPopUp = self.popUpCheck()
        # stop waiting for beginnign of table (remove later)
        counterDivs = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
        print(counterDivs.text)

        whenStarted = counterDivs.text

        # wait until table restarts
        while whenStarted != '0':
            result = self.sessionLogoutCheck()
            if result is False:
                print("line 172")
                return False
            try:
                check = self.pauseCheck()
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
        return True

    def bettingMethod(self):
        check = self.pauseCheck()  # Check if game has paused

        counter = 0  # max try counter

        b = self.initiateTables()
        while b is False:
            if counter >= svBot.StaticVars.maxTry:
                print("line 181")
                return False
            b = self.initiateTables()
            counter += 1

        print(len(b))  # initiated tables display

        tableStatus = ['0', '0', '0', '0', '0']
        tables = [
            "スピードバカラ A",
            "スピードバカラ B",
            "バカラ A",
            "バカラ B",
            "バカラ C"
        ]

        counter = 0  # max try counter
        tablesSearch = False
        while tablesSearch is False:
            if counter >= svBot.StaticVars.maxTry:
                print("line 166")
                return False
            tablesSearch = self.lookForTables(tableStatus, tables)
            counter += 1

        tableStatus = tablesSearch[0]
        tables = tablesSearch[1]

        tableStatus = list(map(int, tableStatus))  # convert string array to int array

        # display all table statuses
        print("tables")
        print(tableStatus)

        maxVal = tableStatus.index(max(tableStatus))  # get to table list again

        selectedTable = tables[maxVal]  # get selected table name

        # walk through iframes to get to tables again
        counter = 0  # max try counter
        b = False
        while (b is False):
            if counter >= svBot.StaticVars.maxTry:
                print("line 224")
                return False
            b = self.initiateTables()
            counter += 1

        # get into selected table
        counter = 0  # max try counter
        targetTable = False
        while targetTable is False:
            if counter >= svBot.StaticVars.maxTry:
                print("line 234")
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
                print("line 247")
                return False
            threeCounts = True
            try:
                GameCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                playerWinCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.PLAYERWINS)))
                bankerWinCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.BANKERWINS)))
                tieCount = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, svBot.StaticVars.TIES)))
            except:
                threeCounts = False
                counter += 1

        print("initial game count: " + GameCount.text)
        print("initial banker count: " + bankerWinCount.text)
        print("initial player count: " + playerWinCount.text)
        print("initial ties count: " + tieCount.text)
        logoutSituation = self.sessionLogoutCheck()
        if logoutSituation is False:
            print("line 291")
            return False

        # Here some notations will be used. they are as follows:
        # P: Player
        # B: Banker
        # Y: Yes
        # N: No
        # NA: Result doesn't exist
        # D: Draw

        # set tracking values of game, player and banker
        lastGame = int(GameCount.text)
        lastPlayer = int(bankerWinCount.text)
        lastBanker = int(playerWinCount.text)
        lastTie = int(tieCount.text)

        qWinner = []  # queue to keep track of winners

        qPrediction = ['NONE']  # queue to keep track of prediction results
        prediction = 100  # Initial prediction assignment
        iteration = 0  # Total games played

        # Yes/No track
        Y = 0
        N = 0

        waitingForGame = 0  # waiting games track
        betFlag = False  # bet start flag
        consWins = 0  # consecutive win track

        # infinite loop to monitor the table
        while True:
            logoutSituationAgain = self.sessionLogoutCheck()
            if logoutSituationAgain is False:
                print("line 326")
                return False
            check = self.pauseCheck()
            checkPopUp = self.popUpCheck()
            time.sleep(1)
            # ignored exception array
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

            # get total game situation
            counter = 0  # max try counter
            k = False
            while k is False:
                if counter >= svBot.StaticVars.maxTry:
                    print("line 305")
                    return False
                k = True
                try:
                    stateGame = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.GAMECOUNT)))
                    latestGame = int(stateGame.text)
                except:
                    k = False
                    counter += 1

            # get player situation
            counter = 0  # max try counter
            j = False
            while j is False:
                if counter >= svBot.StaticVars.maxTry:
                    print("line 295")
                    return False
                j = True
                try:
                    statePlayer = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.PLAYERWINS)))
                    latestPlayer = int(statePlayer.text)
                except:
                    j = False
                    counter += 1

            # get banker situation
            counter = 0  # max try counter
            i = False
            while i is False:
                if counter >= svBot.StaticVars.maxTry:
                    print("line 341")
                    return False
                i = True
                try:
                    stateBanker = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.BANKERWINS)))
                    latestBanker = int(stateBanker.text)
                except:
                    i = False
                    counter += 1

            # get tie situation
            counter = 0  # max try counter
            l = False
            while l is False:
                if counter >= svBot.StaticVars.maxTry:
                    print("line 357")
                    return False
                l = True
                try:
                    stateTie = WebDriverWait(self.driver, 120, ignored_exceptions=ignored_exceptions).until(
                        EC.presence_of_element_located((By.XPATH, svBot.StaticVars.TIES)))
                    latestTie = int(stateTie.text)
                except:
                    l = False
                    counter += 1


            # No new game played
            if (lastGame == latestGame):
                continue
            # New game played, result analysis
            else:
                check = self.pauseCheck()
                iteration += 1

                # update latest game tracker
                lastGame = latestGame

                # Last game is tied, now what do I do?
                if lastTie < latestTie:
                    print("line 376 (Tie)")
                    qWinner.append('D')
                    print(qWinner)
                    lastTie = latestTie
                    iteration -= 1
                    qPrediction.append('TIED')

                # player won last game, now what do i do?
                elif lastPlayer < latestPlayer:
                    qWinner.append('P')
                    print(qWinner)
                    lastPlayer = latestPlayer
                    if prediction == 100:
                        prediction = 'B'
                    else:
                        if prediction == 'P':
                            prediction = 'B'
                            qPrediction.append('YES')
                            if iteration >= 6:
                                Y += 1
                                if qPrediction[len(qPrediction) - 2] == 'YES':
                                    if betFlag is True:
                                        print("line 349")
                                        return False
                                    else:
                                        N = 0
                                else:
                                    yCount = 0
                                    for i in reversed(qPrediction):
                                        if i == "NO":
                                            break
                                        elif i == "TIED":
                                            continue
                                        elif i == "YES":
                                            yCount = yCount + 1
                                            if yCount == 2 and betFlag is True:
                                                print("line 418")
                                                return False

                        elif prediction == 'B':
                            prediction = 'B'
                            qPrediction.append('NO')
                            if iteration >= 6:
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
                            if iteration >= 6:
                                Y += 1
                                if qPrediction[len(qPrediction) - 2] == 'YES':
                                    if betFlag is True:
                                        print("line 374")
                                        return False
                                    else:
                                        N = 0
                                else:
                                    yCount = 0
                                    for i in reversed(qPrediction):
                                        if i == "NO":
                                            break
                                        elif i == "TIED":
                                            continue
                                        elif i == "YES":
                                            yCount = yCount + 1
                                            if yCount == 2 and betFlag is True:
                                                print("line 456")
                                                return False
                        elif prediction == 'P':
                            prediction = 'P'
                            qPrediction.append('NO')
                            if iteration >= 6:
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

            if N >= 4:
                check = self.pauseCheck()
                before_last = qPrediction[len(qPrediction) - 2]
                last = qPrediction[len(qPrediction) - 1]
                betFlag = True
                if last == "TIED":
                    for i in reversed(qPrediction):
                        if i == "TIED":
                            continue
                        elif i == "YES":
                            repeatDouble = True
                            break
                        elif i == "NO":
                            break

                else:
                    repeatDouble = False
                betSuccess = self.bet(prediction, last, repeatDouble)
                betSuccess = True
                if betSuccess is False:
                    print("line 460")
                    return False
            else:
                waitingForGame += 1
            if waitingForGame == svBot.StaticVars.maxCount:
                print("line 465")
                return False

    # Master method
    def start(self):
        check = self.pauseCheck()
        print("automation initiated")

        try:
            print("automation initiated try")
            # maximize browser window
            # driver.maximize_window()

            self.driver.get(svBot.StaticVars.home)

            try:
                time.sleep(5)
                username = self.driver.find_element_by_css_selector(svBot.StaticVars.MAILINPUT)
                password = self.driver.find_element_by_css_selector(svBot.StaticVars.PASSINPUT)
                # Account with balance
                username.send_keys(svBot.StaticVars.userIdFlawTest)
                password.send_keys(svBot.StaticVars.userPassFlawTest)
                time.sleep(2)
                try:
                    # Press submit
                    submitbtn = self.driver.find_element_by_css_selector(svBot.StaticVars.LOGINBUTTON)
                    submitbtn.send_keys(Keys.ENTER)
                except NoSuchElementException:
                    # login fields grabing failed
                    print("line 484")
                    return False
            except NoSuchElementException:
                # login fields grabing failed
                print("hello")
        except:
            print("line 490")

        time.sleep(3)
        try:
            self.driver.get(svBot.StaticVars.lobby)
        except:
            print("line 496")
            return False
        time.sleep(10)
        self.modalCheck()
        # driver.get("https://www.verajohn.com/ja/myaccount/overview")
        # elem = driver.find_element_by_xpath('//span[@class="cta_button cta_primary cookie-disclaimer-close"]').click()
        self.setx = [1 * self.multiple, 2 * self.multiple, 3 * self.multiple, 5 * self.multiple, 7 * self.multiple, 10 * self.multiple,
                     15 * self.multiple, 22 * self.multiple, 33 * self.multiple, 48 * self.multiple, 72 * self.multiple]

        isBetting = self.bettingMethod()
        if isBetting is False:
            print("line 472")
            return False
        else:
            return True

    def bet(self, prediction, last, repeatDouble):
        logoutCheckInBet = self.sessionLogoutCheck()
        if logoutCheckInBet is False:
            print("line 591")
            return False
        check = self.pauseCheck()
        # print("bet started")
        # print(prediction + " will win this time!")
        print("setx after")
        print(self.setx)
        if last == "YES":
            bet = self.setx[len(self.setx) - 1] * 2
        elif last == "TIED":
            if repeatDouble == True:
                bet = self.setx[len(self.setx) - 1] * 2
            else:
                bet = self.setx[len(self.setx) - 1]
        else:
            if self.emptyQueue is True:
                print("line 541")
                return False
            # Get betting amount and push it at the back of the queue
            bet = self.setx.pop(0)
            self.setx.append(bet)
        print("setx after")
        print(self.setx)
        if self.setx[len(self.setx) - 1] == 72:
            self.emptyQueue = True
        bettocalculate = bet

        print (self.chipsArray)
        chipcount = [0, 0, 0, 0, 0, 0, 0]
        doublecount = 0
        if bettocalculate == 22 or bettocalculate == 44:
            doublecount = 1 if bettocalculate == 22 else 2
            bettocalculate = 11
        elif bettocalculate == 72 or bettocalculate == 144:
            doublecount = 1 if bettocalculate == 72 else 2
            bettocalculate = 36
        elif bettocalculate == 20:
            doublecount = 1
            bettocalculate = 10
        elif bettocalculate == 48 or bettocalculate == 96:
            doublecount = 2 if bettocalculate == 48 else 3
            bettocalculate = 12
        elif bettocalculate == 2 or bettocalculate == 4:
            doublecount = 1 if bettocalculate == 2 else 2
            bettocalculate = 1
        else:
            doublecount = 0

        index = 0
        print("to bet")
        print(bettocalculate)
        while index < 7:
            if self.chipsArray[index] <= bettocalculate:
                bettocalculate -= self.chipsArray[index]
                chipcount[index] = chipcount[index] + 1
                if self.chipsArray[index] > bettocalculate:
                    True
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
                print("line 513")
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
                        print("betting $" + str(bet))

                        print("chips count")
                        print(chipcount)

                        for x in chips:
                            val = int(x.get_attribute('data-value'))
                            if val in self.chipsArray:
                                indx = self.chipsArray.index(val)
                                if chipcount[indx] > 0:
                                    if prediction == 'P' and i.text == 'プレイヤー':
                                        print("betting for player")
                                        horse = self.driver.find_element_by_css_selector(svBot.StaticVars.PLAYERBET)
                                    elif prediction == 'B' and i.text == 'バンカー':
                                        print("betting for banker")
                                        horse = self.driver.find_element_by_css_selector(svBot.StaticVars.BANKERBET)
                                    result = self.actionChainBet(chipcount[indx], x, horse)

                                    print("line 583")
                                    print("double count3")
                                    print(doublecount)
                                    if result is False:
                                        print("line 534")
                                        return False
                        print("double count1")
                        print(doublecount)
                        if doublecount > 0:
                            print("double count2")
                            print(doublecount)
                            resultdouble = self.actionChainDouble(doublecount)
                            if resultdouble is False:
                                print("line 650")
                                return False
                except:
                    print("line 537")
                    return False

            except:
                continue

    def actionChainDouble(self, doublecount):
        for i in range(doublecount):
            # action chain to click double button
            db = self.driver.find_element_by_css_selector(svBot.StaticVars.DOUBLE_BUTTON1)
            actions_double = ActionChains(self.driver)
            actions_double.move_to_element(db)
            try:
                print("double time")
                actions_double.click(db)
                actions_double.perform()
            except:
                print("double click failed, do something!")
                print("line 644")
                return False

    def actionChainBet(self, count, x, horse):
        print("actionchain reached")
        print(int(x.get_attribute('data-value')))
        # get double button
        try:
            print("times")
            print(count)
            print("chip")
            print(x.text)
            # actionchain to click chips
            actions = ActionChains(self.driver)
            actions.move_to_element(x)
            actions.click(x)
            actions.perform()

            for i in range(count):
                # action chain to click double button
                try:
                    print("click 1")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(x)
                    actions.click(x)
                    actions.perform()
                    horse.click()
                except:
                    True

        except:
            print("actionchain failed, do something!")
            print("line 675")
            return False




