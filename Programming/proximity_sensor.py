'''
Component to interface proximity sensor
'''

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
        return self._pin.value()
