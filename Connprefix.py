from Crypto.Cipher import AES
import socket

class myClient():
    def __init__(self, sock:socket.socket, pwd:str) -> None:
        self.pwd = self.pad(pwd.encode("utf-8"))
        self.FLAG = "DHY"
        self.sock = sock
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60*1000, 30*1000))
        self.recvmsg = ""
        self.sendmsg = ""
        
        self.ENCRYPTERROR = "encrypterrorid:10000"
        self.SOCKETERROR = "socketerrorid:10001"
        self.UNKNOWNERROR = "unknownerrorid:10002"
        self.OK = "okid:10003"
        
    def pad(self, text:bytes) -> bytes:
        return text + b'\x00' * ((16 - len(text) %16) % 16)

    def encrypt(self, pwd:bytes, text:bytes) -> bytes:
        AESObj = AES.new(pwd, AES.MODE_EAX)
        msg, tag = AESObj.encrypt_and_digest(text)
        return AESObj.nonce + tag + msg

    def decrypt(self, pwd:bytes, nonce:bytes, tag:bytes, cipher_text:bytes) -> bytes:
        AESObj = AES.new(pwd, AES.MODE_EAX, nonce)
        return AESObj.decrypt_and_verify(cipher_text, tag)

    def send(self, msg:str) -> tuple:
        self.sendmsg = msg
        try:
            self.sendmsg = self.encrypt(self.pwd, self.FLAG.encode("utf-8")+msg.encode("utf-8"))
            # print(self.sendmsg)
            self.sock.sendall(self.sendmsg)
        except Exception as e:
            # print(e)
            if e == ValueError:
                return (self.ENCRYPTERROR, e)
            elif e == socket.error:
                return (self.SOCKETERROR, e)
            else:
                return (self.UNKNOWNERROR, e)
        return (self.OK, None)
    
    def recv(self, size:int = 1024) -> tuple:
        try:
            self.recvmsg = self.sock.recv(size)
            # print(self.recvmsg)
            nonce, tag, self.recvmsg = self.recvmsg[:16], self.recvmsg[16:32], self.recvmsg[32:]
            self.recvmsg = self.decrypt(self.pwd, nonce, tag, self.recvmsg).decode("utf-8")
            if self.recvmsg[:3] != self.FLAG:
                raise(socket.error)
            else:
                self.recvmsg = self.recvmsg[3:]
                return (self.OK, self.recvmsg)

        except Exception as e:
            # print(e)
            if e == ValueError:
                return (self.ENCRYPTERROR, e)
            elif e == socket.error:
                return (self.SOCKETERROR, e)
            else:
                return (self.UNKNOWNERROR, e)
