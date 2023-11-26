# import socket
# # 创建一个socket对象
# s1 = socket.socket()
# s1.connect(('192.168.137.203', 9006))
# # 不断发送和接收数据
# while 1:
#     send_data = input("客户端要发送的信息：")
#     # socket传递的都是bytes类型的数据,需要转换一下
#     s1.send(send_data.encode())
#     # 接收数据，最大字节数1024,对返回的二进制数据进行解码
#     text = s1.recv(1024).decode()
#     print("服务端发送的数据：{}".format(text))
#     print("------------------------------")

# import asyncio
#
#
# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection("192.168.137.1", 9006)
#     print(f'Send to server: {message!r}')
#
#     writer.write(message.encode())
#     await writer.drain()
#
#     data = await reader.read(100)
#     print(f'Received from server: {data.decode()!r}')
#
#     writer.close()
#     await writer.wait_closed()
#
#
# if __name__ == '__main__':
#     while True:
#         send_msg = input("send: ")
#         asyncio.run(tcp_echo_client(send_msg))
