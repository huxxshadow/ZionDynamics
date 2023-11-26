# import socket
# # 创建一个socket对象，默认TCP套接字
# s = socket.socket()
# # 绑定端口
# s.bind(('192.168.137.1',9006))
# # 监听端口
# s.listen(5)
# print("正在连接中……")
#
# # 建立连接之后，持续等待连接
# while 1:
#     # 阻塞等待连接
#     sock,addr = s.accept()
#     print(sock,addr)
#     # 一直保持发送和接收数据的状态
#     while 1:
#         text = sock.recv(1024)
#         # 客户端发送的数据为空的无效数据
#         if len(text.strip()) == 0:
#             print("服务端接收到客户端的数据为空")
#         else:
#             print("收到客户端发送的数据为：{}".format(text.decode()))
#             content = input("请输入发送给客户端的信息：")
#             # 返回服务端发送的信息
#             sock.send(content.encode())
#
#     sock.close()

# import asyncio
# from asyncio import StreamReader, StreamWriter
# import re
#
# async def echo(reader: StreamReader, writer: StreamWriter):
#     data = await reader.read(100)
#     message = data.decode()
#     addr = writer.get_extra_info('peername')
#
#     print(f"Received {message!r} from {addr!r}")
#     print(f"Send: {message!r}")
#
#     writer.write(data*2)
#     await writer.drain()
#
#     writer.close()
#
# async def task_read(reader: StreamReader,messageType:str):
#     data = await reader.read(100)
#     message = data.decode()
#
#
#
#
#
#
#
#
#
# async def main(host, port):
#     server = await asyncio.start_server(echo, host, port)
#     addr = server.sockets[0].getsockname()
#     print(f'Serving on {addr}')
#     async with server:
#         await server.serve_forever()
#
# asyncio.run(main("192.168.137.1", 9006))
