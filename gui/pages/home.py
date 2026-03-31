from random import randint
from gui.qt.common import *
from PIL import Image, ImageQt
from utils.config import settings
from gui.workers.tpost import post_req_async
from gui.workers.ntimer import NTimer


def ls(dir: str, filetype: str):
    files=[]
    existing_saves=os.listdir(dir)
    for fname in existing_saves:
        if fname.endswith(filetype): files.append(fname)
    return files

def get_program_image_file(directory: str, name: str, suffix=['.png', '.jpg']):
    targets = [directory + name + ss for ss in suffix]
    for t in targets:
        if os.path.exists(t):
            return t
    
    directory += 'random/'
    options = ls(directory,'.png') + ls(directory,'.jpg')
    return directory+options[randint(0,len(options)-1)]


class HOME(NFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('page_home')
        self.controls_width = 1000
        self.test_bool = False
        
        #~ initializations
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        controls_container = QFrame(self,objectName='container')
        controls_container.setGeometry(QRect(0,settings.header_height,self.controls_width,SCREEN_HEIGHT-settings.header_height))
        controls_layout = QVBoxLayout(controls_container)
        controls_layout.setContentsMargins(0,0,0,0)

        #~ upper half (controls/program #)
        self.program_image = QLabel(self,objectName='image')
        self.program_image.setFixedSize(450,350)
        self.program_image.setScaledContents(True)

        self.program_label = QLabel(self, objectName='program_label', text=f'<div style="line-height: 150%;"><span style="color: #16C60C;">Program #:</span> {mem.program}<br><span style="color: #16C60C;">Name:</span> {mem.program_name}</div>', minimumWidth=450, maximumWidth=450, minimumHeight=175, maximumHeight=175)
        self.program_label.setWordWrap(True)

        self.btn_program_sub = QPushButton(self,text="-", minimumWidth=150, maximumWidth=150, minimumHeight=75, maximumHeight=75)
        self.btn_program_sub.clicked.connect(lambda: self.__inc_program(False))
        self.btn_program_add = QPushButton(self,text="+", minimumWidth=150, maximumWidth=150, minimumHeight=75, maximumHeight=75)
        self.btn_program_add.clicked.connect(lambda: self.__inc_program(True))

        plus_minus_layout = QHBoxLayout()
        plus_minus_layout.setContentsMargins(0,0,0,0)
        plus_minus_layout.addStretch(2)
        plus_minus_layout.addWidget(self.btn_program_sub,alignment=Qt.AlignCenter)
        plus_minus_layout.addStretch(1)
        plus_minus_layout.addWidget(self.btn_program_add,alignment=Qt.AlignCenter)
        plus_minus_layout.addStretch(2)

        vbox_program = QVBoxLayout()
        vbox_program.setContentsMargins(0,0,0,0)
        vbox_program.addStretch(2)
        vbox_program.addWidget(self.program_label, alignment=Qt.AlignCenter)
        vbox_program.addStretch(1)
        vbox_program.addLayout(plus_minus_layout)
        vbox_program.addStretch(2)

        hbox_upper = QHBoxLayout()
        hbox_upper.setContentsMargins(0,0,0,0)
        hbox_upper.addStretch(2)
        hbox_upper.addWidget(self.program_image,alignment=Qt.AlignCenter)
        hbox_upper.addStretch(1)
        hbox_upper.addLayout(vbox_program)
        hbox_upper.addStretch(2)

        #~ grid1 (contols/start stop)
        self.btn_start = QPushButton(objectName='btn_start', text="START", minimumWidth=400, minimumHeight=100)
        self.btn_start.clicked.connect(self.__onbtn_start)
        
        self.btn_stop = QPushButton(objectName='btn_stop', text="STOP", minimumWidth=400, minimumHeight=100)
        self.btn_stop.setCheckable(True)
        self.btn_stop.setChecked(False)
        self.btn_stop.clicked.connect(self.__onbtn_stop)

        self.start_popup = QLabel(self, objectName='start_popup', text='** Remember to enable FGAP on the Senfeng Laser Welder **')

        grid1 = QGridLayout()
        grid1.setContentsMargins(0,0,0,0)
        grid1.addWidget(self.btn_start, 0,0, alignment=Qt.AlignCenter)
        grid1.addWidget(self.btn_stop, 0,1, alignment=Qt.AlignCenter)
        grid1.addWidget(self.start_popup, 1,0,1,2, alignment=Qt.AlignCenter)
        grid1.setColumnStretch(0,1)
        grid1.setColumnStretch(1,1)
        grid1.setRowStretch(0,1)
        grid1.setRowStretch(1,1)

        #~ grid2 (controls/io)
        self.btn_laser = QPushButton(objectName='plc_io',text='Laser Welder')
        self.btn_laser.clicked.connect(self.__on_laser)
        self.btn_test_y = QPushButton(objectName='plc_io',text='-')
        self.btn_test_y.clicked.connect(self.__on_test_y)
        self.btn_shutdown = QPushButton(objectName='plc_io', text='Shutdown')
        self.btn_shutdown.clicked.connect(self.__on_confirm_shutdown)

        grid2 = QGridLayout()
        grid2.setContentsMargins(0,0,0,0)
        grid2.setVerticalSpacing(40)
        grid2.setHorizontalSpacing(25)
        grid2.addWidget(self.btn_laser, 0, 0, alignment=Qt.AlignCenter)
        grid2.addWidget(QPushButton(objectName='plc_io', text='-'), 0, 1)
        grid2.addWidget(QPushButton(objectName='plc_io', text='-'), 0, 2)
        grid2.addWidget(QPushButton(objectName='plc_io', text='-'), 1, 0)
        grid2.addWidget(self.btn_test_y, 1, 1, alignment=Qt.AlignCenter)
        grid2.addWidget(self.btn_shutdown, 1, 2, alignment=Qt.AlignCenter)

        #~ ...add layouts (controls)
        controls_layout.addSpacing(15)
        controls_layout.addWidget(QLabel(self,objectName='h1',text='System Controls'), alignment=Qt.AlignCenter)
        controls_layout.addSpacing(15)
        controls_layout.addLayout(hbox_upper)
        controls_layout.addSpacing(30)
        controls_layout.addLayout(grid1)
        controls_layout.addSpacing(30)
        controls_layout.addLayout(grid2)
        controls_layout.addStretch()

        #~ -- status layout --
        status_container = QFrame(self,objectName='container')
        status_container.setGeometry(QRect(self.controls_width, settings.header_height, SCREEN_WIDTH-self.controls_width, SCREEN_HEIGHT-settings.header_height))
        status_layout=QVBoxLayout(status_container)
        status_layout.setContentsMargins(0,0,0,0)

        #~ log
        self.text_edit = QPlainTextEdit(objectName='log')
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_edit.setFixedSize(SCREEN_WIDTH-self.controls_width-50, 500)
        
        status_layout.addSpacing(15)
        status_layout.addWidget(QLabel(self,objectName='h1',text='Robot Log'), alignment=Qt.AlignCenter)
        status_layout.addSpacing(15)
        status_layout.addWidget(self.text_edit, alignment=Qt.AlignCenter)
        status_layout.addStretch()

        #~ -- page layout --
        control_and_status_layouts=QHBoxLayout()
        control_and_status_layouts.setContentsMargins(0,0,0,0)
        control_and_status_layouts.addLayout(controls_layout)
        control_and_status_layouts.addLayout(status_layout)
        
        self.top_header = TopHeader(self)
        page_layout.addWidget(self.top_header)
        page_layout.addLayout(control_and_status_layouts)
        page_layout.addStretch()

        #~ threads & signals
        mem.log_message.connect(self.__append_log)
        mem.new_status.connect(self.__on_new_status)
        # self.program_number.value_change_signal.connect(self.__update_program_image)

    #? button stuff
    def __inc_program(self, b: bool):
        n = 1 if b else -1
        i = mem.program + n
        if i < 0: return
        mem.program = i
        self.program_label.setText(f'<div style="line-height: 150%;"><span style="color: #16C60C;">Program #:</span> {mem.program}<br><span style="color: #16C60C;">Name:</span> {mem.program_name}</div>')
        post_req_async(path='mem', data={'name': 'program', 'value': str(mem.program)})

        self.__update_program_image()

    def __onbtn_start(self):
        if self.btn_stop.isChecked():
            print(f'> will not set start because btn_stop is checked')
            return
        post_req_async(path='mem', data={'name': 'start', 'value': True})

    def __onbtn_stop(self):
        state = self.btn_stop.isChecked()
        plc.write_coil_async(addr.stop, state, callback=print)
        # plc.read_coil_async(addr.stop, callback=print)

    def __update_program_image(self):
        img = QPixmap(get_program_image_file(vp.images + 'program/', str(mem.program)))
        self.program_image.setPixmap(img)

    def __on_laser(self):
        return

    def __on_test_y(self):
        self.test_bool = not self.test_bool
        plc.write_coil_async(addr.test_y, self.test_bool)

    #? log
    def __append_log(self, s:str=None):
        current_time = QDateTime.currentDateTime().toString('MM-dd hh:mm:ss')
        if s:
            msg = s
            self.text_edit.appendHtml(f'<html><font color="#16C60C">{current_time}:</font> **{msg}**</html>')
        else:
            msg = mem.log
            self.text_edit.appendHtml(f'<html><font color="#16C60C">{current_time}:</font> {msg}</html>')

        scrollbar_current = self.text_edit.verticalScrollBar().value()
        scrollbar_max = self.text_edit.verticalScrollBar().maximum()
        if scrollbar_current == scrollbar_max:
            self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

    def __on_new_status(self):
        status = mem.status
        if status == 'booting':
            post_req_async(path='mem', data={'name': 'program', 'value': str(mem.program)})

    #? shutdown
    def __on_confirm_shutdown(self):
        message_box = QMessageBox(self)
        message_box.setObjectName('confirmShutdownBox')
        message_box.setWindowTitle('Confirm Shutdown')
        message_box.setText('Are you sure you want to shutdown the system?')
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.No)

        reply = message_box.exec_()

        if reply == QMessageBox.Yes:
            self.__shutdown_system()

    def __shutdown_system(self):
        print(f'__shutdown_system')
        QApplication.quit()

        if os.name != 'nt':
            os.system("echo exiting QApplication!")
            # os.system("sleep 10 && sudo shutdown -h now")

    #? PyQt Events
    def showEvent(self, a0):
        self.__append_log('Screen running')
        post_req_async(path='mem', data={'name': 'program', 'value': str(mem.program)})
        self.__update_program_image()
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
    page = HOME(gui)
    if os.name == 'nt':
        page.setGeometry(QRect(0, 0,int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
        gui.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        gui.show()
    else: gui.showFullScreen()
    
    page.show()
    sys.exit(app.exec_())

