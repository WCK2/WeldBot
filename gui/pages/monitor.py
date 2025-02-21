from gui.qt.common import *
from PIL import Image, ImageQt
from utils.config import settings
from gui.workers.tpost import post_req_async
import random
import string
from functools import partial


def random_string(min_length=5, max_length=25):
    length = random.randint(min_length, max_length)
    characters = string.ascii_letters + string.digits  # Include letters and digits
    return ''.join(random.choices(characters, k=length))


class MONITOR(NFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('page_monitor')
        
        #~ initializations
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        container = QFrame(self, objectName='container')
        container.setGeometry(QRect(0, settings.header_height, SCREEN_WIDTH, SCREEN_HEIGHT-settings.header_height))
        layout = QGridLayout(container)
        layout.setVerticalSpacing(50)
        layout.setHorizontalSpacing(10)

        #~ -- right panel --
        self.label_part_request = QLabel(self, objectName='h1', text='Part Requests')

        self.label_part_name = QLabel(self, objectName='label', text='Part Name: ')
        self.label_part_id = QLabel(self, objectName='label', text='Part ID: ')

        self.btn_part_request_running = QPushButton(self, objectName='btn_flag', text='Flag part request running')
        self.btn_part_request_running.setCheckable(True)
        self.btn_part_request_running.setChecked(mem.flag_part_request_running)
        self.btn_part_request_running.clicked.connect(
            partial(self.__toggle_flag, self.btn_part_request_running, 'flag_part_request_running')
        )
        self.btn_place_part = QPushButton(self, objectName='btn_flag', text='Flag place part')
        self.btn_place_part.setCheckable(True)
        self.btn_place_part.setChecked(mem.flag_place_part)
        self.btn_place_part.clicked.connect(
            partial(self.__toggle_flag, self.btn_place_part, 'flag_place_part')
        )
        self.btn_in_place = QPushButton(self, objectName='btn_flag', text='Flag in place')
        self.btn_in_place.setCheckable(True)
        self.btn_in_place.setChecked(mem.flag_in_place)
        self.btn_in_place.clicked.connect(
            partial(self.__toggle_flag, self.btn_in_place, 'flag_in_place')
        )
        self.btn_return_to_pickup = QPushButton(self, objectName='btn_flag', text='Flag return to pickup')
        self.btn_return_to_pickup.setCheckable(True)
        self.btn_return_to_pickup.setChecked(mem.flag_return_to_pickup)
        self.btn_return_to_pickup.clicked.connect(
            partial(self.__toggle_flag, self.btn_return_to_pickup, 'flag_return_to_pickup')
        )

        #~ layout
        layout.addWidget(self.label_part_request, 0, 0, 1, 4, alignment=Qt.AlignCenter) # Row 0, Column 0, Span 1 row and 4 columns
        
        layout.addWidget(self.label_part_name, 1, 0, 1, 2)
        layout.addWidget(self.label_part_id, 1, 2, 1, 2)

        layout.addWidget(self.btn_part_request_running, 2, 0)
        layout.addWidget(self.btn_place_part, 2, 1)
        layout.addWidget(self.btn_in_place, 2, 2)
        layout.addWidget(self.btn_return_to_pickup, 2, 3)

        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding), 3, 0, 1, 4)

        #~ add layouts
        self.top_header = TopHeader(self)
        page_layout.addWidget(self.top_header)
        page_layout.addLayout(layout)
        page_layout.addStretch()

        #~ threads & signals
        mem.new_part_request.connect(self.__update_part_request)
        mem.flag_change.connect(self.__flag_change)


    #? part request stuff
    def __update_part_request(self):
        part_name = mem.part_request.get('part_name')
        part_id = mem.part_request.get('part_id')
        
        self.label_part_name.setText(f'Part Name: {part_name}')
        self.label_part_id.setText(f'Part ID: {part_id}')

    def __toggle_flag(self, btn, flag_name):
        new_state = btn.isChecked()
        setattr(mem, flag_name, new_state)

    def __flag_change(self, flag_name):
        try:
            state = getattr(mem, flag_name)
            
            if flag_name == 'flag_part_request_running':
                self.btn_part_request_running.setChecked(state)
            elif flag_name == 'flag_place_part':
                self.btn_place_part.setChecked(state)
            elif flag_name == 'flag_in_place':
                self.btn_in_place.setChecked(state)
            elif flag_name == 'flag_return_to_pickup':
                self.btn_return_to_pickup.setChecked(state)
        except AttributeError:
            print(f"Error: The attribute '{flag_name}' does not exist in the 'mem' object.")

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
    page = MONITOR(gui)
    if os.name == 'nt':
        page.setGeometry(QRect(0, 0,int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
        gui.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        gui.show()
    else: gui.showFullScreen()
    
    page.show()
    sys.exit(app.exec_())

