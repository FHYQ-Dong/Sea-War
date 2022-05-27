from Qtprefix import *
from Connprefix import *
from random import seed, randint
from time import time
from os import _exit

def selectClient():
    
    class Window1(QWidget):
        def __init__(self):
            super().__init__()
            self.ipmode = ""
            self.closeAll = True
            self.initUI()

        def initUI(self):
            self.setGeometry(300, 300, 350, 170)
            self.setWindowTitle("选择IP模式")
            self.setWindowIcon(QIcon("icon.ico"))

            self.title = Label(self, (100, 20), True, (150, 50), "选择IP模式", QFont("宋体", 14), False, Qt.AlignCenter)
            self.ipv4Button = Button(self, (60, 90), self.selectIPModeFunc, ("ipv4",), (100, 40), "IPv4", True, QFont("宋体", 14))
            self.ipv6Button = Button(self, (190, 90), self.selectIPModeFunc, ("ipv6",), (100, 40), "IPv6", True, QFont("宋体", 14))
            self.show()

        def selectIPModeFunc(self, mode) -> None:
            self.ipmode = mode[0]
            self.closeAll = False
            selectClientModeWindow.show()
            self.close()
            self.closeAll = True

        def closeEvent(self, e:QCloseEvent) -> None:
            if self.closeAll:
                _exit(0)
            else:
                e.accept()

    class Window2(QWidget):
        def __init__(self):
            super().__init__()
            self.ClientMode = ""
            self.closeAll = True
            self.initUI()

        def initUI(self):
            self.setGeometry(300, 300, 350, 170)
            self.setWindowTitle("选择类型")
            self.setWindowIcon(QIcon("icon.ico"))

            self.title = Label(self, (100, 20), True, (150, 50), "选择类型", QFont("宋体", 14), False, Qt.AlignCenter)
            self.ipv4Button = Button(self, (60, 90), self.selectClientModeFunc, ("client",), (100, 40), "客户端", True, QFont("宋体", 14))
            self.ipv6Button = Button(self, (190, 90), self.selectClientModeFunc, ("server",), (100, 40), "服务端", True, QFont("宋体", 14))

        def selectClientModeFunc(self, mode) -> None:
            self.ClientMode = mode[0]
            self.closeAll = False
            self.close()
            self.closeAll = True

        def closeEvent(self, e:QCloseEvent):
            if self.closeAll:
                _exit(0)
            else:
                e.accept()

    App = QApplication(argv)
    selectIPWindow = Window1()
    selectClientModeWindow = Window2()
    App.exec_()
    return selectIPWindow.ipmode, selectClientModeWindow.ClientMode

