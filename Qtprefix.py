from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox,\
    QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtGui import QIcon, QFont, QCloseEvent
from PyQt5.QtCore import Qt, QBasicTimer, QThread, pyqtSignal
from sys import argv

class Label(QLabel):
    def  __init__(self,parent:QWidget,pos:tuple,show:bool=True,\
        size:tuple=False,text:str=False,font:QFont=False,style:str=False,align=False):
        super().__init__(parent)
        if text:self.setText(str(text))
        else:self.setText("Label")
        if size:self.resize(size[0],size[1])
        else:self.resize(self.sizeHint())
        if font:self.setFont(font)
        if style:self.setStyleSheet(style)
        self.move(pos[0],pos[1])
        if show:self.show()
        else:self.hide()
        if align:self.setAlignment(align)

class Button(QPushButton):
    def  __init__(self,parent:QWidget,pos:tuple,func=False,arg:tuple=False,\
        size:tuple=False,text:str=False,show:bool=True,font:QFont=False):
        super().__init__(parent)
        if text:self.setText(str(text))
        else:self.setText("")
        if size:self.resize(size[0],size[1])
        else:self.resize(self.sizeHint())
        if func:
            if arg:self.clicked.connect(lambda:func(arg))
            else:self.clicked.connect(func)
        self.move(int(pos[0]),int(pos[1]))
        if font:self.setFont(font)
        if show:self.show()
        else:self.hide()

class LineEdit(QLineEdit):
    def  __init__(self,parent:QWidget,pos:tuple,size:tuple=False,defaultText:str=False,\
        show:bool=True,font=False):
        super().__init__(parent)
        if defaultText:self.setText(str(defaultText))
        if size:self.resize(size[0],size[1])
        else:self.resize(self.sizeHint())
        self.move(pos[0],pos[1])
        if show:self.show()
        else:self.hide()
        if font:self.setFont(font)

class ComboBox(QComboBox):
    def __init__(self, parent:QWidget, pos:tuple, size:tuple, items:list, font:QFont):
        super().__init__(parent)
        self.move(pos[0], pos[1])
        self.resize(size[0], size[1])
        self.addItems(items)
        self.setFont(font)
        self.show()