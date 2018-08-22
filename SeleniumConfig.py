from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ConfigParser
import LogHandler
import imp
singletonClass = imp.load_source('Singleton', 'Utilities/Singleton.py')

global logger
logger = LogHandler.Start()


#selenium configuration need to happen once.
@singletonClass.singleton
class SeleniumConfiguration():
    def __init__(self):
        try:
            self.a = 1
            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            try:
                optionsString = config.get('DEFAULT', 'chromeOptions')
                optionsList = optionsString.split(",")
                self.chrome_options = Options()

                for option in optionsList:
                    self.chrome_options.add_argument(option)

                self.Driver = webdriver.Chrome(chrome_options=self.chrome_options)
            except:
                logger.info("Chrome options don't exist")
                self.Driver = webdriver.Chrome()
        except Exception as e:
            logger.error("Unable to config web driver. Exception: {}".format(e))

    # def ChangeToMobileView(self):
    #     mobile_emulation = {"deviceName": "iPhone X"}
    #     chrome_options = webdriver.ChromeOptions()
    #     chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    #     # driver = webdriver.Chrome(chrome_options=chrome_options)
    #     self.Driver.create_options(chrome_options)
    #     self.Driver.refresh()

# def InitSelenium():
#     try:
#         config = ConfigParser.ConfigParser()
#         config.read('config.ini')
#         try:
#             optionsString = config.get('DEFAULT','chromeOptions')
#             optionsList = optionsString.split(",")
#
#             chrome_options = Options()
#
#             for option in optionsList:
#                 chrome_options.add_argument(option)
#
#             driver = webdriver.Chrome(chrome_options=chrome_options)
#         except:
#             logger.info("Chrome options don't exist")
#             driver = webdriver.Chrome()
#
#
#         return driver
#     except Exception as e:
#         logger.error("Unable to config web driver. Exception: {}".format(e))

