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
    GET_SENSORS_WEB = 0
    GET_ACTUATORS_WEB = 1
    GET_MPC_WEB = 2
    GET_SENSOR_DATA = 3
    GET_MPC_VALUES = 4
    POST_ACTUATOR_STATES = 5
    POST_TOGGLE_MPC = 6

class Server:
    # Access Point Parameters
    SSID = "SIMACAS"
    PASSWORD = "12345678"

    JAVASCRIPT_TO_PYTHON = {'on': 1, 'off': 0, 'forward': 1, 'backward': -1}
    DEFAULT_WEB_NAME = 'actuators.html'
    def __init__(self):
        '''
        initiate server
        '''
        self.led = Pin("LED", Pin.OUT)  # on-board LED to show state
        self.led.off()

        self.reset()
        #TODO: implement try except block to avoid redefining socket
        self.init_access_point()
        self.init_socket()

        #TODO: redefine this datastructure to hold sensor data for 6 different modules
        self.sensors_dict = {
                'temperature': 0,
                'humidity': 0,
                'soilMoisture': 0,
                'lightIntensity': 0,
                'co2Concentration': 0
                }

        self.actuators_dict = {
               'mechanism1': 0,
               'mechanism2': 0,
               'mechanism3': 0,
               'water1': 0,
               'water2': 0,
               'water3': 0,
               'fertilizer1': 0,
               'fertilizer2': 0,
               'fertilizer3': 0,
               'light1': 50,
               'light2': 50,
               'light3': 50,
               }

        self.mpc_dict = {
               'mpcEnabled': False,
                }

        self.IDENTIFY_HTML_REQUEST = {
                'GET /': HTML_REQUEST.GET_ACTUATORS_WEB,
                'GET /actuators.html': HTML_REQUEST.GET_ACTUATORS_WEB,
                'GET /sensors.html': HTML_REQUEST.GET_SENSORS_WEB,
                'GET /mpc.html': HTML_REQUEST.GET_MPC_WEB,
                'GET /get-sensor-data': HTML_REQUEST.GET_SENSOR_DATA,
                'GET /get-mpc-values': HTML_REQUEST.GET_MPC_VALUES,
                'POST /control': HTML_REQUEST.POST_ACTUATOR_STATES,
                'POST /toggle-mpc': HTML_REQUEST.POST_TOGGLE_MPC
                } 

        self.HANDLE_HTML_REQUEST = {
                HTML_REQUEST.GET_ACTUATORS_WEB: self.handle_get_web,
                HTML_REQUEST.GET_SENSORS_WEB: self.handle_get_web,
                HTML_REQUEST.GET_MPC_WEB: self.handle_get_web,
                HTML_REQUEST.GET_SENSOR_DATA: self.handle_get_sensor_data,
                HTML_REQUEST.GET_MPC_VALUES: self.handle_get_mpc_values,
                HTML_REQUEST.POST_ACTUATOR_STATES: self.handle_post_actuator_states,
                HTML_REQUEST.POST_TOGGLE_MPC: self.handle_post_toggle_mpc
                }
 
    def reset(self):
        '''
        returns station object on reset.
        just deactivate and activate again 
        '''
        self.station = network.WLAN(network.AP_IF)
        self.station.config(ssid=self.SSID, password=self.PASSWORD)

        self.station.active(False)
        sleep(2)
        self.station.active(True)

    def init_access_point(self):
        '''
        set up the Access Point
        '''
        self.station.config(ssid=self.SSID, password=self.PASSWORD)

        while not self.station.active():
            print(f"Station Initializing.. ", end=' \r')

        self.led.on()
        print('Access Point Active!')
        print(self.station.ifconfig())

    def init_socket(self):
        '''
        initiate socket connection
        '''
        try:
            self.station.config(ssid=self.SSID, password=self.PASSWORD)
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
            self.station.config(ssid=self.SSID, password=self.PASSWORD)
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
        Handles GET_ACTUATORS_WEB HTML GET Request
        '''
        web_name = self.request.split(' ')
        web_name = web_name[1]
        if web_name == '/':
            # default web
            web_name = self.DEFAULT_WEB_NAME

        else:
            web_name = web_name[1:]

        with open(web_name, 'r') as f:
            web_page = f.read()

        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        # self.client.send('HTTP/1.1 200 OK\n')
        # self.client.send('Content-Type: text/html\n')
        # self.client.send('Connection: close\n\n')
        self.client.sendall(web_page)

    def handle_get_sensor_data(self):
        '''

        '''
        #TODO: this is just for testing now
        sensor_data = {
            "temperature1": self.sensors_dict['temperature'], "humidity1": self.sensors_dict['humidity'], "soilMoisture1": self.sensors_dict['soilMoisture'], "lightIntensity1": self.sensors_dict['lightIntensity'], "co2Concentration1": self.sensors_dict['co2Concentration'],
            "temperature2": 0, "humidity2": 0, "soilMoisture2": 0, "lightIntensity2": 0, "co2Concentration2": 0,
            "temperature3": 0, "humidity3": 0, "soilMoisture3": 0, "lightIntensity3": 0, "co2Concentration3": 0,
            "temperature4": 0, "humidity4": 0, "soilMoisture4": 0, "lightIntensity4": 0, "co2Concentration4": 0,
            "temperature5": 0, "humidity5": 0, "soilMoisture5": 0, "lightIntensity5": 0, "co2Concentration5": 0,
            "temperature6": 0, "humidity6": 0, "soilMoisture6": 0, "lightIntensity6": 0, "co2Concentration6": 0
        }
        print("handling sensor request!")

        response = json.dumps(sensor_data)

        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.send(response)

    def handle_get_mpc_values(self):
        '''

        '''
        #TODO:
        mpc_values = {
            "temperatureReal": 3, "temperaturePredicted": 8, "temperatureLED": 3,
            "humidityReal": 18, "humidityPredicted": 1, "humidityLED": 2,
            "co2Real": 38, "co2Predicted": 2,
            "soilMoistureReal": 0, "soilMoisturePredicted": 1, "soilMoistureWater": "CLOSED",
            "lightIntensityReal": 9, "lightIntensityPredicted": 7, "lightIntensityLED": 4
        }

        response = json.dumps(mpc_values)

        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.send(response)


    def handle_post_actuator_states(self):
        '''

        '''
        #TODO:
        length = int(self.request.split('Content-Length: ')[1].split('\r\n')[0])
        body = json.loads(self.client.recv(length).decode('utf-8'))

        ### Handle actuator control by saving into actuators_dict ###
        # print('Control Request:', body)            
        key = body['component']
        value = body['action']
        if value in ['backward', 'forward']:
            self.actuators_dict[key] += self.JAVASCRIPT_TO_PYTHON[value]

        elif value in ['on', 'off']:
            self.actuators_dict[key] = self.JAVASCRIPT_TO_PYTHON[value]

        elif value.isdigit():
            self.actuators_dict[key] = int(value)

        else:
            raise ValueError("Unknown Post /control request")

        response = 'HTTP/1.1 200 OK\r\n\r\n'
        self.client.send(response)

    def handle_post_toggle_mpc(self):
        '''

        '''
        #TODO:
        length = int(self.request.split('Content-Length: ')[1].split('\r\n')[0])
        body = json.loads(self.client.recv(length).decode('utf-8'))

        print(f"MPC POST:\n{self.request}\nBody: {body}")

        self.mpc_dict['mpcEnabled'] = body['mpcEnabled'] 

        response = 'HTTP/1.1 200 OK\r\n\r\n'
        self.client.send(response)

    def handle_unkonwn_request(self):
        '''
        Handles unknown request
        '''
        self.client.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        self.client.send('HTTP/1.1 404 Not Found\r\n\r\nFile Not Found')


