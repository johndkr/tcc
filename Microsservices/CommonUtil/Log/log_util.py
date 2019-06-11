import os
import datetime

LOG_FILE_PATH = './logs/log_file_{}'.format(str(datetime.date.today()).replace('-','_'))
TEMPLATE = '[{}] - {} : {}\n' ## time, type, msg

class Log_Util():
    def __init__(self, make_file):
        self.__make_file = make_file
        # self.__log_file = self.__load_log_file()

    def __load_log_file(self):
        ## this method tries to load a log_file for the day. If it does not exists, it returns None
        try:
            log_file = open(LOG_FILE_PATH, 'a').read()
        except Exception as err:
            print('Error while loading {}:\n{}'.format(LOG_FILE_PATH, str(err)))
            log_file = None
        finally:
            return log_file

    def __write_on_file(self, msg):
        try:
            print(msg)
            if(self.__make_file):
                with open(LOG_FILE_PATH, 'a') as log_file:
                    log_file.write(msg)
        except Exception as err:
            print('Error while loading {}:\n{}'.format(LOG_FILE_PATH, str(err)))

    def __template(self, log_type, msg):
        return TEMPLATE.format(str(datetime.datetime.now()), log_type, msg)

    def info(self, msg):
        # self.__log_file.write(self.__template("INFO", msg))
        self.__write_on_file(self.__template("INFO", msg))

    def debbug(self, msg):
        # self.__log_file.write(self.__template("DEBBUG", msg))
        self.__write_on_file(self.__template("DEBBUG", msg))

    def err(self, msg):
        # self.__log_file.write(self.__template("ERROR", msg))
        self.__write_on_file(self.__template("ERROR", msg))

    
