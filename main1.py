import os
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


from PIL import Image
from PIL.ImageFilter import SHARPEN


app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Image")
btn_dir = QPushButton("Folder")
lw_files = QListWidget()


btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpen")
btn_bw = QPushButton("B/W")


row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)


row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)


win.show()


workdir = ''




def filter_by_extension(files, extensions):
    """Keep only files that end with one of the given extensions."""
    result = []
    for filename in files:
        for ext in extensions:
            if filename.lower().endswith(ext):
                result.append(filename)
    return result




def chooseWorkdir():
    global workdir
    chosen = QFileDialog.getExistingDirectory()
    # Only overwrite workdir if the user actually picked something
    # (Cancel returns an empty string, which used to crash os.listdir below)
    if chosen:
        workdir = chosen
    return bool(chosen)




def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if not chooseWorkdir():
        return  # user cancelled the folder dialog, nothing to list


    filenames = filter_by_extension(os.listdir(workdir), extensions)


    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)




btn_dir.clicked.connect(showFilenamesList)




class ImageProcessor:
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Modified"


    def loadImage(self, filename):
        """Remember the file name/path and open the image."""
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)


    def saveImage(self):
        """Save a copy of the edited image into a subfolder."""
        path = os.path.join(workdir, self.save_dir)
        if not os.path.isdir(path):
            os.makedirs(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)


    def _apply(self, fn):
        """Run an edit on the currently loaded image, save it, and refresh the preview."""
        if self.image is None:
            return
        fn()
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_bw(self):
        self._apply(lambda: setattr(self, 'image', self.image.convert("L")))


    def do_left(self):
        self._apply(lambda: setattr(self, 'image', self.image.transpose(Image.ROTATE_90)))


    def do_right(self):
        self._apply(lambda: setattr(self, 'image', self.image.transpose(Image.ROTATE_270)))


    def do_flip(self):
        self._apply(lambda: setattr(self, 'image', self.image.transpose(Image.FLIP_LEFT_RIGHT)))


    def do_sharpen(self):
        self._apply(lambda: setattr(self, 'image', self.image.filter(SHARPEN)))


    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()




def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))




workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)


btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)


app.exec()

