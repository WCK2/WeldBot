from gui.qt.common import *


class BLANK(NFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('page_blank')
        
        self.btn_blank = QPushButton(self, objectName='btn_blank', text='')
        self.btn_blank.setGeometry(QRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.btn_blank.clicked.connect(self.__on_btnblank)

    def __on_btnblank(self):
        gsig.next_page.emit()

    #? PyQt Events
    def showEvent(self, a0):
        return super().enterEvent(a0)

    def enterEvent(self, a0):
        return super().enterEvent(a0)

    def hideEvent(self, a0) -> None: 
        return super().hideEvent(a0)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    with open('assets/style.css', 'r') as f:
        app.setStyleSheet(f.read())

    gui = QLabel()
    page = BLANK(gui)
    if os.name == 'nt':
        page.setGeometry(QRect(0, 0,int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
        gui.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        gui.show()
    else: gui.showFullScreen()
    
    page.show()
    sys.exit(app.exec_())

