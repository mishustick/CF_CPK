import socket
import struct
from queue import Queue
import threading
import time
from cls_pr import Message, SenRec


# Запись в файл

def receiving(UDP_IP, UDP_PORT):
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data_rec = []
    print('Получение запущено!')
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        m = Message.bts2dbl(data)
        print(m.time, m.na())
        data_rec.append(m)
        queue_sen.put(m)  # Передаем сообщение на отправку
        if len(data_rec) == 100:
            n = 0
            queue_rec.put(data_rec)  # Добавляем текущий кэш сообщений в очередь на запись
            data_rec = []  # Сбрасываем текущий кэш сообщений


def sending(UDP_IP, UDP_PORT, que_sen):
    print('Отправление запущено!')
    print("UDP target IP: %s" % UDP_IP)
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    data_sen = []
    while True:
        item = que_sen.get()
        item.dbl2bts()
        s_m = Message.bts2dbl(item.bts)
        data_sen.append(s_m)
        sock.sendto(item.bts, (UDP_IP, UDP_PORT))  # Отправляем в виде 66 + 15 * 0 + 7 п
        if len(data_sen) == 100:
            queue_rec.put(data_sen)
            data_sen = []


res_ip = "172.20.10.3"
sen_ip = "172.20.10.3"
port = 5004
queue_rec = Queue()
queue_sen = Queue()

f_r = open('log_rec.txt', 'w')
f_r.write('time;nx;ny;nz;phix;phiy;phiz;gref;header\n')
f_r.close()

f_s = open('log_sen.txt', 'w')
f_s.write('time;nx;ny;nz;phix;phiy;phiz;gref;header\n')
f_s.close()

#t_sending = threading.Thread(target=sending, args=(sen_ip, port, queue_sen))
#t_reseveing = threading.Thread(target=receiving, args=(res_ip, port))
#t_sav = threading.Thread(target=saver, args=(queue_rec,))

mes = Message.bts2dbl(b'B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x9a\x99\x99?\x9a\x99\x99?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
print(mes.header)
rec = SenRec(ip=res_ip, port=5004, chr='rec')
t_rec = threading.Thread(target=rec.start_rec)
t_rec.start()
sen = SenRec(ip=res_ip, port=5004)
sen.star_saver()
rec.star_saver()
sen.start_sen()
sen.que_sen.put(mes)


#t_reseveing.start()
#t_sav.start()
#t_sending.start()

#t_reseveing.join()
#t_sending.join()
