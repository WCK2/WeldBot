from gui.qt.common import *
from gui.pages.blank import BLANK
from gui.pages.home import HOME
from utils.memory import mem


class WELDBOT(NStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_blank:BLANK = self.addWidget(BLANK())
        self.page_home:HOME = self.addWidget(HOME())

        gsig.previous_page.connect(self.__previous_page)
        gsig.next_page.connect(self.__next_page)

        mem.page_count = self.count()
        mem.page = 1
        self.setCurrentIndex(mem.page)

        self.inactivity_timer = NTimer(900_000, self.__inactivity_call, repeat=False)
        gsig.button_activity.connect(self.__reset_inactivity_timer)

    def __reset_inactivity_timer(self):
        self.inactivity_timer.kill()
        self.inactivity_timer.start()

    def __inactivity_call(self):
        self.setCurrentWidget(self.page_blank)

    def __previous_page(self):
        self.setCurrentIndex(self.currentIndex() - 1)
    def __next_page(self):
        self.setCurrentIndex(self.currentIndex() + 1)
    def setCurrentIndex(self, index: int) -> None:
        return super().setCurrentIndex(index)
    def setCurrentWidget(self, w: QWidget) -> None:
        return super().setCurrentWidget(w)
    
    def hideEvent(self, a0: QHideEvent) -> None:
        if self.inactivity_timer.isRunning():
            self.inactivity_timer.kill()
        return super().hideEvent(a0)
    
    def showEvent(self, a0: QShowEvent) -> None:
        if not self.inactivity_timer.isRunning():
            self.inactivity_timer.start()
        return super().showEvent(a0)




if __name__ == "__main__":
    with open('assets/style.css', 'r') as f:
        qapp.setStyleSheet(f.read())
    
    app = WELDBOT()
    if os.name == 'nt':
        app.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        app.show()
    else:
        app.showFullScreen()

    sys.exit(qapp.exec_())

