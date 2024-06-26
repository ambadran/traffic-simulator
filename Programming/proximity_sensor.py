'''
Component to interface proximity sensor
'''
from machine import Pin

class ProximitySensor:
    '''
    Class to interface proximity sensor
    '''
    def __init__(self, pin_num):
        self._pin = Pin(pin_num, Pin.IN)

    @property
    def state(self):
        '''
        returns current state of proximity sensor
        '''
        return not self._pin.value()
