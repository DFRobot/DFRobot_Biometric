'''!
@file enroll_user.py
@brief Example of face or palm user enrollment on Raspberry Pi 5/4 (pyserial).
@details This example performs user enrollment every time you input the command:1 (enroll face),2 (enroll palm)
@n and prints the enrollment result through the terminal
@n Enrollment should work normally as long as the connection is correct
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

from DFRobot_Biometric import DFRobot_Biometric


def main():
  bio = DFRobot_Biometric(port='/dev/serial0', baudrate=115200)
  try:
    # Determine whether the module is ready
    while not bio.check_state():
      print("Module not ready!")
      time.sleep(0.2)
    print("Module ready!")
    print("----------------------------------------------------")
    print("Enter the command below through the serial port:")
    print("1     # enroll face user")
    print("2     # enroll palm user")
    print("----------------------------------------------------")

    face_name = "face"
    palm_name = "palm"
    user_class = bio.ROLE_NORMAL
    face_count = 1
    palm_count = 1

    while True:
      try:
        cmd = input().strip()
      except EOFError:
        cmd = ""

      if not cmd:
        time.sleep(0.1)
        continue

      print("-----------------------------------------------------------------------------------------------")
      if cmd == "1" or cmd == "2":
        if cmd == "1":
          print("Start face enrollment. Please keep your face directly facing the camera, 30cm~60cm away")
          full_name = f"{face_name}{face_count}"
          user_kind = bio.FACE_USER
          result, user_id = bio.enroll_user(user_kind, full_name, user_class)
        else:
          print("Start palm enrollment. Please keep your face directly facing the camera, 15cm~20cm away")
          full_name = f"{palm_name}{palm_count}"
          user_kind = bio.PALM_USER
          result, user_id = bio.enroll_user(user_kind, full_name, user_class)

        # Determine the execution result
        if result == 1:
          if cmd == "1":
            print("Face enrollment successful!")
          else:
            print("Palm enrollment successful!")
          print(f"the user id is:{user_id}")
          print(f"the user name is:{full_name}")
          print("the user kind is:", end="")
          if user_kind == bio.FACE_USER:
            print("face user")
          elif user_kind == bio.PALM_USER:
            print("palm user")
          print("the userClass is:", end="")
          if user_class == bio.ROLE_NORMAL:
            print("Normal user")
          elif user_class == bio.ROLE_ADMIN:
            print("Adminer")
          if cmd == "1":
            face_count += 1
          else:
            palm_count += 1
        elif result == 2:
          print("User already exists")
        elif result == 3:
          print("Enrollment timeout")
        elif result == bio.NO_ACK:
          print("No response from module")
        elif result == bio.ERROR:
          print("Parameter range error")
      else:
        print("Error command!")
      print("-----------------------------------------------------------------------------------------------")
      print()
      print("please input next command:")
      time.sleep(2)
  except KeyboardInterrupt:
    pass
  finally:
    bio.close()


if __name__ == "__main__":
  main()
