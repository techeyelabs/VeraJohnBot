class StaticVars:
    #Global host
    host = "http://bot.bitpeboot.com/VeraJohnBotApiEndpoints/public/api"

    # System credentials holder
    userId = "unique user id"
    userPass = "Secure"

    # account for logic flaw testing (kuni)
    userIdFlawTest = "mskmskmsk4@gmail.com"
    userPassFlawTest = "Z2cKT3VGsx6M@86"

    # account without balance (kuni)
    userIdWithoutBalance = "coginc2009@gmail.com"
    userPassWithoutBalance = "!rQzzz2JHEDdP9G"

    # account with balance (main client)
    userIdWithBalance = "sarry19741029@gmail.com"
    userPassWithBalance = "sarry1029"

    # alternate account (new)
    userIdAlter = "mikata@marp.com.sg"
    userPassAlter = "love0614"

    # Verajohn creds
    verajohnUserId = "unique user id"
    verajohnUserPass = "Secure"

    # System authentication status
    isAuthenticated = False

    # Authentication api centrally stored here
    clientAuthenticationApi = host + "/userauthentication"

    # Bet log keeping api
    betLogApi = host + "/bet-log"

    # VreaJohn URLs
    home = "https://verajohn.com/ja"
    lobby = "https://www.verajohn.com/ja/game/baccarat-lobby-paris"

    # max wait count for table
    maxCount = 35  #35 actually

    # max try count in case of failure
    maxTry = 3

    # css selectors
    CHIPS = "div[class*='chip--1itRi shadow--2_7Gl']"
    PLAYERBET = "div[class*='player--1nDyW']"
    BANKERBET = "div[class*='banker--Q8hMb']"
    PLAYERBANKERCANDIDATEDIVS = "div[class*='title--3u2Hb']"
    LOGINBUTTON = ".button[class*='button form-submit'][id='edit-submit-signin']"
    MAILINPUT = "input[class*='form-text required'][id='signin-mail']"
    PASSINPUT = "input[class*='form-text required'][id='signin-pass']"
    TABLES = "div[class*='TableName--2WO05']"
    CLICABLEPAUSEOVERLAY = "div[class*='clickable--3IFrf']"
    PROMPT = "a[class*='lightboxClose']"
    UNAVAILABLE = "div[class*='label--2kPAA labelCapitalized--3pF45']"
    IRRITATING_POPUPS = "button[class*='n-button n-button--tertiary form-input-button']"

    DOUBLE_BUTTON1 = "li[class*='double--2JCkY']"
    DOUBLE_BUTTON2 = "button[data-role*='double-button']"
    DOUBLE_BUTTON3 = "span[data-role*='button-bordered']"
    DOUBLE_BUTTON4 = "span[class*='bordered--3kSwE borderedWithIcon--b2oEs roundingBoth--177dl']"

    SESSION_LOGOUT_SPAN = "span[class*='bordered--3kSwE roundingBoth--177dl']"
    SESSION_LOGOUT_DIV = "div[class*='buttonContainerItem--286mU restrictedMinWidth--1yzrO']"

    # xpaths
    DOUBLEBUTTON = "//button[contains(@class,'button--3h5xe buttonSizeDefault--3mQ1i buttonStateDefault--3rSF6 buttonLabelPositionRight--w4wqn buttonIconPositionLeft--2FL2w buttonThemeDanger--3YUsK buttonModeDesktop--i3Cpv')]"
    PLAYERWINS = "//div[contains(@data-type,'playerWins')]"
    BANKERWINS = "//div[contains(@data-type,'bankerWins')]"
    TIES = "//div[contains(@data-type,'ties')]"
    GAMECOUNT = "//div[contains(@data-type,'gameCount')]"
    IFRAME_1 = "//iframe[contains(@src,'/game/baccarat-lobby-paris/frame')]"
    IFRAME_2 = "//iframe[contains(@name,'innergame')]"
    IFRAME_3 = "//iframe[contains(@name,'EVO_GAME')]"
    NAVA = "//div[contains(@class,'cash-balance')]"
    POPUP_CLOSE = "//div[contains(@class,'lightboxClose js-close')]"



    # popup close
    # lightboxClose js-close