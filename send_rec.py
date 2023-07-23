import socket
import struct
from queue import Queue
import threading
import time
from cls_pr import Message


def sending(UDP_IP, UDP_PORT):
    pass


# Запись в файл
def saver(que):
    print('Saver запущен!')
    while True:
        items = que.get()
        fi = open('log_rec.txt', 'a')
        for el in items:
            fi.write(str(el.time)+','+str(el)+'\n')
            time.sleep(0.05)
        fi.close()


def receiving(UDP_IP, UDP_PORT):
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    n = 0  # Счетчик сообщений
    global data_rec, curr_time
    print('Получение запущено!')
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        m = Message.bts2dbl(data)
        print(m.time, m.na())
        data_rec.append(m)
        n += 1  # Увеличиваем количество полученных сообщений
        if n == 100 or time.perf_counter() - curr_time > 10:
            n = 0
            queue.put(data_rec)  # Добавляем текущий кэш сообщений в очередь на запись
            data_rec = []  # Сбрасываем текущий кэш сообщений
            curr_time = time.perf_counter()  # Обновляем время


curr_time = time.perf_counter()

res_ip = "192.168.1.64"
sen_ip = "192.168.1.64"
data_rec = []
port = 5005
queue = Queue()

f = open('log_rec.txt', 'w')
f.write('time,nx,ny,nz,phix,phiy,phiz,gref\n')
f.close()

t_sending = threading.Thread(target=sending, args=(sen_ip, port))
t_reseveing = threading.Thread(target=receiving, args=(res_ip, port))
t_sav = threading.Thread(target=saver, args=(queue,))


t_sav.start()
t_reseveing.start()
t_sending.start()

t_reseveing.join()
t_sending.join()
