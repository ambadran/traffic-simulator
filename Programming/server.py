'''
Meant to run on the second Core of Pico for Optimal Performance
    - Host Web App (HTML file including the CSS and JAVASCRIPT)
    - Serve the HTML GET and POST requests
    - Updates internal variables to control Actuators through other Core
    - Updates the real-time Sensor values displayed on the Web App
'''
from micropython import const
from machine import Pin
import network
import socket
import json
from time import sleep, sleep_ms

class HTML_REQUEST:
    GET_WEB = 0
    

class Server:
    # Access Point Parameters
    SSID = const("Orange-79BC")
    PASSWORD = const("MGMEN6M54LR")

    SERVER_IP = const("192.168.1.107")
    SERVER_PORT = const("4400")
    def __init__(self):
        '''
        initiate server
        '''
        self.reset()
        self.connect_wifi()

        self.addr = (self.SERVER_IP, self.SERVER_PORT)

    def reset(self):
        '''
        returns station object on reset.
        just deactivate and activate again 
        '''
        self.station = network.WLAN(network.STA_IF)
        self.sock = socket.socket()
        #TODO:

        self.station.active(False)
        sleep(2)
        self.station.active(True)

    def connect_wifi(self):
        '''
        connect to wifi
        '''
        if not self.station.isconnected():
                print('connecting to network...')
                self.station.active(True)
                self.station.connect(SSID, PASSWORD)
                while not self.station.isconnected():
                    pass
        print('network config:', self.station.ifconfig())

    def socket_connect(self):
        '''
        connect to socket
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)
        # return self.sock.recv(1024)  #TODO:

    def socket_send_data(self, img):
        '''
        sends data to socket
        '''
        # self.sock.sendall(f"124,{img}")
        self.sock.sendall(img)

    def socket_disconnect(self):
        '''
        closes socket safely
        '''
        self.sock.close()


