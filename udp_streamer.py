import socket
from struct import pack,unpack
import numpy as np
from time import time,sleep

class udp_handler(object):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.PKTSZ = 65500-12
		self.packets = {}
		self.pklist = []
		self.PKLEN = 2000000
		self.subtime = time()

	def make_listener(self,ip,port):
		self.sock.bind((ip,port))

	def send_data(self,img,ip,port):
		rembytes=1
		stt=0
		data=img.tobytes()
		pkid=img[np.random.randint(0,30)].sum()+np.random.random()*1000+(time()-self.subtime)*1000
		while rembytes>0:
			buffer=data[stt:stt+self.PKTSZ]
			stt+=self.PKTSZ
			rembytes=len(data)-stt
			if rembytes<=0:
				rembytes=0
			self.sock.sendto(pack('d',pkid)+pack('f',np.float32(rembytes))+buffer,(ip,port))

	def get_data(self):
		rembuf, address = self.sock.recvfrom(self.PKTSZ+12)
		pkid=unpack('d', rembuf[:8])[0]
		rembytes=unpack('f', rembuf[8:12])[0]
		buffer=rembuf[12:]
		try:
			self.packets[pkid]+=buffer
		except KeyError:
			self.packets[pkid]=buffer
			self.pklist.append(pkid)
			if len(self.pklist)>self.PKLEN:
				self.packets.pop(self.pklist.pop(0))
		if rembytes<=0:
			data=self.packets[pkid]
			self.packets.pop(pkid)
			self.pklist.remove(pkid)
		else:
			try:
				data=self.get_data()
			except RecursionError:
				data=None
		return data

	def send_data_small(self,img,ip,port):
		data=img.tobytes()
		self.sock.sendto(data,(ip,port))

	def get_data_small(self):
		data, address = self.sock.recvfrom(self.PKTSZ)
		return data

	def close(self):
		self.sock.close()