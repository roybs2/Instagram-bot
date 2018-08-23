from InstagramAPI import InstagramAPI
import ConfigParser
import LogHandler
import imp
import os
import base64
import AutoLike
from google_images_download import google_images_download
from random import randint
import schedule
singletonClass = imp.load_source('Singleton', 'Utilities/Singleton.py')

@singletonClass.singleton
class Upload:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')

        self.logger = LogHandler.Start()
        self.logger.getLogger('AutoLike')

        self.captionTags = self.config.get('DEFAULT','tags')
        self.InstagramAPI = InstagramAPI(self.config.get('DEFAULT','userName'), self.config.get('DEFAULT','password'))
        self.InstagramAPI.login()  # login

        #Download pictures:
        self.searchKeyword = "best success quotes"
        argumnets = {
            "keywords": self.searchKeyword,
            "limit": 50,
            "print_urls": True
        }
        response = google_images_download.googleimagesdownload()
        self.images = response.download(argumnets)

    def UploadPost(self, postPath, title):
        try:
            tags = '#' + self.captionTags
            tags = tags.replace(',', ' #')
            caption = title + ' ' + tags

            self.InstagramAPI = InstagramAPI(self.config.get('DEFAULT', 'userName'), self.config.get('DEFAULT', 'password'))
            self.InstagramAPI.login()  # login

            self.InstagramAPI.uploadPhoto(postPath, caption=caption)
        except Exception as e:
            self.logger.error(
                "Unable to upload post! post path: {}, caption: {}. Exception: {}".format(postPath, caption, e))
            raise Exception('Unable to upload post!')

    def CheckIfImageExistInFolder(self, image):
        s = image.rfind('\\')
        folderPath = image[:s]
        print folderPath
        print image
        for file in os.listdir(folderPath):
            if base64.b64encode(file) == base64.b64encode(image):
                return False
        return True

    def AutoUploadImage(self):
        randomNumber = randint(0,50)
        randomTitle = randint(0, 9)
        title = self.config.get('DEFAULT', 'titles').split(',')[randomTitle]
        # todo: add check if file is image
        if self.CheckIfImageExistInFolder(self.images[self.searchKeyword][randomNumber]):
            self.UploadPost(self.images[self.searchKeyword][randomNumber], title)

    def ScheduleUpload(self):
        schedule.every().hour.do(self.AutoUploadImage)
        schedule.every(70).minutes.do(AutoLike.MainAutoLiker)
        while 1:
            schedule.run_pending()

#photo_path = r'C:\Roy-Personal\temp\14_14.jpg'


a= Upload()
a.ScheduleUpload()


# searchKeyword = "best success quotes"
# argumnets = {
#         "keywords": searchKeyword,
#         "limit": 3,
#         "print_urls": True
#     }
#
# response = google_images_download.googleimagesdownload()
# images = response.download(argumnets)
# a = Upload()
# for imagePath in images[searchKeyword]:
#     if a.CheckIfImageExistInFolder(imagePath):
#         a.UploadPost(imagePath, 'So, how was your day? :)')
#         time.sleep(15)
#



