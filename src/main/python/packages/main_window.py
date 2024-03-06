from PySide6 import QtWidgets, QtCore, QtGui
from . image import ImageConverter

class Worker(QtCore.QObject):
    def __init__(self, images_to_convert, quality, size, folder):
        super().__init__()
        self.images_to_convert = images_to_convert
        self.quality = quality
        self.size = size
        self.folder = folder

    def convert_images(self):
        for image_lw_item in self.images_to_convert:
            if not image_lw_item.processed:
                image = ImageConverter(path=image_lw_item.text(), folder=self.folder)
                image.resize_image(size=self.size, quality=self.quality)



class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx=ctx
        self.setWindowTitle('PyConverter')
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layout()
        self.add_widgets_to_layouts()
        self.setup_events()

    def create_widgets(self):
        self.lbl_quality = QtWidgets.QLabel('Quality:')
        self.spn_quality = QtWidgets.QSpinBox()
        self.lbl_size = QtWidgets.QLabel('Size:')
        self.spn_size = QtWidgets.QSpinBox()
        self.lbl_output_folder = QtWidgets.QLabel('Output folder:')
        self.le_output_folder = QtWidgets.QLineEdit()
        self.lw_files = QtWidgets.QListWidget()
        self.btn_convert = QtWidgets.QPushButton('Convert')
        self.lbl_drop_info = QtWidgets.QLabel('^ Drop the images')


    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, 'r') as f:
            self.setStyleSheet(f.read())

        # Alignement
        self.spn_quality.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.spn_size.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.le_output_folder.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # Range
        self.spn_quality.setRange(1, 100)
        self.spn_quality.setValue(75)
        self.spn_size.setRange(1, 100)
        self.spn_size.setValue(50)

        # Other
        self.le_output_folder.setPlaceholderText("Output folder")
        self.le_output_folder.setText("Optimized")
        self.lbl_drop_info.setVisible(False)
        self.setAcceptDrops(True)


    def create_layout(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lbl_quality, 0, 0)
        self.main_layout.addWidget(self.spn_quality, 0, 1)
        self.main_layout.addWidget(self.lbl_size, 1, 0)
        self.main_layout.addWidget(self.spn_size, 1, 1)
        self.main_layout.addWidget(self.lbl_output_folder, 2, 0)
        self.main_layout.addWidget(self.le_output_folder, 2, 1)
        self.main_layout.addWidget(self.lw_files, 3, 0, 1, 2)
        self.main_layout.addWidget(self.btn_convert, 4, 0, 1, 2)
        self.main_layout.addWidget(self.lbl_drop_info, 5, 0, 1, 2)

    def setup_events(self):
        QtGui.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_files, self.delete_selected_items)
        self.btn_convert.clicked.connect(self.convert_images)

    def delete_selected_items(self):
        for item in self.lw_files.selectedItems():
            row = self.lw_files.row(item)
            self.lw_files.takeItem(row)


    def convert_images(self):
        quality = self.spn_quality.value()
        size = self.spn_size.value()/100.0
        folder = self.le_output_folder.text()

        lw_items = [self.lw_files.item(index) for index in range(self.lw_files.count())]
        images_to_convert = [1 for lw_item in lw_items if not lw_item.processed]
        if not images_to_convert:
            msg_box = QtWidgets.QMessageBox(QtGui.QIcon.Warning, 'No image to be converted')
            msg_box.exec()
            return False
        self.thread = QtCore.QThread(self)
        self.worker = Worker(images_to_convert=lw_items, quality=quality, size=size, folder=folder)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.convert_images)
        self.thread.start()

    def dragEnterEvent(self, event):
        self.lbl_drop_info.setVisible(True)
        event.accept()

    def dragLeaveEvent(self, event):
        self.lbl_drop_info.setVisible(False)


    def dropEvent(self, event):
        event.accept()
        for url in event.mimeData().urls():
            self.add_file(path = url.toLocalFile())
        self.lbl_drop_info.setVisible(False)

    def add_file(self, path):
        items = [self.lw_files.item(index).text() for index in range(self.lw_files.count())]
        if path not in items:
            lw_item = QtWidgets.QListWidgetItem(path)
            lw_item.setIcon(self.ctx.image_unchecked)
            lw_item.processed = False
            self.lw_files.addItem(lw_item)



