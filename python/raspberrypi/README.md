# DFRobot_Biometric

- [中文版](./README_CN.md)

The FP001 and FP002 are face and palm vein recognition modules equipped with a bionic face recognition algorithm. They support UVC/UAC transmission and MJPEG video format, achieving both security and a good user experience. Featuring low power consumption, low cost, fast recognition, exquisite appearance, and compact structure, these modules utilize high-performance chips to quickly complete the entire process of face recognition and palm vein recognition.

The Biometric library uniformly encapsulates the functions of the SEN0736 and SEN0737 modules. Both modules support face enrollment, recognition, user query, and user deletion. The SEN0737 additionally features a three-color indicator, with control functions encapsulated for each color. Algorithms run on the modules. This library handles command interaction—sending commands, receiving feedback, and ensuring timely responses.



<table align="center">
  <tr>
    <td><img src="../../resources/images/SEN0736_black.png" ></td>
    <td><img src="../../resources/images/SEN0736_white.png" ></td>
    <td><img src="../../resources/images/SEN0737.png"       ></td>
  </tr>
  <tr>
    <td><img src="../../resources/images/SEN0736_use.png"   ></td>
    <td><img src="../../resources/images/SEN0737_use.png"   ></td>
  </tr>
</table>


## Product Link (Link to DFRobot store)
    SKU: SEN0736 FP001 and SEN0737 FP002 Face and Palm Vein Recognition Modules

## Table of Contents

  * [Summary](#summary)
  * [Installation](#installation)
  * [Methods](#methods)
  * [Compatibility](#compatibility)
  * [History](#history)
  * [Credits](#credits)

## Summary

Introduce the basic and special functions of this python Library.

## Installation

To use this library, first download the library to your Raspberry Pi, then navigate to the examples folder. To run an example script, such as demox.py, type python demox.py in the command line. For example, to run the enrollUser.py example, you would enter:

```python
python enroll_user.py
```



## Methods

```python
  '''!
      @brief Check module is ready and idle
      @return bool True if module ready
      @retval True module ready
      @retval False module not ready
    '''
  def check_state(self):

  '''!
      @brief Get number of palm users
      @return int Count on success
      @retval nums>0 collect Number of palm users
      @retval NO_ACK no response
    '''
  def get_all_nums_palm_user_ids(self):

  '''!
      @brief Get number of face users
      @return int Count on success
      @retval nums>0 collect Number of face users
      @retval NO_ACK no response
    '''
  def get_all_nums_face_user_ids(self):

  '''!
      @brief Get specific face user IDs
      @param id_buffer writable sequence to receive face IDs
      @param length int Maximum number of IDs the buffer can hold
      @return int RESULT_OK on success, ERROR when buffer is too small, NO_ACK no response
    '''
  def get_all_face_user_ids(self, id_buffer, length):

  '''!
      @brief Enroll face or palm
      @param kind FACE_USER or PALM_USER
      @param user_name str 1~32 characters
      @param is_admin ROLE_NORMAL or ROLE_ADMIN
      @return tuple (retval, new_id) retval: 1 success, 2 duplicate, 3 timeout, NO_ACK is no response, ERROR parameter error; new_id int or None
    '''
  def enroll_user(self, kind, user_name, is_admin):

  '''!
      @brief Identify user; fills sid on success
      @param sid SId instance to fill
      @return the result
      @retval  1 success,2 timeout,3 not found,NO_ACK no response,ERROR parameter error
    '''
  def get_recognition_result(self, sid):

  '''!
      @brief Delete user by id (same bounds and branches as C++: 1~800)
      @param user_id int
      @return the result
      @retval  1 success,2 not found,3 unknow err,NO_ACK no response,ERROR parameter error
    '''
  def delete_user(self, user_id):

    '''!
      @brief Delete all users
      @return the result
      @retval  1 success,2 unknown err,NO_ACK no response
    '''
  def delete_all_user(self):

    '''!
      @brief LED color on/off
      @param color COLOR_GREEN, COLOR_RED, COLOR_WHITE
      @param kind LED_ON or LED_OFF
      @return the result
      @retval  1 success,NO_ACK no response,ERROR parameter error
    '''
  def led_color(self, color, kind):

    '''!
      @brief Close serial port
    '''
  def close(self):
```

## Compatibility

* RaspberryPi Version

| Board        | Work Well | Work Wrong | Untested | Remarks |
| ------------ | :-------: | :--------: | :------: | ------- |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |
| RaspberryPi5 |     √     |            |          |         |

* Python Version

| Python  | Work Well | Work Wrong | Untested | Remarks |
| ------- | :-------: | :--------: | :------: | ------- |
| Python2 |           |            |    √     |         |
| Python3 |     √     |            |          |         |

## History

- 2026/05/22 - Version 1.0.0 released.

## Credits

Written by Olive-hy(feng.yang@dfrobot.com), 2026-5-11 (Welcome to our [website](https://www.dfrobot.com/))