def Server(ipMode:str):
    
    class Waiting(QWidget):
        def __init__(self):
            super().__init__()
            self.myturn = False
            self.sock = None
            self.rootsock = None
            self.receiver = None
            self.host = None
            self.closeAll = True
            self.initUI()

        def waiting(self, ipMode, host, reconnect:bool=False) -> None:
            self.ipMode = ipMode
            self.host = host
            self.timer.start(1000, self)
            self.ownHostReminder.setText(f"本地IP：{self.host[0]} 端口：{self.host[1]}")
            self.ownHostReminder.show()
            if not reconnect:
                if ipMode == "ipv4":
                    self.rootsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                elif ipMode == "ipv6":
                    self.rootsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                try:
                    self.rootsock.bind(self.host)
                    self.rootsock.listen(1)
                    self.Thread = myThread(self, self.rootsock)
                    self.Thread.emitSignal.connect(self.timer.stop)
                except OSError:
                    self.host = host
                    self.timer.stop()
                    self.ownHostReminder.setText("")
                    self.ownHostReminder.hide()
                    ServerWindow.show()
                    self.closeAll = False
                    self.close()
                    self.closeAll = True
                    QMessageBox.warning(ServerWindow, "错误", "端口被占用", QMessageBox.Ok)
                    return
                self.Thread.start()
            else:
                self.Thread = myThread(self, self.rootsock)
                self.Thread.emitSignal.connect(self.timer.stop)
                self.Thread.start()

        def initUI(self):
            self.setGeometry(300, 300, 650, 230)
            self.setWindowTitle("连接中")
            self.setWindowIcon(QIcon("icon.ico"))
            
            self.ownHostReminder = Label(self, (25, 30), False, (600, 30), "", QFont("宋体", 10), False, Qt.AlignCenter)
            self.waitingTitle = Label(self, (160, 90), True, (330, 80), "等待连接", QFont("宋体", 30), False, Qt.AlignCenter)
            self.waitingTitleDotCount = 0
            self.timer = QBasicTimer()

            self.receiverIPReminder = Label(self, (30, 70), False, (120, 40), "对方IP:", QFont("宋体",10), False, Qt.AlignCenter)
            self.receiverIPaddress = Label(self, (150, 70), False, (450, 35), "", QFont("宋体", 10), False, Qt.AlignCenter)
            self.receiverPortReminder = Label(self, (30, 110), False, (120, 40), "对方端口:", QFont("宋体",10), False, Qt.AlignCenter)
            self.receiverPort = Label(self, (150, 110), False, (450, 35), "", QFont("宋体", 10), False, Qt.AlignCenter)

            self.rejectButton = Button(self, (200, 160), self.rejectConnection, False, (80, 40), "拒 绝", False, QFont("宋体", 10))
            self.acceptButton = Button(self, (370, 160), self.acceptConnection, False, (80, 40), "连 接", False, QFont("宋体", 10))

        def rejectConnection(self):
            self.sock.sendall("reject".encode("utf-8"))
            self.sock.close()
            self.waitingTitle.show()
            self.receiverIPReminder.hide()
            self.receiverIPaddress.hide()
            self.ownHostReminder.hide()
            self.receiverPortReminder.hide()
            self.receiverPort.hide()
            self.rejectButton.hide()
            self.acceptButton.hide()
            self.waiting(self.ipMode, self.host, True)

        def acceptConnection(self):
            self.myturn = bool(randint(0,1))
            self.sock.sendall(f"accept{1-int(self.myturn)}".encode("utf-8"))
            self.closeAll = False
            self.close()
            self.closeAll = True

        def timerEvent(self, e) -> None:
            self.waitingTitleDotCount = (self.waitingTitleDotCount + 1) % 4
            self.waitingTitle.setText("等待连接"+"."*self.waitingTitleDotCount)

        def closeEvent(self,e:QCloseEvent):
            if self.closeAll:
                _exit(0)
            else:
                e.accept()

    class myThread(QThread):

        emitSignal = pyqtSignal()

        def __init__(self, surface:Waiting, sock:socket.socket):
            super().__init__()
            self.surface = surface
            self.sock = sock

        def run(self) -> None:
            self.surface.sock, self.surface.receiver = self.sock.accept()
            self.emitSignal.emit()
            self.surface.waitingTitle.hide()
            self.surface.receiverIPaddress.setText(str(self.surface.receiver[0]))
            self.surface.receiverPort.setText(str(self.surface.receiver[1]))
            self.surface.receiverIPReminder.show()
            self.surface.receiverPortReminder.show()
            self.surface.receiverIPaddress.show()
            self.surface.receiverPort.show()
            self.surface.acceptButton.show()
            self.surface.rejectButton.show()
            return

    class Server(QWidget):
        def __init__(self, ipMode):
            super().__init__()
            self.closeAll = True
            self.ipMode = ipMode
            self.ipaddrlist = []
            self.host = ()
            self.pwd = ""
            self.getipaddr()
            self.initUI()

        def getipaddr(self):
            if self.ipMode == "ipv4":
                tmp = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET)
            elif self.ipMode == "ipv6":
                tmp = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)
            for i in tmp:
                self.ipaddrlist.append(i[4][0])

        def initUI(self):
            self.setGeometry(300, 300, 650, 270)
            self.setWindowTitle("服务端设置")
            self.setWindowIcon(QIcon("icon.ico"))

            self.title = Label(self, (250, 20), True, (150, 40), "服务端设置", QFont("宋体", 14), False, Qt.AlignCenter)
            self.selectIPReminder = Label(self, (30, 70), True, (120, 40), "选择IP地址:", QFont("宋体",10), False, Qt.AlignCenter)
            self.selectIPBox = ComboBox(self, (150, 70), (450, 35), self.ipaddrlist, QFont("宋体", 10))
            self.enterPortReminder = Label(self, (30, 110), True, (120, 40), "选择端口:", QFont("宋体",10), False, Qt.AlignCenter)
            self.enterPortEdit = LineEdit(self, (150, 110), (450, 35), "1024 ~ 49151", True, QFont("宋体", 10))
            self.setPINReminder = Label(self, (30, 150), True, (120, 40), "设置密码:", QFont("宋体", 10), False, Qt.AlignCenter)
            self.enterPINEdit = LineEdit(self, (150, 150), (450, 35), False, True, QFont("宋体", 10))
            self.enterPINEdit.setEchoMode(QLineEdit.Password)
            self.confirmButton = Button(self, (265, 205), self.confirmButtonfunc, False, (120, 40), "确  定", True, QFont("宋体", 14))
            self.show()

        def confirmButtonfunc(self):
            self.pwd = self.enterPINEdit.text()
            if self.pwd == "":
                QMessageBox.warning(self, "错误", "密码不能为空", QMessageBox.Ok)
                return
            try:
                self.host = (self.selectIPBox.currentText(), int(self.enterPortEdit.text()))
                if not (int(self.enterPortEdit.text()) >= 1024 and int(self.enterPortEdit.text()) <= 49151):
                    raise(ValueError)
            except:
                QMessageBox.warning(self, "错误", "输入格式或数值错误", QMessageBox.Ok)
                return
            self.closeAll = False
            self.close()
            self.closeAll = True
            OnWaitingWindow.show()
            OnWaitingWindow.waiting(self.ipMode, self.host)
            
        def closeEvent(self, e:QCloseEvent):
            if self.closeAll:
                _exit(0)
            else:
                e.accept()

    App = QApplication(argv)
    ServerWindow = Server(ipMode)
    OnWaitingWindow = Waiting()
    App.exec_()
    return myClient(OnWaitingWindow.sock, ServerWindow.pwd), bool(OnWaitingWindow.myturn)

