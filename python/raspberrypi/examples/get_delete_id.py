'''!
@file get_delete_id.py
@brief This routine implements user lookup and deletion on Raspberry Pi 5/4 (pyserial).
@details This routine sends string commands over terminal to the host controller
@n which parses and executes the corresponding actions on the module.
@n Supported commands: 1 (get number of users), 2 (delete user by ID), and 3 (delete all users).
@copyright   Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
@license     The MIT License (MIT)
@author      [Olive](feng.yang@dfrobot.com)
@version     V1.0.0
@date        2026-06-02
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
    first_run = True
    while True:
      # Determine whether the module is ready
      while not bio.check_state():
        print(" Module not ready !")
        time.sleep(0.2)
      # The module is ready, only print the message at the first time
      if first_run:
        print(" Module ready !")
        # Command Introduction
        print("-----------------------------")
        print("Enter the command below through the serial port:")
        print("1          # Get all user information")
        print("2          # Delete the specified user")
        print("3          # Delete all users")
        print("-----------------------------")
        first_run = False

      try:
        cmd = input().strip()
      except EOFError:
        cmd = ""

      if not cmd:
        time.sleep(0.1)
        continue

      # Match the command of user
      if cmd == "1":
        face_count = bio.get_all_nums_face_user_ids()
        print(f"face user nums:{face_count}")
        time.sleep(0.1)
        id_buffer = [0] * 50
        bio.get_all_face_user_ids(id_buffer, 50)
        if face_count > 0:
          face_ids = [str(id_buffer[i]) for i in range(face_count)]
          print(f"face user ids:{' '.join(face_ids)}")
          time.sleep(0.1)
        palm_count = bio.get_all_nums_palm_user_ids()
        print(f"palm user nums:{palm_count}")
      elif cmd == "2":
        print("input the id that you delete:")
        try:
          id_str = input().strip()
        except EOFError:
          id_str = ""
        if not id_str or not id_str.isdigit():
          print("Invalid ID")
        else:
          user_id = int(id_str)
          if user_id <= 500:
            face_count = bio.get_all_nums_face_user_ids()
            id_buffer = [0] * 50
            bio.get_all_face_user_ids(id_buffer, 50)
            id_exists = False
            for idx in range(face_count):
              if user_id == id_buffer[idx]:
                id_exists = True
            if id_exists:
              result = bio.delete_user(user_id)
              if result == 1:
                print(f"Successful delete user:{user_id}")
              else:
                print("Failed to delete user")
            else:
              print("The user with this ID does not exist")
          elif user_id > 500 and user_id <= 800:
            result = bio.delete_user(user_id)
            if result == 1:
              print(f"Successful delete user:{user_id}")
            else:
              print("Failed to delete user")
          else:
            print("The user with this ID does not exist")
      elif cmd == "3":
        result = bio.delete_all_user()
        if result == 1:
          print("Successful delete all user")
        else:
          print("Failed to delete all user")
      else:
        print("ERROR command")
      print()
      print("please input next command:")
      time.sleep(1)
  except KeyboardInterrupt:
    pass
  finally:
    bio.close()


if __name__ == "__main__":
  main()
