'''
Abstraction to all actuators in the system
'''
from micropython import const
from traffic_lights import TrafficLight
from motor import DCMotor

class Actuators:
    '''
    Object to control all actuators in the system
    '''
    RED_LED_PIN_NUM = const(12)
    YELLOW_LED_PIN_NUM = const(13)
    GREEN_LED_PIN_NUM = const(15)

    MOTOR_PWM_PIN_NUM = const(14)
    MOTOR_DIR_PIN_NUM = const(2)
    def __init__(self):
        self.traffic_lights = TrafficLight(RED_LED_PIN_NUM, YELLOW_LED_PIN_NUM, GREEN_LED_PIN_NUM)
        self.motor = DCMotor(MOTOR_PWM_PIN_NUM, MOTOR_DIR_PIN_NUM)


