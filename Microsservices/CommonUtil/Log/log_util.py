import os, sys
import datetime

LOG_FILE_PATH = '.\\logs\\log_file_{}'.format(str(datetime.date.today()).replace('-','_'))
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE_PATH)
TEMPLATE = '[{}] - {} : {}' ## time, type, msg

class Log_Util():
    def __init__(self, make_file):
        self.__make_file = make_file
        if not os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, 'w'): pass
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
                mode = 'a' if os.path.isfile(LOG_FILE_PATH) else 'w'
                with open(LOG_FILE_PATH, mode) as log_file:
                    log_file.write(msg + '\n')
        except Exception as err:
            print('Error while loading {}:\n{}'.format(LOG_FILE_PATH, err.__doc__))

    def __template(self, log_type, msg):
        return TEMPLATE.format(str(datetime.datetime.now()), log_type, msg)

    def info(self, msg):
        self.__write_on_file(self.__template("INFO", msg))

    def debbug(self, msg):
        self.__write_on_file(self.__template("DEBBUG", msg))

    def err(self, msg):
        self.__write_on_file(self.__template("ERROR", msg))

    def exception(self, err):
        ## handles Exception types directly. Concentrates the template here
        if type(err) != type(str):
            self.err("{} - {}".format(sys.exc_info()[0], err.__doc__))
        else:
            self.err(err)
        
    
