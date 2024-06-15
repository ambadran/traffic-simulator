'''
Traffic Simulator System:
    1- host web app and get photo picture when prompted
    2- control traffic lights (3 LEDs)
    3- Read Proximity Sensor to detect car movement
'''
from micropython import const
from machine import Pin, Timer, ADC, PWM
from server import server
from proximity_sensor import ProximitySensor
from traffic_lights import TrafficLight
import camera

POT_PIN_NUM = const()
SWITCH_PIN_NUM = const()
RED_LED_PIN_NUM = const()
YELLOW_LED_PIN_NUM = const()
GREEN_LED_PIN_NUM = const()
PROXIMITY_SENSOR_PIN_NUM = const()
MOTOR_PWM_PIN_NUM = const()

def main():
    '''
    Main Routine
    '''
    # Object Initiations
    pot = ADC(POT_PIN_NUM)
    motor_pwm = PWM(Pin(MOTOR_PWM_PIN_NUM))
    switch = Pin(SWITCH_PIN_NUM, Pin.IN)
    traffic_lights = TrafficLight(RED_LED_PIN_NUM, YELLOW_LED_PIN_NUM, GREEN_LED_PIN_NUM)
    proximity_sensor = ProximitySensor(PROXIMITY_SENSOR_PIN_NUM)

    if not camera.init():
        #TODO: show user something is wrong!!!
        pass

    # The switch determines auto state or user controlled state
    if switch.value():
        # Auto MODE
        timer = 
        # while True:
        #TODO: init a timer and call traffic_lights.next_light()
        #TODO: take value from POT and output PWM

    else:
        # Manual Mode
        while True:

            try:

                server.wait_for_client()

                html_request_full = server.get_html_request()
                print(f"HTML Request: {html_request_full}")

                if html_request_full:
                    # html_request, pin_id, pin_value = html_request_full

                    # switch_values = [b'on', b'off']

                    # if html_request == HTML_REQUEST.GET_SENSOR_ACTUATOR:
                    #     values = sensors.all_values
                    #     values.extend(actuators.all_values)
                    #     server.handle_get_values(values)

                    # elif html_request == HTML_REQUEST.POST_SWITCH:
                    #     print("TODO:")

                    # elif html_request == HTML_REQUEST.GET_WEB:
                    #     values = None
                    #     server.handle_get_web(values)

                    # else:
                    #     raise ValueError("HOW THE FUCK?!?!")

                else:
                    server.client.close()


            except Exception as e:
                print(f"Error in Main Server Loop: {e}")



