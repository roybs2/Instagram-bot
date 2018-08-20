import logging.config
import os

def Start():
    try:
        path = r'C:\logs'
        if not os.path.exists(path):
            os.makedirs(path)
        filePath = r"{}\AutoLike-log.log".format(path)
    except Exception as e:
        filePath = r"AutoLike-log.log"

    logging.config.fileConfig('logging.ini', defaults={'logfilename': filePath})
    return logging
