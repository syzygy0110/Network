import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QThread

class ReceiveThread(QThread):
    # 定义一个信号，将接收到的消息作为字符串传递
    message_received = pyqtSignal(str)
    
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.running = True

    def run(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    # 发射信号，将接收到的数据解码后传递出去
                    self.message_received.emit(data.decode('utf-8'))
                else:
                    break
            except Exception as e:
                print("接收消息异常：", e)
                break

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class ChatClient(QMainWindow):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.setWindowTitle("PyQt 聊天客户端")
        self.resize(500, 400)
        
        # 建立 socket 连接
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_ip, server_port))
        except Exception as e:
            print("连接服务器失败：", e)
            sys.exit(1)
        
        # 创建 UI 控件
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_input = QLineEdit()
        self.send_button = QPushButton("发送")
        self.send_button.clicked.connect(self.send_message)
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        layout.addWidget(self.text_input)
        layout.addWidget(self.send_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # 创建接收消息线程，并连接信号
        self.receive_thread = ReceiveThread(self.client_socket)
        self.receive_thread.message_received.connect(self.display_message)
        self.receive_thread.start()
        
    def display_message(self, message):
        # 将接收到的消息追加到聊天记录中
        self.text_display.append(message)
        
    def send_message(self):
        message = self.text_input.text().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                # 这里也可以将自己的发送记录显示在界面上
                self.text_display.append("我: " + message)
                self.text_input.clear()
            except Exception as e:
                self.text_display.append("发送消息失败：" + str(e))
                
    def closeEvent(self, event):
        # 关闭窗口时停止线程并关闭 socket
        self.receive_thread.stop()
        self.client_socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 请确保服务器已经启动，并输入正确的 IP 与端口（例如127.0.0.1和9999）
    server_ip = "127.0.0.1"
    server_port = 9999
    window = ChatClient(server_ip, server_port)
    window.show()
    sys.exit(app.exec_())