def Client(ipMode:str):
       
    class Client(QWidget):
        def __init__(self, ipMode):
            super().__init__()
            self.closeAll = True
            self.ipMode = ipMode
            self.sock = None
            self.Serverhost = None
            self.recvmsg = ""
            self.myturn = False
            self.pwd = ""
            self.initUI()

        def getsock(self):
            if self.ipMode == "ipv4":
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.ipMode == "ipv6":
                self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        
        def initUI(self):
            self.setGeometry(300, 300, 650, 270)
            self.setWindowTitle("客户端连接")
            self.setWindowIcon(QIcon("icon.ico"))

            self.title = Label(self, (250, 20), True, (150, 40), "客户端设置", QFont("宋体", 14), False, Qt.AlignCenter)
            self.ServerIPReminder = Label(self, (30, 70), True, (120, 40), "服务端IP地址:", QFont("宋体",10), False, Qt.AlignCenter)
            self.ServerIPEdit = LineEdit(self, (150, 70), (450, 35), self.ipMode, True, QFont("宋体", 10))
            self.ServerPortReminder = Label(self, (30, 110), True, (120, 40), "服务端端口:", QFont("宋体",10), False, Qt.AlignCenter)
            self.ServerPortEdit = LineEdit(self, (150, 110), (450, 35), "1024 ~ 49151", True, QFont("宋体", 10))
            self.ServerPINReminder = Label(self, (30, 150), True, (120, 40), "服务端密码:", QFont("宋体", 10), False, Qt.AlignCenter)
            self.ServerPINEdit = LineEdit(self, (150, 150), (450, 35), False, True, QFont("宋体", 10))
            self.ServerPINEdit.setEchoMode(QLineEdit.Password)
            self.confirmButton = Button(self, (265, 205), self.confirmButtonfunc, False, (120, 40), "确  定", True, QFont("宋体", 14))
            self.connectingReminder = Label(self, (265, 205), False, (120, 40), "连接中...", QFont("宋体", 10), False, Qt.AlignCenter)
            self.show()

        def closeEvent(self, e:QCloseEvent) -> None:
            if self.closeAll:
                _exit(0)
            else:
                e.accept()

        def showWarning(self, e):
            QMessageBox.warning(self, "错误", str(e), QMessageBox.Ok)

        def confirmButtonfunc(self):
            self.pwd = self.ServerPINEdit.text()
            if self.pwd == "":
                QMessageBox.warning(self, "错误", "密码不能为空", QMessageBox.Ok)
                return
            self.getsock()
            self.Serverhost = (self.ServerIPEdit.text(), int(self.ServerPortEdit.text()))
            self.confirmButton.hide()
            self.connectingReminder.show()
            self.Thread = myThread(self)
            self.Thread.emitSignal.connect(self.showWarning)
            self.Thread.start()
            
    class myThread(QThread):

        emitSignal = pyqtSignal(str)

        def __init__(self, surface:Client):
            super().__init__()
            self.surface = surface

        def run(self):
            try:
                self.surface.sock.connect(self.surface.Serverhost)
            except socket.gaierror:
                self.emitSignal.emit("IP地址格式错误")
                self.surface.connectingReminder.hide()
                self.surface.confirmButton.show()
                return
            except OSError as e:
                if e.args[0] == 10061:
                    self.emitSignal.emit("无法连接到目标主机")
                else:
                    self.emitSignal.emit("未知错误")
                self.surface.connectingReminder.hide()
                self.surface.confirmButton.show()
                return
            except Exception as e:
                self.emitSignal.emit("未知错误")
                self.surface.connectingReminder.hide()
                self.surface.confirmButton.show()
                return
            self.surface.recvmsg = self.surface.sock.recv(1024).decode("utf-8")
            if self.surface.recvmsg[:6] == "reject":
                self.emitSignal.emit("目标主机拒绝连接")
                self.surface.connectingReminder.hide()
                self.surface.confirmButton.show()
                return
            elif self.surface.recvmsg[:6] == "accept":
                self.surface.myturn = bool(int(self.surface.recvmsg[6:]))
                self.surface.closeAll = False
                self.surface.close()
                self.surface.closeAll = True 
                return
        
    App = QApplication(argv)
    ClientWindow = Client(ipMode)
    App.exec()
    return myClient(ClientWindow.sock, ClientWindow.pwd), ClientWindow.myturn

