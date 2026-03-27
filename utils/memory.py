import threading
from PyQt5.QtCore import *


PROGRAM_NAMES = {
    1: '965-0101-B CALE Door', # CALE
    2: '1881-0150M-B MS3 Door',
    3: '101-0111 (Qty: 1)',
    4: '101-0111 (Qty: 2)',
    5: '101-0111 (Qty: 4)',
    6: '101-108 (Qty: 1)',
    7: '101-108 (Qty: 5)',
    8: '101-108 (Qty: 10)',
    9: '871-025B (Qty: 1)',
    10: '871-025B (Qty: 2)',
    11: '767-2205 B (Qty: 1)',
    12: '767-2205 B (Qty: 2)',
    13: '767-2205 B (Qty: 7)',
    14: '1881-1015 (Qty: 1)',
    15: '1881-1015 (Qty: 2)',
    16: '767-119 Fixture A',
    17: '767-119 Fixture B',
    18: '1881-0151 (Qty: 1)',
    19: '1881-0151 (Qty: 2)',
}


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

        self._program = 0
        self.program_name = '-'
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
    
    def _get_program(self):
        with self.lock:
            return self._program
    def _set_program(self, n):
        with self.lock:
            self._program = n
            self.program_name = PROGRAM_NAMES.get(n, '-')
    program = property(_get_program, _set_program)


mem = MEM()










