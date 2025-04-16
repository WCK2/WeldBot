from gui.qt.nframe import *
from gui.qt.nstackedwidget import NStackedWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from gui.workers.ntimer import NTimer
from utils.config import settings, vp
import os


class AUDIO_WRLD(QMediaPlayer):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(AUDIO_WRLD, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
    
    def __init__(self):
        super().__init__(None)
        self.setVolume(settings.volume)

    def playaudio(self, fname:str, force=False):
        if not fname.endswith('.mp3'): fname += '.mp3'
        if force: pass
        elif self.state()==1: return

        self.stop()
        path = vp.audio + fname
        self.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        return self.play()
    
    def click(self):
        print(f'sound.click()')
        self.playaudio("btn_feedback")

    def changevolume(self,val):
        self.setVolume(val)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)    
    qapp = QApplication(sys.argv)
    sound=AUDIO_WRLD()

    sound.playaudio("btn_feedback.mp3", True)
    sound.playaudio("btn_feedback.mp3", True)

    # sound.click()
    # sound.click()
    input("")
    sound.playaudio("btn_feedback.mp3", True)
    input("")
    
    