def setSea(Client:myClient):

    class Window(QWidget):
        def __init__(self, Client:myClient):
            super().__init__()
            self.sea = [[False for j in range(10)] for i in range(10)]
            self.shipcount = 20
            self.SHIP = "$ship$"
            self.BLANK = "$blank$"
            self.Ships = []

            self.closeAll = True

            self.Client = Client
            self.recvThread = recvThread(self.Client)
            self.recvThread.ErrorSignal.connect(self.threadError)
            self.recvThread.msgSignal.connect(self.closeWindow)

            self.initUI()
            QMessageBox.information(self, "提示", "程序设计者未设计较完善的检查船只放置合法性的功能\n请自觉遵守游戏规则", QMessageBox.Ok)
        
        def threadError(self, e:tuple):
            if e[0] == self.Client.OK:
                return
            else:
                QMessageBox.warning(self, "错误", e[0]+"\n"+str(e[1]), QMessageBox.Ok)

        def closeWindow(self, b):
            if b:
                self.closeAll = False
                self.close()
                self.closeAll = False

        def initUI(self):
            self.setGeometry(300, 300, 500, 550)
            self.setWindowTitle("放置船只")
            self.setWindowIcon(QIcon("icon.ico"))
            self.blockButtons = [[Button(self, (50+i*40, 70+j*40), self.selectShipFunc, (i, j), (40, 40), False, True, False) for j in range(10)] for i in range(10)]

            self.title = Label(self, (200, 20), True, (100, 40), "放置船只", QFont("宋体", 12), False, Qt.AlignCenter)
            self.confirmbutton = Button(self, (210, 490), self.confirmButtonFunc, False, (80, 40), "确 定", True, QFont("宋体", 10))
            self.waitingReminder = Label(self, (210, 490), False, (100, 40), "请等待...", QFont("宋体", 10), False, Qt.AlignCenter)
            self.show()

        def confirmButtonFunc(self):
            if self.shipcount != 0:
                QMessageBox.warning(self, "错误", "船只未全部放置")
                return
            else:
                for i in range(10):
                    for j in range(10):
                        if self.sea[i][j] == self.SHIP:
                            self.Ships.append((i, j))
                self.threadError(self.Client.send("over"))
                self.recvThread.start()
                for Buttons in self.blockButtons:
                    for Button in Buttons:
                        Button.setDisabled(True)
                self.confirmbutton.hide()
                self.waitingReminder.show()
                return

        def closeEvent(self, e:QCloseEvent) -> None:
            if self.closeAll == True:
                _exit(0)
            else:
                e.accept()

        def selectShipFunc(self, pos):
            x, y = pos[0], pos[1]
            if self.sea[x][y] == self.SHIP:
                self.sea[x][y] = self.BLANK
                self.shipcount += 1
                self.blockButtons[x][y].setStyleSheet("QPushButton{border-image:url()}")
            else:
                if self.shipcount == 0:
                    QMessageBox.warning(self, "错误", "船只数量已达上限", QMessageBox.Ok)
                else:
                    self.sea[x][y] = self.SHIP
                    self.shipcount -= 1
                    self.blockButtons[x][y].setStyleSheet("QPushButton{border-image:url(ship.png)}")
            pass

    class recvThread(QThread):
        msgSignal = pyqtSignal(bool)
        ErrorSignal = pyqtSignal(tuple)
        
        def __init__(self, Client:myClient) -> None:
            super().__init__()
            self.Client = Client

        def run(self):
            msg = self.Client.recv(1024)
            if msg[0] == self.Client.ENCRYPTERROR:
                self.ErrorSignal.emit(("加/解密时错误", str(msg[1])))
            elif msg[0] == self.Client.SOCKETERROR:
                self.ErrorSignal.emit(("通信时错误", str(msg[1])))
            elif msg[0] == self.Client.UNKNOWNERROR:
                self.ErrorSignal.emit(("未知错误", str(msg[1])))
            elif msg == (self.Client.OK, "over"):
                self.msgSignal.emit(True)
            return

    App = QApplication(argv)
    setSeaWindow = Window(Client)
    App.exec_()
    return setSeaWindow.Ships

