'''!
@file enrollUser.py
@brief Example of face or palm user enrollment on Raspberry Pi 5/4 (pyserial).
@details This example performs user enrollment every time the board is reset,
@n and prints the enrollment result through the terminal
@n Enrollment should work normally as long as the connection is correct
@copyright   Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
@license     The MIT License (MIT)
@author      [Olive](feng.yang@dfrobot.com)
@version     V1.0.0
@date        2026-05-10
@url         https://github.com/DFRobot/DFRobot_Biometric
'''

import serial
import time
from DFRobot_Biometric import DFRobot_Biometric, SId

if __name__ == "__main__":
  bio = DFRobot_Biometric(port='/dev/serial0', baudrate=115200)  # Initialize the class object and pass in a serial port
  try:
    print("------------------------------------------------")
    print("Start connect Module...")
    # Determine whether the module is ready
    while not bio.check_state():
      print("Connection Module Fail")
    print(" Module is ready")
    print("Starting to enroll:")
    # Initialize the registered user information
    user_kind = bio.PALM_USER
    name = "zwjhy"
    kind_class = bio.ROLE_NORMAL

    result, id = bio.enroll_user(user_kind, name, kind_class)
    if result == 1:
      print("enroll success !")
      print(f"the id is: {id}")
      print(f"the name is: {name}")
      if user_kind == bio.PALM_USER:
        print("the user kind is : PALM")
      else:
        print("the user kind is : FACE")
      if kind_class == bio.ROLE_NORMAL:
        print("the user class is : NORMAL USER")
      elif kind_class == bio.ROLE_ADMIN:
        print("the user class is : ADMINER")
    elif result == 2:
      print("face duplicate")
    elif result == 3:
      print("Enrollment timeout")
    elif result == bio.ERROR:
      print("parameter error")
    else:
      print("Unknown error")
    print("------------------------------------------------")
    print("")
    time.sleep(2)
  except KeyboardInterrupt:
    print("\n user stop the program")

  except Exception as e:
    print(f"err: {e}")

  finally:
    bio.close()
    print("the serial is closed safely")
