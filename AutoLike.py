import time
import ConfigParser
import LogHandler
import SeleniumConfig
import selenium

class AutoLike:
    def __init__(self):

        self.logger = LogHandler.Start()
        self.logger.getLogger('AutoLike')

        try:
            self.driver = SeleniumConfig.InitSelenium()

            self.config = ConfigParser.ConfigParser()
            self.config.read('config.ini')
            self.userName = self.config.get('DEFAULT','userName')
            self.password = self.config.get('DEFAULT','password')
            self.likeClassName = self.config.get('DEFAULT', 'likeClassName')
            self.unLikeClassName = self.config.get('DEFAULT', 'unLikeClassName')
            self.numberOfLikes = self.config.get('DEFAULT', 'numberOfLikes')

        except Exception as e:
            self.logger.error("Unable to init chrome driver or config file. Exception: %s", e)
            self.driver.close()
            raise Exception('Unable to init')

    def Login(self):
        try:
            self.driver.get(self.config.get('DEFAULT','instagramLogin'))
            time.sleep(2)

            userNameTextBox = self.driver.find_element_by_name('username')
            userNameTextBox.send_keys(self.userName)
            passwordTextBox = self.driver.find_element_by_name('password')
            passwordTextBox.send_keys(self.password)

            loginButton = self.driver.find_element_by_class_name('_5f5mN')
            loginButton.click()
        except Exception as e:
            self.logger.error("Unable to login to instagram with username:{}, psasword:{}. Exception: {}".format(self.userName, self.password, e))
            print "Unable to login to instagram with username:{}, psasword:{}. Exception: {}".format(self.userName, self.password, e)
            self.driver.close()
            raise Exception('Internal Error')


    # select the first option of the search
    def Search(self, Tag):
        searchTextBox = self.driver.find_element_by_class_name('XTCLo')
        searchTextBox.send_keys(Tag)
        time.sleep(1)
        searchResult = self.driver.find_elements_by_class_name('yCE8d')
        searchResult[0].click()



    def AutoLikerForPost(self):
        try:
            likeButton = self.driver.find_element_by_class_name(self.likeClassName)
            likeButton.click()
        except Exception as e:
            try:
                self.driver.find_element_by_class_name(self.unLikeClassName)
                self.logger.info("Post was already liked")
            except Exception as ex:
                self.logger.error("Unable to do like with class name: {}, url: {}. Exception: {}".format(self.likeClassName,
                                                                                                         self.driver.current_url, e))


    def AutoLiker(self, numberOfLiks):
        tags = self.config.get('DEFAULT', 'tags')
        tagPagePrefix = self.config.get('DEFAULT', 'instagramTagPagePrefix')
        postClassName = self.config.get('DEFAULT', 'postClassName')

        listOfTags = tags.split(",")
        for tag in listOfTags:
            try:
                self.driver.get("{}{}".format(tagPagePrefix, tag))

                listOfPosts = self.driver.find_elements_by_class_name(postClassName)
                if(self.numberOfLikes > len(listOfPosts)):
                    maxRange = len(listOfPosts)
                else:
                    maxRange = self.numberOfLikes

                for i in range(0, maxRange):
                    try:
                        listOfPosts[i].click()
                        time.sleep(1)
                        self.AutoLikerForPost()

                        self.driver.execute_script("window.history.go(-1)")
                        time.sleep(1)
                    except Exception as e:
                        self.logger.error("Can not do like for: tag: {}, postClassName: {}. Exception: {}".format(tag, postClassName, e))
                        #raise Exception('Internal Error')

            except Exception as e:
                self.logger.error("Something in the auto liker went wrong. Exception: {}".format(e))
                self.driver.close()
                raise Exception('Internal Error')



    def UploadPost(self, picture, textBox, tags):
        upload = self.driver.find_element_by_class_name('coreSpriteFeedCreation')
        upload.send_keys(picture)

        nextButton = self.driver.find_element_by_class_name('_9glb8')
        nextButton.click()

        text = self.driver.find_element_by_tag_name('textarea')
        text.send_keys(textBox)
        text.send_keys(selenium.webdriver.Keys.RETURN);
        text.send_keys(tags)


    def MainAutoLiker(self):
        self.Login()
        time.sleep(1)
        self.AutoLiker(int(self.numberOfLikes))

        self.driver.close()


#a = AutoLike()
#a.MainAutoLiker()
# to run without flask:
#MainAutoLiker()
