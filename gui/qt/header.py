import time
import datetime
from gui.qt.common import *
from utils.config import settings
from gui.workers.tpost import post_req_async


class TopHeader(QLabel):
    _next_page = pyqtSignal()
    _previous_page = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(QRect(0, 0, settings.header_height, SCREEN_HEIGHT))
        self.setFixedSize(SCREEN_WIDTH, settings.header_height)
        self.setObjectName('header')

        #~ Header
        header_container = QFrame(self, objectName='banner')
        header_container.setGeometry(QRect(0, 0, SCREEN_WIDTH, settings.header_height))
        header = QHBoxLayout(header_container)
        header.setContentsMargins(0, 5, 0, 5)

        img=QPixmap(vp.images+'IPS-Logo-Blue-NO-Tagline.jpg')
        self.header_image=QLabel(self)
        self.header_image.setPixmap(img.scaledToHeight(settings.header_height-20))
        self.header_title=QLabel(self,objectName='banner_h1',text='Robotic Welder',minimumWidth=800)
        self.header_clock=QLabel(self,objectName='banner_h1',text='',minimumWidth=300)
        self.header_clock.setStyleSheet('font-size: 40px')
        self.__update_clock()
        self.__clock_timer=NTimer(15000, lambda:self.__update_clock(), repeat=True)

        header.addSpacing(20)
        header.addWidget(self.header_image)
        header.addStretch()
        header.addWidget(self.header_title)
        header.addStretch()
        header.addWidget(self.header_clock)
        header.addSpacing(20)

        #~ hidden buttons
        self.btn_prev_page = QPushButton(self, objectName='btn_invis')
        self.btn_prev_page.setGeometry(QRect(0, 0, 150, settings.header_height))
        self.btn_prev_page.clicked.connect(self._previous_page.emit)

        self.btn_next_page = QPushButton(self, objectName='btn_invis')
        self.btn_next_page.setGeometry(QRect(SCREEN_WIDTH-150, 0, 150, settings.header_height))
        self.btn_next_page.clicked.connect(self._next_page.emit)


    #? Header buttons / events
    def __update_clock(self):
        now=datetime.datetime.now()
        date_str=now.strftime('%m/%d/%y')
        # time_str=now.strftime('%I:%M %p')
        time_str=now.strftime('%I:%M:%S %p')
        self.header_clock.setText(f'{date_str}\n{time_str}')


    #? PyQt Events
    def showEvent(self, a0):
        if not self.__clock_timer.isRunning(): self.__clock_timer.start()
        return super().enterEvent(a0)

    def enterEvent(self, a0):
        return super().enterEvent(a0)

    def hideEvent(self, a0) -> None:
        if self.__clock_timer.isRunning(): self.__clock_timer.kill()
        return super().hideEvent(a0)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    qapp = QApplication(sys.argv)
    with open(vp.assets + 'style.css', 'r') as f:
        qapp.setStyleSheet(f.read())
    gui = QLabel()
    background = QLabel(gui)
    background.setGeometry(QRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    background.setScaledContents(True)
    page = TopHeader(gui)

    if os.name == 'nt':
        page.setGeometry(QRect(0, 0,int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
        gui.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        gui.show()
    else: gui.showFullScreen()
    
    
    page.show()
    input("")