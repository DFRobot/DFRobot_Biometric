/*!
 * @file sen0736Recognition.ino
 * @brief Continuous automatic user recognition routine on Raspberry Pi 2/3/4 (pyserial).
 * @details This routine periodically detects faces, automatically recognizes them
 * @n and prints user details via the serial port.
 * @copyright Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [Olive](feng.yang@dfrobot.com)
 * @version V1.0
 * @date 2026-04-30
 * @url https://github.com/DFRobot/DFRobot_Biometric
 */

#include "DFRobot_Biometric.h"

/* -----------------------------------------------------------------------------------------------------
  *    board   |             MCU                |   Leonardo/Mega2560/M0  |   ESP8266  |     ESP32     |
  *     VCC    |            3.3V/5V             |          VCC            |    VCC     |      VCC      |
  *     GND    |              GND               |          GND            |    GND     |      GND      |
  *     RX     |              TX                |      Serial1 TX1        |    5/D6    |  Serial2 TX1  |
  *     TX     |              RX                |      Serial1 RX1        |    4/D7    |  Serial2 RX1  |
  * ----------------------------------------------------------------------------------------------------*/
/* Baud rate cannot be changed , it is 115200 */

#if defined(ESP8266)
#define SOFT_RX_PIN 4
#define SOFT_TX_PIN 5
#include <SoftwareSerial.h>
SoftwareSerial ModuleSerial(SOFT_RX_PIN, SOFT_TX_PIN);
#elif defined(ESP32)
#define RX_PIN       16
#define TX_PIN       17
#define ModuleSerial Serial2
#else
#define ModuleSerial Serial1
#endif

DFRobot_Biometric face(ModuleSerial);

void setup()
{
#if defined(ESP32)
  ModuleSerial.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);
#else
  ModuleSerial.begin(115200);
#endif

  Serial.begin(115200);    //Start serial 1, for information printing
  delay(1500);             //Wait for module to start
}

void loop()
{
  // put your main code here, to run repeatedly:
  while (face.checkState() == false) {    //Determine whether the module is ready
    Serial.println("Module not ready !");
  }
  Serial.println("Module ready!");
  Serial.println("------------------------------------------------");
  DFRobot_Biometric::sId_t user   = { 0, DFRobot_Biometric::eFaceUser, DFRobot_Biometric::eRoleNormal, { 0 } };    //Store the recognized user information
  int8_t                   result = 0;
  result                          = face.getRecognitionResult(&user);
  //Determine the execution result
  if (result == 1) {
    Serial.println("Success! The imformation of the user:");
    Serial.print("id:");
    Serial.println(user.id);
    Serial.print("userName:");
    Serial.println(user.userName);
    Serial.print("user kind:");
    if (user.kind == face.eFaceUser) {
      Serial.println("face user");
    } else if (user.kind == face.ePalmUser) {
      Serial.println("palm user");
    }
    Serial.print("userClass:");
    if (user.isAdmin == face.eRoleNormal) {
      Serial.println("Normal user");
    } else if (user.isAdmin == face.eRoleAdmin) {
      Serial.println("Adminer");
    }
  } else if (result == 2) {
    Serial.println("time out");
  } else if (result == NO_ACK) {
    Serial.println("No response from module");
  } else if (result == 3) {
    Serial.println("not found");
  }
  Serial.println("------------------------------------------------");
  Serial.println("");
  delay(10000);
}
