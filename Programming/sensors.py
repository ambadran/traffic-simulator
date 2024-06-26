'''
Abstraction to deal with sensors
'''
from micropython import const
from proximity_sensor import ProximitySensor
from machine import Pin

class Sensors:
    '''
    Object to abstract sensors
    '''
    PROXIMITY_SENSOR_PIN_NUM = const(4)
    def __init__(self):
        self.proximity_sensor = ProximitySensor(PROXIMITY_SENSOR_PIN_NUM)


