import socket
import struct
from queue import Queue
import threading
from cls_pr import Message, SenRec


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

rec = SenRec(ip=res_ip, port=5004, chr='rec')
t_rec = threading.Thread(target=rec.start_rec)
t_rec.start()
sen = SenRec(ip=res_ip, port=5004)
sen.star_saver()
rec.star_saver()
sen.start_sen()

