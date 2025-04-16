import os


SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080


class VPath:
    def __init__(self) -> None:
        self.assets = os.getcwd() + '/assets/'
        self.configs = os.getcwd() + '/assets/configs/'
        self.data = os.getcwd() + '/assets/data/'
        self.images = os.getcwd() + '/assets/images/'
        self.temp = os.getcwd() + '/assets/temp/'
        self.audio = os.getcwd() + '/assets/audio/'

vp = VPath()



class SETTINGS:
    def __new__(cls, *args, **kw):
         if not hasattr(cls, '_instance'):
             orig = super(SETTINGS, cls)
             cls._instance = orig.__new__(cls, *args, **kw)
         return cls._instance
    
    def __init__(self): 
        self.TESTING = True if os.name == 'nt' else False
        if self.TESTING: print(f'\n--- TESTING MODE ---\n')

        #? gui
        self.header_height = 150
        self.volume = 50

        #? Server / Network
        self.plc_ip = '192.168.69.181'
        self.rpi_port = 42001

        self.robot_ip = '192.168.69.120' if os.name == 'nt' else '192.168.69.50'
        # self.robot_ip = '192.168.69.170'
        self.robot_port = 42000
        self.robot_url = f'http://{self.robot_ip}:{self.robot_port}/'

        # self.data_server_ip = 'http://192.168.69.169:80'

    def reset(self):
        pass

settings = SETTINGS()


