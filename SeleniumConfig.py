import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ConfigParser
import LogHandler

global logger
logger = LogHandler.Start()

def InitSelenium():
    try:

        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        try:
            optionsString = config.get('DEFAULT','chromeOptions')
            optionsList = optionsString.split(",")

            chrome_options = Options()

            for option in optionsList:
                chrome_options.add_argument(option)

            driver = webdriver.Chrome(chrome_options=chrome_options)
        except:
            logger.info("Chrome options don't exist")
            driver = webdriver.Chrome()


        return driver
    except Exception as e:
        logger.error("Unable to config web driver. Exception: {}".format(e))


# def ChangeToMobileView():
#     mobile_emulation = {"deviceName": "Nexus 5"}
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
#     #driver = webdriver.Chrome(chrome_options=chrome_options)
#     driver.create_options(chrome_options)
#     driver.refresh()