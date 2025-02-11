import socket
import threading

# 存储所有已连接的客户端
clients = []

def broadcast(message, current_client):
    """将消息广播给所有客户端（除了发送者本身）"""
    for client in clients:
        if client != current_client:
            try:
                client.send(message)
            except Exception as e:
                print("发送消息出错：", e)
                clients.remove(client)

def handle_client(client_socket):
    """处理某个客户端的接收消息"""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print("接收到消息：", message.decode('utf-8'))
            broadcast(message, client_socket)
        except Exception as e:
            print("客户端异常：", e)
            break
    client_socket.close()
    if client_socket in clients:
        clients.remove(client_socket)
    print("客户端断开连接")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定到本机所有网卡，端口号9999（可自行更换）
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("服务器已启动，等待客户端连接...")
    
    while True:
        client_socket, addr = server.accept()
        print("新客户端连接：", addr)
        clients.append(client_socket)
        # 为每个客户端开启一个线程进行处理
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    start_server()
