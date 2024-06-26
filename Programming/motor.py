'''
Abstraction to control the MOTOR speed
'''
from machine import Pin, PWM

class DCMotor:
    '''
    Object to control Motor
    '''
    DUTY_0 = const(0)
    DUTY_25 = const(16384)
    DUTY_50 = const(32728)
    DUTY_75 = const(49151)
    DUTY_100 = const(65535)

    DEFAULT_FREQUENCY = const(20000)
    DEFAULT_DUTY = const(DUTY_50)
    def __init__(self, pwm_pin_num, dir_pin_num):
        self._pwm = PWM(Pin(pwm_pin_num), freq=DEFAULT_FREQUENCY, duty_u16=DEFAULT_DUTY)
        self._dir_pin = Pin(dir_pin_num, Pin.OUT)

    def set(self, pwm_value):
        '''
        Sets pwm duty cycle in 16-bit value
        '''
        self._pwm.duty_u16(pwm_value)

    @property
    def dir(self):
        '''
        getter for direction value
        '''
        return self._dir_pin.value()

    @dir.setter
    def dir(self, dir_value):
        '''
        setter for direction value
        '''
        self._dir_pin.value(dir_value)

    def dir_toggle(self):
        '''
        toggles direction
        '''
        self._dir_pin.value(not self._dir_pin.value())
