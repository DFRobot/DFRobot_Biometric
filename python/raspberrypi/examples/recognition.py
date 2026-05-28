'''!
@file recognition.py
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

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DFRobot_Biometric import DFRobot_Biometric, SId


def main():
  bio = DFRobot_Biometric(port='/dev/serial0', baudrate=115200)
  try:
    while True:
      # Determine whether the module is ready
      while not bio.check_state():
        print("Module not ready !")
        time.sleep(0.2)
      print("Module ready!")
      print("-------------------------------------------------------------------------------")
      my_sid = SId()
      print("Start recognition. Face the camera directly. Palm vein: 10-20cm, Face: 20-90cm")
      result = bio.get_recognition_result(my_sid)
      # Determine the execution result
      if result == 1:
        print("Success! The imformation of the user:")
        print(f"id:{my_sid.id}")
        print(f"userName:{my_sid.user_name}")
        print("user kind:", end="")
        if my_sid.kind == bio.FACE_USER:
          print("face user")
        elif my_sid.kind == bio.PALM_USER:
          print("palm user")
        print("userClass:", end="")
        if my_sid.is_admin == bio.ROLE_NORMAL:
          print("Normal user")
        elif my_sid.is_admin == bio.ROLE_ADMIN:
          print("Adminer")
      elif result == 2:
        print("User recognition timeout")
      elif result == bio.NO_ACK:
        print("No response from module")
      elif result == 3:
        print("Recognized user not found")
      print("-------------------------------------------------------------------------------")
      print()
      time.sleep(10)
  except KeyboardInterrupt:
    pass
  finally:
    bio.close()


if __name__ == "__main__":
  main()
