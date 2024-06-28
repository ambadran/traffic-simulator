'''
Component implementing class to easily control the traffic lights
'''
from machine import Pin, Timer
from time import sleep_ms

class TrafficLight:
    '''
    Class to easily control Traffic light
    '''
    DEFAULT_TIME_IN_BETWEEN = 1000  # 1 second
    RED_LED_IND = 0
    YELLOW_LED_IND = 1
    GREEN_LED_IND = 2

    def __init__(self, red_led_pin_num, yellow_led_pin_num, green_led_pin_num):
        self.red_led = Pin(red_led_pin_num, Pin.OUT)
        self.yellow_led = Pin(yellow_led_pin_num, Pin.OUT)
        self.green_led = Pin(green_led_pin_num, Pin.OUT)

        self.leds = (self.red_led, self.yellow_led, self.green_led)

        self._current_led_ind = 2 # so that first call will light up the red led

    def run(self):
        '''
        runs the Traffic lights
        '''
        #TODO: Apparently on the esp32-cam. Using the Timer invokes the wdt for some reason
        #       I tried timer ids 0-3, all of them invoke this error and reset the chip

        # Guru Meditation Error: Core  1 panic'ed (Interrupt wdt timeout on CPU1).

        # Core  1 register dump:
        # PC      : 0x40092543  PS      : 0x00060034  A0      : 0x80091d21  A1      : 0x3ffb1190
        # A2      : 0x3ffb1238  A3      : 0x3ffb36f4  A4      : 0x3ffb36ec  A5      : 0x00060021
        # A6      : 0x0000abab  A7      : 0xb33fffff  A8      : 0x3ffb36f4  A9      : 0x00000000
        # A10     : 0x00000004  A11     : 0x00060023  A12     : 0x00060021  A13     : 0x3ffbcaa0
        # A14     : 0x00000000  A15     : 0x3ffb3760  SAR     : 0x0000001d  EXCCAUSE: 0x00000006
        # EXCVADDR: 0x00000000  LBEG    : 0x00000000  LEND    : 0x00000000  LCOUNT  : 0x00000000
        # Core  1 was running in ISR context:
        # EPC1    : 0x400d2fcb  EPC2    : 0x00000000  EPC3    : 0x00000000  EPC4    : 0x40092543


        # Backtrace:0x40092540:0x3ffb11900x40091d1e:0x3ffb11b0 0x400d6bc1:0x3ffb11d0 0x400d6c47:0x3ffb1200 0x40083d19:0x3ffb1220 0x4000bfed:0x3ffbca50 0x4011ec92:0x3ffbca60 0x400d2b7d:0x3ffbca80 0x40090574:0x3ffbcaa0


        # Core  0 register dump:
        # PC      : 0x40191d92  PS      : 0x00060734  A0      : 0x800d2b86  A1      : 0x3ffbc300
        # A2      : 0x3ffb4a48  A3      : 0x00060720  A4      : 0x8008a07a  A5      : 0x3ffb0bc0
        # A6      : 0x3ffb1420  A7      : 0x3ffb48a4  A8      : 0x8011ec95  A9      : 0x3ffbc2f0
        # A10     : 0x00000003  A11     : 0x00060723  A12     : 0x00060720  A13     : 0x3ffccce0
        # A14     : 0x00000003  A15     : 0x00060023  SAR     : 0x0000001d  EXCCAUSE: 0x00000006
        # EXCVADDR: 0x00000000  LBEG    : 0x00000000  LEND    : 0x00000000  LCOUNT  : 0x00000000


        # Backtrace:0x40191d8f:0x3ffbc3000x400d2b83:0x3ffbc320 0x40090574:0x3ffbc340

        # ELF file SHA256: 1fb92b2bca51293c


        self.timer = Timer(3) 
        self.timer.init(period=self.DEFAULT_TIME_IN_BETWEEN, mode=Timer.PERIODIC, callback=self.next_light)

    def stop(self):
        '''
        stops the traffic lights
        '''
        self.timer.deinit()

    def next_light(self, t):
        '''
        function to close the previous light and open the next light in order (red, yellow, green)

        param t is for the timer module
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


