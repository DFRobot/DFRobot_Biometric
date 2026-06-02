# DFRobot_Biometric
- [中文版](./README_CN.md)

The FP001 and FP002 are face and palm vein recognition modules equipped with a bionic face recognition algorithm. They support UVC/UAC transmission and MJPEG video format, achieving both security and a good user experience. Featuring low power consumption, low cost, fast recognition, exquisite appearance, and compact structure, these modules utilize high-performance chips to quickly complete the entire process of face recognition and palm vein recognition.

The Biometric library uniformly encapsulates the functions of the SEN0736 and SEN0737 modules. Both modules support face enrollment, recognition, user query, and user deletion. The SEN0737 additionally features a three-color indicator, with control functions encapsulated for each color. Algorithms run on the modules. This library handles command interaction—sending commands, receiving feedback, and ensuring timely responses。




<table align="center">
  <tr>
    <td><img src="./resources/images/SEN0736_black.png" ></td>
    <td><img src="./resources/images/SEN0736_white.png" ></td>
    <td><img src="./resources/images/SEN0737.png"       ></td>
  </tr>
  <tr>
    <td><img src="./resources/images/SEN0736_use.png"   ></td>
    <td><img src="./resources/images/SEN0737_use.png"   ></td>
  </tr>
</table>


## Product Link (www.dfrobot.com)
    SKU: SEN0736 FP001 and SEN0737 FP002 Face and Palm Vein Recognition Modules

## Table of Contents

  * [Summary](#summary)
  * [Installation](#installation)
  * [Methods](#methods)
  * [Compatibility](#compatibility)
  * [History](#history)
  * [Credits](#credits)

## Summary

Introduce the basic and special functions of this Arduino Library.

## Installation

To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++
  /**
   * @fn checkState
   * @brief Check if the module is ready and idle
   * @return bool type
   * @retval true Module is ready
   * @retval false Module is not ready
   * @note Use checkState() to check status before initialization or executing commands
   */
  bool checkState(void);

  /**
   * @fn enrollUser
   * @brief Enroll face or palm for recognition
   * @details Ensure that the parameters meet the requirements.
   * @param kind eFaceUser for face enrollment, ePalmUser for palm enrollment
   * @param userName User name, length 1 to 32 characters
   * @param id Store the enrolled user ID, range 1 to 800
   * @param idAdmin Set user role, eRoleAdmin for administrator, eRoleNormal
   * @return Task execution result
   * @retval NO_ACK -1 No response from module
   * @retval ERROR  -2 User parameter error, such as invalid user type or name length
   * @retval 1 Success
   * @retval 2 Duplicate
   * @retval 3 Enrollment timeout
   */
  int8_t enrollUser(eUserKind_t kind, const char* userName, uint16_t* id, eIsAdmin_t idAdmin);

  /**
   * @fn getAllNumsFaceUserIDs
   * @brief Get the number of face users
   * @return Number of face users
   * @retval NO_ACK -1 No response from module
   */
  int16_t getAllNumsFaceUserIDs(void);

  /**
   * @fn getAllNumsPalmUserIDs
   * @brief Get the number of palm users
   * @return Number of palm users
   * @retval NO_ACK -1 No response from module
   */
  int16_t getAllNumsPalmUserIDs(void);

  /**
   * @fn getAllFaceUserIDs
   * @brief Retrieve the specific information of the face user
   * @param id_buffer store the specific information of the face user
   * @param length the length of the id_buffer
   * @return result
   * @retval NO_ACK -1 No response from module
   * @retval ERROR  -2 User parameter error:The length of the incoming array is less than the number of users.
   */
  int8_t getAllFaceUserIDs(uint16_t *id_buffer,uint16_t length);

  /**
   * @fn getRecognitionResult
   * @brief Recognize the user
   * @param ID Store the recognized user information
   * @return Execution result
   * @retval NO_ACK -1 No response from module
   * @retval 1 Success
   * @retval 2 Timeout
   * @retval 3 User not found
   */
  int8_t getRecognitionResult(sId_t* ID);

  /**
   * @fn deleteUser
   * @brief Delete specified user
   * @details The ID must fall within the valid range
   * @param id User ID, range 1 to 800
   * @return Delete result
   * @retval NO_ACK -1 No response from module
   * @retval ERROR  -2 ID out of range 1 to 800
   * @retval 1 Delete success
   * @retval 2 User not found
   * @retval 3 Unknown error, suggest retry
   */
  int8_t deleteUser(uint16_t id);

  /**
   * @fn deleteAllUser
   * @brief Delete all users
   * @return Delete result
   * @retval NO_ACK -1 No response from module
   * @retval 1 Delete success
   * @retval 2 Unknown error, suggest retry
   */
  int8_t deleteAllUser(void);

  /**
   * @fn ledColor
   * @brief Control LED status
   * @details Ensure that the parameters meet the requirements
   * @param color LED color: COLOR_GREEN green, COLOR_RED red, COLOR_WHITE white
   * @param kind LED_ON turn on, LED_OFF turn off
   * @return Execution result
   * @retval NO_ACK -1 No response from module
   * @retval ERROR -2 Invalid kind or color parameter
   * @retval 1 Success
   */
  int8_t ledColor(uint8_t color, uint8_t kind);
```

## Compatibility

| MCU                | Work Well | Work Wrong | Untested | Remarks |
| ------------------ | :--------: | :--------: | :------: | ------- |
| Arduino Uno        |          |     √    |         |     unstable        |
| Arduino Leonardo   |    √     |          |         |                     |
| Arduino MEGA2560   |    √     |          |         |                     |
| FireBeetle-ESP32   |    √     |          |         |                     |
| ESP8266            |    √     |          |         |                     |
| FireBeetle-M0      |    √     |          |         |                     |
| Micro:bit          |          |    √     |         |                     |


## History

- 2026/06/02 - Version 1.0.0 released.

## Credits

Written by Olive-hy(feng.yang@dfrobot.com), 2026-6-02 (Welcome to our [website](https://www.dfrobot.com/))
