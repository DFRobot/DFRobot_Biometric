'''!
@file sen0737_special.py
@brief the example show some function that SEN0737 Independently owned on Raspberry Pi 5/4 (pyserial).
@details When an object is detected, the module automatically starts recognition.
@n The light is off when idle, turns white during recognition, green upon success, and red upon failure
@copyright   Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
@license     The MIT License (MIT)
@author      [Olive](feng.yang@dfrobot.com)
@version     V1.0.0
@date        2026-05-10
@url         https://github.com/DFRobot/DFRobot_Biometric
'''

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DFRobot_Biometric import DFRobot_Biometric, SId
from gpiozero import DigitalInputDevice

# Use BCM encoding
IR_PIN = 25


def main():
  bio = DFRobot_Biometric(port='/dev/serial0', baudrate=115200)
  ir_sensor = None
  try:
    # Use BCM encoding
    ir_sensor = DigitalInputDevice(IR_PIN, pull_up=False)
    time.sleep(1.5)
    first_run = True
    while True:
      # Determine whether the module is ready
      while not bio.check_state():
        print(" Module not ready !")
        time.sleep(0.2)
      # The module is ready, only print the message at the first time
      if first_run:
        print(" Module ready !")
        print("-------------------------------------------------------------------------------")
        first_run = False

      # Power-on and normal state
      bio.led_color(bio.COLOR_WHITE, bio.LED_OFF)
      bio.led_color(bio.COLOR_RED, bio.LED_OFF)
      bio.led_color(bio.COLOR_GREEN, bio.LED_OFF)
      while not ir_sensor.is_active:
        time.sleep(0.5)

      # Object detected: the white light indicates the detection state
      bio.led_color(bio.COLOR_GREEN, bio.LED_OFF)
      bio.led_color(bio.COLOR_WHITE, bio.LED_ON)
      bio.led_color(bio.COLOR_RED, bio.LED_OFF)
      my_sid = SId()
      print("Start recognition. Face the camera directly. Palm vein: 10-20cm, Face: 20-90cm")
      result = bio.get_recognition_result(my_sid)
      # Determine the execution result
      if result == 1:
        bio.led_color(bio.COLOR_GREEN, bio.LED_ON)
        bio.led_color(bio.COLOR_RED, bio.LED_OFF)
        bio.led_color(bio.COLOR_WHITE, bio.LED_OFF)
        print("Success! This is information of the user:")
        print(f"id:{my_sid.id}")
        print(f"userName:{my_sid.user_name}")
        print("user kind:", end="")
        if my_sid.kind == bio.FACE_USER:
          print("face user")
        elif my_sid.kind == bio.PALM_USER:
          print("palm user")
        print("userClass:", end="")
        if my_sid.is_admin == bio.ROLE_ADMIN:
          print("Administrator")
        else:
          print("Normal user")
        time.sleep(2)
      elif result == 2:
        print("User recognition timeout")
      elif result == bio.NO_ACK:
        print("No response from module")
      elif result == 3:
        print("Recognized user not found")
      if result != 1:
        bio.led_color(bio.COLOR_GREEN, bio.LED_OFF)
        bio.led_color(bio.COLOR_RED, bio.LED_ON)
        bio.led_color(bio.COLOR_WHITE, bio.LED_OFF)
        time.sleep(2)
      print("-------------------------------------------------------------------------------")
      print()
  except KeyboardInterrupt:
    pass
  finally:
    bio.close()
    if ir_sensor is not None:
      ir_sensor.close()


if __name__ == "__main__":
  main()
