'''!
@file SEN0736_Recognition.py
@brief Continuous automatic user recognition routine on Raspberry Pi 5/4 (pyserial).
@details This routine periodically detects faces, automatically recognizes them
@n and prints user details to the terminal.
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
    while True:
      print("------------------------------------------------")
      print("Start connect Module...")
      # Determine whether the module is ready
      while not bio.check_state():
        print("Connection Module Fail")
      print("Module is ready")
      my_sid = SId()  # Create an SId object to store the recognition result
      result = bio.get_recognition_result(my_sid)
      if result == 1:
        print("Recognition successful")
        print("the information of user:")
        print(f"{my_sid}")
      elif result == 2:
        print("Recognition timeout")
      elif result == 3:
        print("User not found")
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
