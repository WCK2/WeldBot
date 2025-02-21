import threading
from PyQt5.QtCore import *


#~ memory class
class MEM(QObject):
    new_status = pyqtSignal()
    log_message = pyqtSignal()
    new_part_request = pyqtSignal()
    flag_change = pyqtSignal(str)
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

        #? part requests
        # self.part_name = ''
        # self.part_id = ''
        self._part_request = {}
        self._flag_part_request_running = False
        self._flag_place_part = False
        self._flag_in_place = False
        self._flag_return_to_pickup = False

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

    def _get_part_request(self):
        with self.lock:
            return self._part_request
    def _set_part_request(self, d):
        with self.lock:
            self._part_request = d
        self.new_part_request.emit()
    part_request = property(_get_part_request, _set_part_request)

    def _get_flag_part_request_running(self):
        with self.lock:
            return self._flag_part_request_running
    def _set_flag_part_request_running(self, s):
        with self.lock:
            self._flag_part_request_running = s
        self.flag_change.emit('flag_part_request_running')
    flag_part_request_running = property(_get_flag_part_request_running, _set_flag_part_request_running)

    def _get_flag_place_part(self):
        with self.lock:
            return self._flag_place_part
    def _set_flag_place_part(self, s):
        with self.lock:
            self._flag_place_part = s
        self.flag_change.emit('flag_place_part')
    flag_place_part = property(_get_flag_place_part, _set_flag_place_part)

    def _get_flag_in_place(self):
        with self.lock:
            return self._flag_in_place
    def _set_flag_in_place(self, s):
        with self.lock:
            self._flag_in_place = s
        self.flag_change.emit('flag_in_place')
    flag_in_place = property(_get_flag_in_place, _set_flag_in_place)

    def _get_flag_return_to_pickup(self):
        with self.lock:
            return self._flag_return_to_pickup
    def _set_flag_return_to_pickup(self, s):
        with self.lock:
            self._flag_return_to_pickup = s
        self.flag_change.emit('flag_return_to_pickup')
    flag_return_to_pickup = property(_get_flag_return_to_pickup, _set_flag_return_to_pickup)


mem = MEM()










