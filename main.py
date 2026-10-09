import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Dialogue for opening files (and folders)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

########### Task 2. Displaying a list of graphic file names #########
app = QApplication([])
win = QWidget()       
win.resize(1000, 500) 
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Image")
lb_image.setAlignment(Qt.AlignCenter)   # center the picture inside the label
btn_dir = QPushButton("Folder")
lw_files = QListWidget()
 
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")
 
row = QHBoxLayout()          # Main line
col1 = QVBoxLayout()         # divided into two columns
col2 = QVBoxLayout()
col1.addWidget(btn_dir)      # in the first - directory selection button
col1.addWidget(lw_files)     # and file list
col2.addWidget(lb_image, 95) # in the second - image
row_tools = QHBoxLayout()    # and button bar
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
 
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.lower().endswith(ext):   # case-insensitive check (.PNG, .Png, etc now match too)
               result.append(filename)
   return result
 
def chooseWorkdir():
   global workdir
   selected = QFileDialog.getExistingDirectory()
   if selected:            # only overwrite workdir if user didn't press Cancel
       workdir = selected
 
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   if not workdir:         # user cancelled the dialog -> do nothing
       return
   filenames = filter(os.listdir(workdir), extensions)
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)
 
btn_dir.clicked.connect(showFilenamesList)


########### Task 3. Displaying the selected image #########

def showImage():
   filename = lw_files.currentItem()
   if filename is None:        # nothing selected yet
       return
   path = os.path.join(workdir, filename.text())
   pixmap = QPixmap(path)
   # scale the image to fit the label while keeping aspect ratio
   pixmap = pixmap.scaled(
       lb_image.width(), lb_image.height(),
       Qt.KeepAspectRatio, Qt.SmoothTransformation
   )
   lb_image.setPixmap(pixmap)

lw_files.currentRowChanged.connect(showImage)

app.exec()