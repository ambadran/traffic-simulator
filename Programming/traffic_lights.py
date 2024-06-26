'''
Component implementing class to easily control the traffic lights
'''
from machine import Pin
from time import sleep_ms

class TrafficLight:
    '''
    Class to easily control Traffic light
    '''
    def __init__(self, red_led_pin_num, yellow_led_pin_num, green_led_pin_num):
        self.red_led = Pin(red_led_pin_num, Pin.OUT)
        self.yellow_led = Pin(yellow_led_pin_num, Pin.OUT)
        self.green_led = Pin(green_led_pin_num, Pin.OUT)

        self.leds = (self.red_led, self.yellow_led, self.green_led)

        self._current_led_ind = 2 # so that first call will light up the red led

    def next_light(self):
        '''
        function to close the previous light and open the next light in order (red, yellow, green)
        '''
        self.leds[self._current_led_ind].off()

        self._current_led_ind += 1
        if self._current_led_ind > 2:
            self._current_led_ind = 0

        self.leds[self._current_led_ind].on()

    def off(self):
        '''
        closes off all the lights
        '''
        self.red_led.off()
        self.yellow_led.off()
        self.green_led.off()

    def on(self):
        '''
        Turns on all the lights
        '''
        self.red_led.on()
        self.yellow_led.on()
        self.green_led.on()

    def flash_all(self):
        '''
        flashes all leds 3 times with 0.5 second gaps
        '''
        for _ in range(3):
            self.on()
            sleep_ms(500)
            self.off()
            sleep_ms(500)