def Battle(myturn:bool, Client:myClient, Ships:list):

    class Window(QWidget):
        def __init__(self, myturn, Client:myClient, Ships):
            super().__init__()
            self.myturn = myturn
            self.Client = Client
            self.myShips = Ships
            self.closeAll = True
            self.reBattle = False

            self.BLANK = "$blank$"
            self.SHIP = "$ship$"
            self.DESTROYED = "$destroyed$" # ship
            self.BOOMED = "$boomed$" # No ship
            self.FAIL = "$fail$"

            self.mySea = [[self.BLANK for j in range(10)] for i in range(10)]
            for i in self.myShips:
                x, y = i[0], i[1]
                self.mySea[x][y] = self.SHIP

            self.opSea = [[self.BLANK for j in range(10)] for i in range(10)]

            self.recvThread = recvThread(self.Client, self)
            self.recvThread.ErrorSignal.connect(self.dealError)
            self.recvThread.recvSignal.connect(self.setFail)
            self.reBattleThread = reBattleThread(self.Client, self)
            self.reBattleThread.ErrorSignal.connect(self.dealError)
            self.reBattleThread.recvSignal.connect(self.checkReBattle)
            if self.myturn == False:
                self.recvThread.start()
            self.initUI()

        def checkReBattle(self, e):
            if e == True:
                self.closeAll = False
                self.close()
                self.closeAll = True
            else:
                QMessageBox.information(self, "提示", "对方拒绝再来一局", QMessageBox.Ok)
                self.reBattle = False

        def setFail(self, e):
            self.myturnReminder.setText("你输了")
            for Buttons in self.opSeaBlockButton:
                for Button in Buttons:
                    Button.setDisabled(True)
            LoseMessageBox = MessageBox("你输了", "你输了！")
            LoseMessageBox.exec_()
            if LoseMessageBox.clickedButton() == LoseMessageBox.ReButton:
                self.reBattle = True
                self.reBattleThread.start()
            elif LoseMessageBox.clickedButton() == LoseMessageBox.NoButton:
                self.dealError(self.Client.send(str(False)))
            return

        def checkfail(self):
            return self.myShips == []

        def initUI(self):
            self.setGeometry(300, 300, 925, 510)
            self.setWindowTitle("开战")
            self.setWindowIcon(QIcon("icon.ico"))

            self.mySeaBlockButton = [[Button(self, (50+40*i, 80+40*j), False, False, (40, 40), False, True, False) for j in range(10)] for i in range(10)]
            for i in range(10):
                for j in range(10):
                    if (i, j) in self.myShips:
                        self.mySeaBlockButton[i][j].setStyleSheet("QPushButton{border-image:url(ship.png)}")
            self.mySeaReminder = Label(self, (20,20), True, (80, 40), "我方", QFont("宋体", 12), False, Qt.AlignCenter)
           
            self.opSeaBlockButton = [[Button(self, (475+40*i, 80+40*j), self.attackFunc, (i, j), (40, 40), False, True) for j in range(10)] for i in range(10)]
            self.opSeaReminder = Label(self, (825, 20), True, (80, 40), "对方", QFont("宋体", 12), False, Qt.AlignCenter)

            self.myturnReminder = Label(self, (412, 30),True, (150, 30), "请选择" if self.myturn else "对方正在思考", QFont("宋体", 10), False, Qt.AlignCenter)
            self.show()

        def dealError(self, e:tuple):
            if e[0] == self.Client.OK:
                pass
            elif e[0] == self.Client.ENCRYPTERROR:
                QMessageBox.warning(self, "错误", "加/解密时错误"+str(e[1]), QMessageBox.Ok)
            elif e[0] == self.Client.SOCKETERROR:
                QMessageBox.warning(self, "错误", "通信错误"+str(e[1]), QMessageBox.Ok)
            elif e[0] == self.Client.UNKNOWNERROR:
                QMessageBox.warning(self, "错误", "未知错误"+str(e[1]), QMessageBox.Ok)
            return
                
        def attackFunc(self, pos):
            x, y = pos[0], pos[1]
            if self.myturn:
                if self.opSea[x][y] == self.BOOMED or self.opSea[x][y] == self.DESTROYED:
                    return
                res = self.Client.send(str(pos))
                if res == (self.Client.OK, None):
                    pass
                else:
                    self.dealError(res)
                    return
                res = self.Client.recv(1024)
                if res[0] == self.Client.OK:
                    if res[1] == self.FAIL:
                        self.opSea[x][y] = self.DESTROYED
                        self.opSeaBlockButton[x][y].setStyleSheet("QPushButton{border-image:url(ship_destroyed.png)}")
                        self.myturnReminder.setText("你赢了")
                        for Buttons in self.opSeaBlockButton:
                            for Button in Buttons:
                                Button.setDisabled(True)
                        WinMessageBox = MessageBox("你赢了", "你赢了！")
                        WinMessageBox.exec_()
                        if WinMessageBox.clickedButton() == WinMessageBox.ReButton:
                            self.reBattle = True
                            self.reBattleThread.start()
                        elif WinMessageBox.clickedButton() == WinMessageBox.NoButton:
                            self.dealError(self.Client.send(str(False)))
                        return
                    
                    elif res[1] == self.SHIP:
                        self.opSea[x][y] = self.DESTROYED
                        self.opSeaBlockButton[x][y].setStyleSheet("QPushButton{border-image:url(ship_destroyed.png)}")
                    
                    elif res[1] == self.BLANK:
                        self.opSea[x][y] = self.BOOMED
                        self.opSeaBlockButton[x][y].setStyleSheet("QPushButton{border-image:url(boomed.png)}")
                        self.myturn = False
                        self.myturnReminder.setText("对方正在思考")
                        self.recvThread.start()
                else:
                    pass

        def closeEvent(self, e:QCloseEvent) -> None:
            if self.closeAll:
                _exit(0)
            else:
                e.accept()

    class MessageBox(QMessageBox):
        def __init__(self, title, text):
            super().__init__()
            self.setWindowTitle(title)
            self.setText(text)
            self.setIcon(1)
            self.ReButton = self.addButton(self.tr("再来一局"), QMessageBox.YesRole)
            self.NoButton = self.addButton(self.tr("取消"), QMessageBox.NoRole)

    class recvThread(QThread):
        ErrorSignal = pyqtSignal(tuple)
        recvSignal = pyqtSignal(bool)

        def __init__(self, Client:myClient, surface:Window):
            super().__init__()
            self.Client = Client
            self.surface = surface
        
        def run(self):
            res = self.Client.recv(1024)
            if res[0] == self.Client.OK:
                pos = eval(res[1])
                x, y = pos[0], pos[1]
                if self.surface.mySea[x][y] == self.surface.SHIP:
                    self.surface.mySea[x][y] = self.surface.DESTROYED
                    self.surface.mySeaBlockButton[x][y].setStyleSheet("QPushButton{border-image:url(ship_destroyed.png)}")
                    self.surface.myShips.remove(pos)
                    if self.surface.checkfail():
                        res = self.Client.send(self.surface.FAIL)
                        if res[0] == self.Client.OK:
                            pass
                        else:
                            self.ErrorSignal.emit(res)
                            return
                        self.recvSignal.emit(True)
                    else:
                        res = self.Client.send(self.surface.SHIP)
                        if res[0] == self.Client.OK:
                            pass
                        else:
                            self.ErrorSignal.emit(res)
                            return
                        self.run()
                        return
                else:
                    self.surface.mySea[x][y] = self.surface.BOOMED
                    self.surface.mySeaBlockButton[x][y].setStyleSheet("QPushButton{border-image:url(boomed.png)}")
                    res = self.Client.send(self.surface.BLANK)
                    if res[0] == self.Client.OK:
                        pass
                    else:
                        self.ErrorSignal.emit(res)
                        return
                    self.surface.myturn = True
                    self.surface.myturnReminder.setText("请选择")
                    return
            else:
                self.ErrorSignal.emit(res)
                return

    class reBattleThread(QThread):
        recvSignal = pyqtSignal(bool)
        ErrorSignal = pyqtSignal(tuple)

        def __init__(self, Client:myClient, surface:Window):
            super().__init__()
            self.Client = Client
            self.surface = surface

        def run(self):
            res = self.Client.send(str(self.surface.reBattle))
            if res[0] == self.Client.OK:
                pass
            else:
                self.ErrorSignal.emit(res)
                return
            res = self.Client.recv(1024)
            if res[0] == self.Client.OK:
                self.recvSignal.emit(eval(res[1]))
                return
            else:
                self.ErrorSignal.emit(res)
                return

    App = QApplication(argv)
    BattleWindow = Window(myturn, Client, Ships)
    App.exec_()
    return BattleWindow.reBattle

def main():
    seed(time())
    ipMode, ClientMode = selectClient()

    if ClientMode == "server":
        client, myturn= Server(ipMode)
    else:
        client, myturn = Client(ipMode)
    
    reBattle = True
    while reBattle:
        Ships = setSea(client)
        reBattle = Battle(myturn, client, Ships)

if __name__ == "__main__":
    main()