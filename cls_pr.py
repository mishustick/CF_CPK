import struct
import socket
import threading
from time import perf_counter
from datetime import datetime
from queue import Queue


class Message:

    def __init__(self, header=0, g_ref=0, phi_x=0, phi_y=0, phi_z=0,
                 nx=0, ny=0, nz=0, end=0):
        self.header = header
        self.gref = g_ref
        self.phix = phi_x
        self.phiy = phi_y
        self.phiz = phi_z
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.end = 0
        self.wx, self.wy, self.wz = 0, 0, 0
        self.time = datetime.now()
        self.bts = bytes()

    @staticmethod
    def bts2dbl(bts):
        if bts[:4] == b'9\x00\x00\x00':  # Если заголовок 57
            got_mes = struct.unpack('<'+16 * 'i' + 7 * 'f' + 6 * 'i', bts)
            header = got_mes[0]
            nx = got_mes[16]
            ny = got_mes[17]
            nz = got_mes[18]
            phix = got_mes[19]
            phiy = got_mes[20]
            phiz = got_mes[21]
            gref = got_mes[22]
            end = got_mes[28]
            return Message(header, g_ref=gref, phi_x=phix, phi_y=phiy, phi_z=phiz,
                     nx=nx, ny=ny, nz=nz)
        elif bts[:4] == b'B\x00\x00\x00':  # Если заголовок 66
            got_mes = struct.unpack(17 * 'i' + 7 * 'f', bts)
            header = got_mes[0]
            nx = got_mes[17]
            ny = got_mes[18]
            nz = got_mes[19]
            phix = got_mes[20]
            phiy = got_mes[21]
            phiz = got_mes[22]
            gref = got_mes[23]
            return Message(header, g_ref=gref, phi_x=phix, phi_y=phiy, phi_z=phiz,
                           nx=nx, ny=ny, nz=nz)

    def dbl2bts(self):
        # Для отправки
        # Упаковка заголовка + 16 нулей + 7 полезных переменных
        self.bts = bytes()
        self.bts += struct.pack('i', 66)
        for i in range(16):
            self.bts += struct.pack('i', 0)
        for val in self.na():
            self.bts += struct.pack('f', self.na()[val])

    def na(self):
        return {'nx': self.nx, 'ny': self.ny,
                'nz': self.nz, 'phix': self.phix, 'phiy': self.phiy,
                'phiz': self.phiz, 'gref': self.gref}

    def __str__(self):
        return f'{self.nx};{self.ny};{self.nz};{self.phix};' \
               f'{self.phiy};{self.phiz};{self.phiz};'


    #def noise(self):
    #    us_dat = ['nx', 'ny', 'nz', 'phix', 'phiy', 'phiz', 'gref']
    #    for x in dir(self):
    #        if not x.startswith('_') and getattr(self, x) != 0 and x in us_dat:
    #            self.__setattr__(x, self.__getattribute__(x) + numpy.random.normal(0, 0.01))


class SenRec:

    def __init__(self, ip, port, chr='sen',):
        self.ip = ip
        self.port = port
        self.chr = chr
        self.receiving = False
        self.sending = False
        self.que_sen = Queue()
        self.que_rec = Queue()
        self.data_sen = []

    def start_sen(self):
        t_sen = threading.Thread(target=self.sender)
        t_sen.start()

    def sender(self):
        print('Отправитель запущен!')
        UDP_IP = self.ip
        UDP_PORT = self.port
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        while True:
            item = self.que_sen.get()  # Получаем сообщение из очереди
            item.dbl2bts()  # Переводим в байты
            item.time = datetime.now()
            sock.sendto(item.bts, (UDP_IP, UDP_PORT))
            self.data_sen.append(item)
            print('Отправил:', item)
            if len(self.data_sen) == 1:
                self.que_rec.put(self.data_sen)
                print('HEADER:', self.data_sen[0].header)
                self.data_sen = []

    def start_rec(self):
        if self.receiving:
            return
        self.receiving = True

        print('Получение запущено')
        UDP_IP = self.ip
        UDP_PORT = self.port
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        data_rec = []
        while self.receiving:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            m = Message.bts2dbl(data)
            print(m.time, m.na())
            data_rec.append(m)
            if len(data_rec) == 10:
                self.que_rec.put(data_rec)  # Добавляем текущий кэш сообщений в очередь на запись
                data_rec = []  # Сбрасываем текущий кэш сообщений

    def star_saver(self):
        t_sav = threading.Thread(target=self.saver)  # Создаем поток на запись
        print('Saver запущен!')
        t_sav.start()

    def saver(self):
        while True:
            que = self.que_rec
            items = que.get()
            f_rec = open('log_rec.txt', 'a')
            f_sen = open('log_sen.txt', 'a')
            for el in items:
                if el.header == 57:
                    f_rec.write(str(el.time)+';'+str(el)+str(el.header)+'\n')
                elif el.header == 66:
                    f_sen.write(str(el.time)+';'+str(el)+str(el.header)+'\n')
            f_rec.close()
            f_sen.close()


if __name__ == '__main__':
    m = Message(header=57, nx=1, ny=1, nz=1)
    print(m.nx)
    print(m.na())
    m.dbl2bts()
    print(struct.unpack(17*'i'+7*'f',m.bts))
