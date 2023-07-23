import struct
from time import perf_counter
from datetime import datetime


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

    def dbl2bts(self):
        # Упаковка заголовка + 16 нулей + 7 полезных переменных
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
        return f'{self.nx},{self.ny},{self.nz},{self.phix},' \
               f'{self.phiy},{self.phiz},{self.phiz}'


    #def noise(self):
    #    us_dat = ['nx', 'ny', 'nz', 'phix', 'phiy', 'phiz', 'gref']
    #    for x in dir(self):
    #        if not x.startswith('_') and getattr(self, x) != 0 and x in us_dat:
    #            self.__setattr__(x, self.__getattribute__(x) + numpy.random.normal(0, 0.01))


if __name__ == '__main__':
    m = Message(header=57, nx=1, ny=1, nz=1)
    print(m.nx)
    print(m.na())
    print(m.time)