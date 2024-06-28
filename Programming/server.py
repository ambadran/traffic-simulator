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
    SSID = const("Mr.A's Lab")
    PASSWORD = const("lskdmin2938#$")

    SERVER_IP = const("")
    def __init__(self):
        '''
        initiate server
        '''
        self.reset()
        self.connect_wifi()

        #TODO: redefine this datastructure to hold sensor data for 6 different modules
        self.sensors_dict = {
                'proximity': 0,
                'img': None
                }

        self.actuators_dict = {
               'redLed': 50,
               'yellowLed': 50,
               'greenLed': 50,
               }

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
        self.sockaddr = socket.getaddrinfo(SERVER_IP, 80, 0, socket.SOCK_STREAM)[0][-1]
        self.sock = socket.socket()
        self.sock.connect(self.sockaddr)

    def socket_send_data(self):
        '''
        sends data to socket
        '''

        text = f"124,{self.sensors_dict['img']}"
        self.sock.sendall()

    def socket_disconnect(self):
        '''
        closes socket safely
        '''
        self.sock.close()


