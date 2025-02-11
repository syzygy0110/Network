import socket
import threading

def receive_messages(client_socket):
    """在单独的线程中接收并打印服务器发送过来的消息"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode('utf-8'))
        except Exception as e:
            print("接收消息出错：", e)
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("请输入服务器IP（例如127.0.0.1）：")
    server_port = int(input("请输入服务器端口（例如9999）："))
    try:
        client_socket.connect((server_ip, server_port))
    except Exception as e:
        print("连接失败：", e)
        return
    print("成功连接到服务器！")
    
    # 开启线程用于不断接收消息
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    
    print("请输入消息（输入 exit 退出）：")
    while True:
        msg = input("")
        if msg.lower() == 'exit':
            break
        try:
            client_socket.send(msg.encode('utf-8'))
        except Exception as e:
            print("发送消息失败：", e)
            break
    client_socket.close()

if __name__ == '__main__':
    start_client()
