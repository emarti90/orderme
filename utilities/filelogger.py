# Import General Package
import logging
from settings import LOGLEVEL

# Class Log
class Log():
    def __init__(self, logname):
        self.logname = logname
        # Config Log Format
        formattr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Create Handler
        self.handlr = logging.FileHandler(filename='log/qrapp.log', encoding='utf-8')
        self.handlr.setFormatter(formattr)
        self.handlr.setLevel(LOGLEVEL)
        return 
        
    def getLog(self):
        log = logging.getLogger(self.logname)
        log.setLevel(LOGLEVEL)
        log.addHandler(self.handlr)
        return log

    
        

