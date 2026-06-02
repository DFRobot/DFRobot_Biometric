/*!
 * @file DFRobot_Biometric.cpp
 * @brief Define the implementation of DFRobot_Biometric class
 * @details   This is Biometric sensor that can be controlled through USART port.
 * @copyright	Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license   The MIT License (MIT)
 * @author    [Olive](feng.yang@dfrobot.com)
 * @version   V1.0.0
 * @date      2026-06-02
 * @url       https://github.com/DFRobot/DFRobot_Biometric
 */
#include "DFRobot_Biometric.h"

#include <Arduino.h>
#include <string.h>
DFRobot_Biometric::DFRobot_Biometric(Stream& serial) : _serial(serial) {}

bool DFRobot_Biometric::checkState(void)
{
  bool    state       = false;
  uint8_t data[6]     = CMD_CHECK_STATE;
  uint8_t buffer[250] = { 0 };
  state               = writeCmd(data, 6, buffer, 2000);
  if (state == true) {
    if (buffer[7] == STATUS_STANDBY) {
      return true;
    }
  }
  return false;
}

void DFRobot_Biometric::calculateChecksum(uint8_t* data, uint8_t len)
{
  uint8_t checkSum = 0;
  for (uint8_t i = 2; i < len - 1; i++) {
    checkSum ^= data[i];
  }
  //Write checksum value
  data[len - 1] = checkSum;
}

int16_t DFRobot_Biometric::getAllNumsFaceUserIDs(void)
{
  uint8_t data[7]     = CMD_GET_FACE_USER_NUMS;
  bool    state       = false;
  int16_t nums        = 0;
  uint8_t buffer[250] = { 0 };
  state               = writeCmd(data, 7, buffer, 1000);
  if (state == true) {
    nums = buffer[7] * 256 + buffer[8];
    return nums;
  }
  return NO_ACK;
}

int16_t DFRobot_Biometric::getAllNumsPalmUserIDs(void)
{
  uint8_t data[7]     = CMD_GET_PALM_USER_NUMS;
  bool    state       = false;
  int16_t nums        = 0;
  uint8_t buffer[250] = { 0 };
  state               = writeCmd(data, 7, buffer, 1000);
  if (state == true) {
    nums = buffer[7] * 256 + buffer[8];
    return nums;
  }
  return NO_ACK;
}

int8_t DFRobot_Biometric::getAllFaceUserIDs(uint16_t* id_buffer, uint16_t length)
{
  uint8_t  data[7]     = CMD_GET_FACE_USER_SPECIFIC;
  bool     state       = false;
  uint8_t  buffer[250] = { 0 };
  uint16_t userNums    = 0;
  state                = writeCmd(data, 7, buffer, 3000);
  if (state == true) {
    userNums = buffer[7] * 256 + buffer[8];
    if (length < userNums) {
      return ERROR;
    }
    for (uint16_t i = 0; i < userNums; i++) {
      id_buffer[i] = buffer[9 + i * 2] * 256 + buffer[9 + i * 2 + 1];
    }
    return RESULT_OK;
  }
  return NO_ACK;
}

bool DFRobot_Biometric::waitForReply(uint8_t* buffer, uint16_t timeout)
{
  uint16_t recmdLen = 0, bufLen = 0;
  uint8_t  recData   = 0;
  uint32_t startTime = millis();
  while (millis() - startTime < timeout) {
    yield();
    if (_serial.available()) {
      recData = _serial.read();
      if (bufLen < 3) {
        if (recData == 0xEF && bufLen == 0) {
          buffer[bufLen++] = recData;
        } else if (recData == 0xAA && bufLen == 1) {
          buffer[bufLen++] = recData;
        } else if (recData == 0x00 && bufLen == 2) {
          buffer[bufLen++] = recData;
        } else if (recData == 0x01 && bufLen == 2) {
          bufLen = 0;
        } else {
          bufLen = 0;
        }
      } else {
        if (bufLen == 3) {
          buffer[bufLen++] = recData;
        } else if (bufLen == 4) {
          buffer[bufLen++] = recData;
          recmdLen         = buffer[3] * 256 + buffer[4];
          if (recmdLen > 220) {
            return false;
          }
        } else if (bufLen > 4 && bufLen <= (4 + recmdLen)) {
          buffer[bufLen++] = recData;
        } else if (bufLen == (5 + recmdLen)) {
          calculateChecksum(buffer, bufLen + 1);
          if (recData == buffer[bufLen]) {
            serialEmpty();
            return true;
          }
        }
      }
    }
  }
  return false;
}

