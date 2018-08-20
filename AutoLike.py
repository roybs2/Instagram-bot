from selenium import webdriver
import selenium
import time
import ConfigParser
import LogHandler

global driver, userName, password, config, likeClassName, unLikeClassName, logger, numberOfLikes

def Init():
    global driver, config, userName, password, likeClassName, unLikeClassName, logger, numberOfLikes

    logger = LogHandler.Start()
    logger.getLogger('AutoLike')

    try:
        driver = webdriver.Chrome()
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        userName = config.get('DEFAULT','userName')
        password = config.get('DEFAULT','password')
        likeClassName = config.get('DEFAULT', 'likeClassName')
        unLikeClassName = config.get('DEFAULT', 'unLikeClassName')
        numberOfLikes = config.get('DEFAULT', 'numberOfLikes')

    except Exception as e:
        logger.error("Unable to init chrome driver or config file. Exception: %s", e)
        raise Exception('Unable to init')


def Login():
    try:
        driver.get(config.get('DEFAULT','instagramLogin'))
        time.sleep(2)

        userNameTextBox = driver.find_element_by_name('username')
        userNameTextBox.send_keys(userName)
        passwordTextBox = driver.find_element_by_name('password')
        passwordTextBox.send_keys(password)

        loginButton = driver.find_element_by_class_name('_5f5mN')
        loginButton.click()
    except Exception as e:
        logger.error("Unable to login to instagram with username:{}, psasword:{}. Exception: {}".format(userName, password, e))
        raise Exception('Internal Error')


# select the first option of the search
def Search(Tag):
    searchTextBox = driver.find_element_by_class_name('XTCLo')
    searchTextBox.send_keys(Tag)
    time.sleep(1)
    searchResult = driver.find_elements_by_class_name('yCE8d')
    searchResult[0].click()

def ChangeToMobileView():
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.create_options(chrome_options)
    driver.refresh()

def AutoLike():
    try:
        likeButton = driver.find_element_by_class_name(likeClassName)
        likeButton.click()
    except Exception as e:
        try:
            driver.find_element_by_class_name(unLikeClassName)
            logger.info("Post was already liked")
        except Exception as ex:
            logger.error("Unable to do like with class name: {}. Exception: {}".format(likeClassName, e))
            raise Exception('Internal Error')


def AutoLiker(numberOfLiks):
    tags = config.get('DEFAULT', 'tags')
    tagPagePrefix = config.get('DEFAULT', 'instagramTagPagePrefix')
    postClassName = config.get('DEFAULT', 'postClassName')

    listOfTags = tags.split(",")
    for tag in listOfTags:
        try:
            driver.get("{}{}".format(tagPagePrefix, tag))

            listOfPosts = driver.find_elements_by_class_name(postClassName)
            for i in range(0, numberOfLiks):
                try:
                    listOfPosts[i].click()
                    time.sleep(1)
                    AutoLike()

                    driver.execute_script("window.history.go(-1)")
                    time.sleep(1)
                except Exception as e:
                    logger.error("Can not do like for: tag: {}, postClassName: {}. Exception: {}".format(tag, postClassName, e))
                    raise Exception('Internal Error')

        except Exception as e:
            logger.error("Something in the auto liker went wrong. Exception: {}".format(e))
            raise Exception('Internal Error')



def UploadPost(picture, textBox, tags):
    upload = driver.find_element_by_class_name('coreSpriteFeedCreation')
    upload.send_keys(picture)

    nextButton = driver.find_element_by_class_name('_9glb8')
    nextButton.click()

    text = driver.find_element_by_tag_name('textarea')
    text.send_keys(textBox)
    text.send_keys(selenium.webdriver.Keys.RETURN);
    text.send_keys(tags)


def MainAutoLiker():
    Init()
    Login()

    time.sleep(1)
    AutoLiker(int(numberOfLikes))

    driver.close()


