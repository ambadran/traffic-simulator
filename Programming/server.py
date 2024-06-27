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
    SSID = const("iPhone 15 Pro")
    PASSWORD = const("dnjdjcnd")

    JAVASCRIPT_TO_PYTHON = {'on': 1, 'off': 0, 'forward': 1, 'backward': -1}
    DEFAULT_WEB_NAME = 'index.html'
    def __init__(self):
        '''
        initiate server
        '''
        self.reset()
        self.connect()
        self.init_socket()

        #TODO: redefine this datastructure to hold sensor data for 6 different modules
        self.sensors_dict = {
                'proximity': 0,
                'captureBtn': 0
                }

        self.actuators_dict = {
               'redLed': 50,
               'yellowLed': 50,
               'greenLed': 50,
               }

        self.IDENTIFY_HTML_REQUEST = {
                'GET /': HTML_REQUEST.GET_WEB,
                } 

        self.HANDLE_HTML_REQUEST = {
                HTML_REQUEST.GET_WEB: self.handle_get_web,
                }
 
    def reset(self):
        '''
        returns station object on reset.
        just deactivate and activate again 
        '''
        self.station = network.WLAN(network.STA_IF)
        # self.station.config(ssid=self.SSID, password=self.PASSWORD)
        #TODO:

        self.station.active(False)
        sleep(2)
        self.station.active(True)

    def connect(self):
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

    def init_socket(self):
        '''
        initiate socket connection
        '''
        try:
            # self.station.config(ssid=self.SSID, password=self.PASSWORD)
            #TODO:
            sleep_ms(500)

            self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(self.addr)
            self.s.listen(1)  # Reduce the backlog to minimize memory usage
            print('Listening on', self.addr)
        except OSError as e:
            print(f"Caught: {e}")

    def wait_for_client(self):
        '''
        Await client to connect then return new socket object used to 
        communicate with the connected client. 
        This socket is distinct from the listening socket (s) 
        and is used for sending and receiving data with the specific client that connected.
        '''
        try:
            # self.station.config(ssid=self.SSID, password=self.PASSWORD)
            #TODO:
            sleep_ms(500)

            self.client, addr = self.s.accept()
            print('Got a connection from %s' % str(addr))
        except Exception as e:
            print(f"Caught: {e}")
        # finally:
        #     self.client.close()

    def identify_html_request(self) -> HTML_REQUEST:
        '''
        return what HTML request is given. 
        Every HTML request must be mapped to a function that handles it.
        '''
        self.request = self.client.recv(1024).decode()
        
        tmp = self.request.split(' ')
        if len(tmp) > 1:
            tmp = tmp[0] + ' ' + tmp[1]

        return self.IDENTIFY_HTML_REQUEST.get(tmp, None)

    def handle_html_request(self, html_request: HTML_REQUEST):
        '''
        handles the identified html request
        '''
        try:
            if html_request is not None:
                self.HANDLE_HTML_REQUEST[html_request]()
        
            else:
                self.handle_unkonwn_request()
                print(f"Got unkonwn Request:\n{self.request}")

        except Exception as e:
            print(f"Error in handle web get request: {e}")
            print(f"html request detected: {html_request}")
            print(f"Raw html request:\n{self.request}")

        finally:
            self.client.close()

    def handle_get_web(self):
        '''
        Handles HTML GET WEB Request
        '''
        with open('index.html', 'r') as f:
            web_page = f.read()

        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.sendall(web_page)

    def handle_unkonwn_request(self):
        '''
        Handles unknown request
        '''
        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.send('HTTP/1.1 404 Not Found\r\n\r\nFile Not Found')


