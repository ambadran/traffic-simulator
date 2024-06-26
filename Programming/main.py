'''
Traffic Simulator System:
    1- host web app and get photo picture when prompted
    2- control traffic lights (3 LEDs)
    3- Read Proximity Sensor to detect car movement
'''
from time import sleep, sleep_ms
from actuators import Actuators
from sensors import Sensors
import camera
# from server import server

def main():
    '''
    Main Routine
    '''
    ### Inits ###
    actuators = Actuators()
    sensors = Sensors()
    # server = Server()

    print("All System Components UP")

# sleep(3)

try:
    actuators = Actuators()
    sensors = Sensors()
    camera.init()

except Exception as e:
    print(f"Caught {e}")

finally:
    camera.deinit()


