import threading
from PyQt5.QtCore import *


#~ memory class
class MEM(QObject):
    new_status = pyqtSignal()
    log_message = pyqtSignal()
    def __new__(cls, *args, **kw):
         if not hasattr(cls, '_instance'):
             orig = super(MEM, cls)
             cls._instance = orig.__new__(cls, *args, **kw)
         return cls._instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.Lock()
        self.page_count = 1 # updates in main.py

        #? system controls
        self.start = False
        self.stop = False

        self.page = 0
        self._status = 'Booting'
        self._log = ''

        self.program = 1

    def _get_status(self):
        with self.lock:
            return self._status
    def _set_status(self, s):
        with self.lock:
            self._status = s
        self.new_status.emit()
    status = property(_get_status, _set_status)

    def _get_log(self):
        with self.lock:
            return self._log
    def _set_log(self, s):
        with self.lock:
            self._log = s
        self.log_message.emit()
    log = property(_get_log, _set_log)
    

mem = MEM()










