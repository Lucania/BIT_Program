import linecache
import socket
import struct
import time

list_former = []
list_medium = []
list_later = []

# 创建UDP客户端
client = socket.socket(type=socket.SOCK_DGRAM)
ip_port = ('127.0.0.1', 1200)
client.connect(ip_port)

f = open(r'D:\滑雪\复现\data.txt', 'r')
length = len(f.readlines())  # 获取文件总行数
# print(length)
for i in range(1, length):
    list_former = linecache.getline(r'D:\滑雪\复现\data.txt', i).split(',')  # 相邻两包数据，用","分割，返回一个列表
    list_later = linecache.getline(r'D:\滑雪\复现\data.txt', i+1).split(',')

    for t in range(4):  # 去除包中前四个不是姿态的数据
        list_former.pop(0)
        list_later.pop(0)
    for t in range(8):  # 去除包中后八个不是姿态的数据
        list_former.pop(-1)
        list_later.pop(-1)
    # print(list_former)
    # print(list_later)
    list_medium = []  # 进行中间包的计算
    for t in range(len(list_former)):
        list_medium.append((int(list_former[t]))/2 + (int(list_later[t]))/2)  # 将前后相邻两包的数据作平均可得到中间包的数据
    # print(list_medium)
    # 发送给Unity
    if i == 1:  # 在第一次发送时需要发送前面一包
        client.send('AA'.encode())
        for j in list_former:
            client.send(struct.pack("!h", int(j)))
        time.sleep(0.05)
    # 第二次及以后发送中间包和后一包
    client.send('AA'.encode())
    for j in list_medium:
        client.send(struct.pack("!h", int(j)))
    time.sleep(0.05)
    client.send('AA'.encode())
    for j in list_later:
        client.send(struct.pack("!h", int(j)))
    time.sleep(0.05)

client.close()
f.close()




