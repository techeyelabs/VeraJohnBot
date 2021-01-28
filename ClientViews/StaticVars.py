class StaticVars:
    # System credentials holder
    userId = "unique user id"
    userPass = "Secure"

    # account without balance
    userIdWithoutBalance = "coginc2009@gmail.com"
    userPassWithoutBalance = "!rQzzz2JHEDdP9G"

    # account with balance
    userIdWithBalance = "sarry19741029@gmail.com"
    userPassWithBalance = "sarry1029"

    # Verajohn creds
    verajohnUserId = "unique user id"
    verajohnUserPass = "Secure"

    # System authentication status
    isAuthenticated = False

    # Authentication api centrally stored here
    clientAuthenticationApi = "http://bot.bitpeboot.com/VeraJohnBotApiEndpoints/public/api/userauthentication"

    # VreaJohn URLs
    home = "https://verajohn.com/ja"
    lobby = "https://www.verajohn.com/ja/game/baccarat-lobby-paris"

    # max wait count for table
    maxCount = 35

    # max try count in case of failure
    maxTry = 5

    # css selectors
    CHIPS = "div[class*='chip--1itRi shadow--2_7Gl']"
    PLAYERBET = "div[class*='player--1nDyW']"
    BANKERBET = "div[class*='banker--Q8hMb']"
    PLAYERBANKERCANDIDATEDIVS = "div[class*='title--3u2Hb']"
    BALANCEDIV = "div[class*='navbarMainBalance']"
    LOGINBUTTON = ".button[class*='button form-submit'][id='edit-submit-signin']"
    MAILINPUT = "input[class*='form-text required'][id='signin-mail']"
    PASSINPUT = "input[class*='form-text required'][id='signin-pass']"
    TABLES = "div[class*='TableName--2WO05']"

    # xpaths
    DOUBLEBUTTON = "//button[contains(@class,'button--3h5xe buttonSizeDefault--3mQ1i buttonStateDefault--3rSF6 buttonLabelPositionRight--w4wqn buttonIconPositionLeft--2FL2w buttonThemeDanger--3YUsK buttonModeDesktop--i3Cpv')]"
    PLAYERWINS = "//div[contains(@data-type,'playerWins')]"
    BANKERWINS = "//div[contains(@data-type,'bankerWins')]"
    GAMECOUNT = "//div[contains(@data-type,'gameCount')]"
    IFRAME_1 = "//iframe[contains(@src,'/game/baccarat-lobby-paris/frame')]"
    IFRAME_2 = "//iframe[contains(@name,'innergame')]"
    IFRAME_3 = "//iframe[contains(@name,'EVO_GAME')]"