int8_t DFRobot_Biometric::enrollUser(eUserKind_t kind, const char* userName, uint16_t* id, eIsAdmin_t isAdmin)
{
  uint8_t nameLen = strlen(userName);
  //Check name length
  if (nameLen > 32 || nameLen == 0) {
    return ERROR;
  }
  //Check user type
  if (kind != eFaceUser && kind != ePalmUser) {
    return ERROR;
  }
  //Check user type
  if (isAdmin != eRoleNormal && isAdmin != eRoleAdmin) {
    return ERROR;
  }
  uint8_t data[46]    = { 0xEF, 0xAA, 0x26, 0x00, 0x28 };
  uint8_t i           = 0;
  bool    state       = false;
  uint8_t buffer[250] = { 0 };
  data[5]             = isAdmin;
  for (i = 6; i < 6 + 32; i++) {
    if (i < 6 + nameLen) {
      data[i] = (uint8_t)userName[i - 6];
    } else {
      data[i] = 0;
    }
  }
  if (kind == eFaceUser) {
    data[38] = 0x00;
  } else if (kind == ePalmUser) {
    data[38] = 0xFD;
  }
  data[39] = 0x01;    //Single frame enrollment
  data[40] = 0x00;    //0: Face cannot be re-enrolled, but user name can be duplicated; 1: Allow duplicate enrollment
  data[41] = 0x0A;    //Wait time
  data[42] = 0x00;
  data[43] = 0x00;
  data[44] = 0x00;
  calculateChecksum(data, 46);
  state = writeCmd(data, 46, buffer, 11000);
  if (state == true) {
    if (buffer[6] == RESULT_OK) {
      *id = buffer[7] * 256 + buffer[8];
      return 1;
    } else if (buffer[6] == RESULT_REPEAT) {
      return 2;
    } else if (buffer[6] == RESULT_TIMEOUT) {
      return 3;
    }
  }
  return NO_ACK;
}

int8_t DFRobot_Biometric::deleteUser(uint16_t id)
{
  if (id < 1 || id > 800) {
    return ERROR;
  }
  uint8_t data[9]     = { 0xEF, 0xAA };
  uint8_t buffer[250] = { 0 };
  bool    state       = false;
  if (id <= 500) {
    data[2] = 0x20;    //Face command
    data[7] = 0x00;    //Face
  } else if (id > 500) {
    data[2] = 0x80;    //Palm command
    data[7] = 0x01;    //Palm
  }
  data[3] = 0x00;
  data[4] = 0x03;
  data[5] = id / 256;
  data[6] = id % 256;
  calculateChecksum(data, 9);
  state = writeCmd(data, 9, buffer, 7000);
  if (state == true) {
    if (buffer[6] == RESULT_OK) {
      return 1;
    } else if (buffer[6] == RESULT_NOT_FOUND) {
      return 2;
    } else if (buffer[6] == RESULT_UNKNOWN_ERROR) {
      return 3;
    }
  }
  return NO_ACK;
}

int8_t DFRobot_Biometric::deleteAllUser(void)
{
  uint8_t data[11]    = CMD_DELETE_ALL_USER;
  uint8_t buffer[250] = { 0 };
  bool    state       = false;
  state               = writeCmd(data, 11, buffer, 5000);
  if (state == true) {
    if (buffer[6] == RESULT_OK) {
      return 1;
    } else if (buffer[6] == RESULT_UNKNOWN_ERROR) {
      return 2;
    }
  }
  return NO_ACK;
}

int8_t DFRobot_Biometric::getRecognitionResult(sId_t* ID)
{
  uint8_t data[8]     = CMD_IDENTIFY_USER;
  uint8_t buffer[250] = { 0 };
  bool    state       = false;
  state               = writeCmd(data, 8, buffer, 11000);
  if (state == true) {
    if (buffer[6] == RESULT_OK) {
      ID->id      = buffer[7] * 256 + buffer[8];
      ID->isAdmin = (eIsAdmin_t)buffer[41];
      if (buffer[42] == RECOGNIZED_FACE || buffer[42] == RECOGNIZED_FACE_EYES_CLOSED) {
        ID->kind = eFaceUser;
      } else if (buffer[42] == RECOGNIZED_PALM) {
        ID->kind = ePalmUser;
      }
      for (uint8_t i = 0; i < 32; i++) {
        ID->userName[i] = (char)buffer[9 + i];
      }
      ID->userName[32] = '\0';
      return 1;
    } else if (buffer[6] == RESULT_TIMEOUT) {
      return 2;
    } else if (buffer[6] == RESULT_NOT_FOUND) {
      return 3;
    }
  }
  return NO_ACK;
}

int8_t DFRobot_Biometric::ledColor(uint8_t color, uint8_t kind)
{
  if (kind != LED_ON && kind != LED_OFF) {
    return ERROR;
  }
  if (color != COLOR_GREEN && color != COLOR_RED && color != COLOR_WHITE) {
    return ERROR;
  }
  uint8_t data[8]     = { 0xEF, 0xAA, 0x90, 0x00, 0x02, 0x00, 0x00, 0x00 };
  uint8_t buffer[250] = { 0 };
  bool    state       = false;
  data[5]             = color;
  data[6]             = kind;
  calculateChecksum(data, 8);
  state = writeCmd(data, 8, buffer, 2000);
  if (state == true) {
    if (buffer[6] == RESULT_OK) {
      return 1;
    }
  }
  return NO_ACK;
}

void DFRobot_Biometric::serialEmpty(void)
{
  uint8_t limit = 200;
  while (_serial.available() && limit) {
    _serial.read();
    limit--;
  }
}

bool DFRobot_Biometric::writeCmd(uint8_t* data, uint8_t len, uint8_t* buffer, uint16_t outTime)
{
  bool state = false;
  serialEmpty();
  _serial.write(data, len);
  state = waitForReply(buffer, outTime);
  return state;
}
