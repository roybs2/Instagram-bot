from InstagramAPI import InstagramAPI
import ConfigParser
import LogHandler
import imp
singletonClass = imp.load_source('Singleton', 'Utilities/Singleton.py')

@singletonClass.singleton
class Upload:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')

        self.logger = LogHandler.Start()
        self.logger.getLogger('AutoLike')

        self.captionTags = config.get('DEFAULT','tags')
        self.InstagramAPI = InstagramAPI(config.get('DEFAULT','userName'), config.get('DEFAULT','password'))
        self.InstagramAPI.login()  # login

    def UploadPost(self, postPath, title):
        try:
            tags = '#' + self.captionTags
            tags = tags.replace(',', ' #')
            caption = title + ' ' + tags
            self.InstagramAPI.uploadPhoto(postPath, caption=caption)
        except Exception as e:
            self.logger.error(
                "Unable to upload post! post path: {}, caption: {}. Exception: {}".format(postPath, caption, e))
            raise Exception('Unable to upload post!')


a = Upload()
a.UploadPost(r'C:\Roy-Personal\temp\workHard.jpg', 'Work hard play hard! ')

#photo_path = r'C:\Roy-Personal\temp\14_14.jpg'
