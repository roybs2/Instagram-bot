import ConfigParser
import LogHandler
import SeleniumConfig
import time

global driver, userName, password, config, logger

def Init():
    global driver, config, userName, password, logger
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    logger = LogHandler.Start()
    logger.getLogger('AutoLike')


def Login():
    Init()
    try:
        driver = SeleniumConfig.SeleniumConfiguration()
        driver = driver.Driver
        driver.get(config.get('DEFAULT','instagramLogin'))
        time.sleep(2)

        userNameTextBox = driver.find_element_by_name('username')
        userNameTextBox.send_keys(config.get('DEFAULT','userName'))
        passwordTextBox = driver.find_element_by_name('password')
        passwordTextBox.send_keys(config.get('DEFAULT','password'))

        loginButton = driver.find_element_by_class_name('_5f5mN')
        loginButton.click()
    except Exception as e:
        logger.error("Unable to login to instagram with username:{}, psasword:{}. Exception: {}".format(userName, password, e))
        raise Exception('Internal Error')
