'''
Traffic Simulator System:
    1- host web app and get photo picture when prompted
    2- control traffic lights (3 LEDs)
    3- Read Proximity Sensor to detect car movement
'''
from time import sleep, sleep_ms
from actuators import Actuators
from sensors import Sensors
from server import Server
import camera

def main():
    '''
    Main Routine
    '''
    sleep(4)

    try:
        actuators = Actuators()
        sensors = Sensors()
        server = Server()
        camera.init()

        actuators.traffic_lights.flash_all()
        print("\nAll System Components Up and running!!\n")

        while True:
            
            actuators.traffic_lights.next_light('tmp')
            print(f"Current Traffic Light: {actuators.traffic_lights._current_led_ind}")

            if sensors.proximity_sensor.state and actuators.traffic_lights._current_led_ind == 0:
                # Capture Image
                img = camera.capture()
                print(f"Picture Captured, len: {len(img)}")

                # Send to Server
                server.socket_connect()
                response = server.socket_send_data(img)
                server.socket_disconnect()
                print(f"Sent!, Response: {response}")

                print("Proximity Detected in Red Lights!!\n")

            sleep(1)

    except Exception as e:
        print(f"Caught {e}")

    finally:
        camera.deinit()
        actuators.traffic_lights.stop()
        server.socket_disconnect()

