'''!
@file SEN0736_get_delete_id.py
@brief This routine implements user lookup and deletion on Raspberry Pi 5/4 (pyserial).
@details This routine sends string commands over terminal to the host controller
@n which parses and executes the corresponding actions on the module.
@n Supported commands: AT+GETUSERS (get number of users), AT+DELUSER=<ID> (delete user by ID), and AT+DELALLUSERS (delete all users).
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
    # Determine whether the module is ready
    while not bio.check_state():
      print("Connection Module Fail")
    # Command Introduction
    print("Module is ready")
    print("-----------------------------")
    print("Available commands:")
    print("AT+GETUSERS       # Get all user information")
    print("AT+DELUSER=ID     # Delete the specified user (e.g. AT+DELUSER=250)")
    print("AT+DELALLUSERS    # Delete all users")
    print("-----------------------------")
    while True:
      try:
        cmd = input("Please enter command : ").strip()
      except EOFError:
        cmd = ""
      if not cmd:
        time.sleep(0.1)
        continue
      data = cmd.encode()

      # Match the command of user
      if data == b"AT+GETUSERS":
        nums = bio.get_all_nums_face_user_ids()
        print(f"face user nums: {nums}")
        id_buffer = [0] * 50
        bio.get_all_face_user_ids(id_buffer, 50)
        # Print all face ids on the same line, separated by a single space (decimal)
        face_ids = [str(id_buffer[i]) for i in range(nums)]
        print(f"face user ids: " + ' '.join(face_ids))
        nums = bio.get_all_nums_palm_user_ids()
        print(f"palm user nums: {nums}")
      elif data == b"AT+DELALLUSERS":
        result = bio.delete_all_user()
        if result == 1:
          print("Successful delete all users")
        else:
          print("Fail")
      elif data.startswith(b"AT+DELUSER="):
        user_id = data.split(b"=")[1]
        result = bio.delete_user(int(user_id))
        if result == 1:
          print(f"Successful delete user:{user_id.decode()}")
        else:
          print("Fail")
      else:
        print("Unknown command")
      time.sleep(0.5)
      print("")

  except KeyboardInterrupt:
    print("\n user stop the program")

  except Exception as e:
    print(f"err: {e}")

  finally:
    bio.close()
    print("the serial is closed safely")
