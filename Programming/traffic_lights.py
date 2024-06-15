'''
Component implementing class to easily control the traffic lights
'''
class TrafficLight:
    '''
    Class to easily control Traffic light
    '''
    def __init__(self, red_led_pin_num, yellow_led_pin_num, green_led_pin_num):
        self.red_led = Pin(RED_LED_PIN_NUM, Pin.OUT)
        self.yellow_led = Pin(YELLOW_LED_PIN_NUM, Pin.OUT)
        self.green_led = Pin(GREEN_LED_PIN_NUM, Pin.OUT)

        self.NEXT_LED = {self.red_led: self.yellow_led,
                         self.yellow_led: self.green_led,
                         self.green_led: self.red_led}

        self._current_led = self.green_led  # so that first call will light up the red led

    def next_light(self):
        '''
        function to close the previous light and open the next light in order (red, yellow, green)
        '''
        self._current_led.off()
        self._current_led = self.NEXT_LED[self._current_led]
        self._current_led.on()

    def off(self):
        '''
        closes off all the lights
        '''
        self.red_led.off()
        self.yellow_led.off()
        self.green_led.off()


