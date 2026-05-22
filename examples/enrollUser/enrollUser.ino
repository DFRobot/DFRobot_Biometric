/*!
 * @file enrollUser.ino
 * @brief Example of face or palm user enrollment
 * @details This example performs user enrollment every time the board is reset,
 * @n and prints the enrollment result through the serial port
 * @n Enrollment should work normally as long as the connection is correct
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

#if defined(ESP8266) || defined(ARDUINO_AVR_UNO)
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
  delay(1000);             //Wait for module to start
  Serial.println("------------------------------------------------");
  while (face.checkState() == false) {    //Determine whether the module is ready
    Serial.println("Module not ready!");
    delay(200);
  }
  Serial.println("Module ready!");
  int8_t result = 0;
  //Initialize user information
  uint16_t                       id;
  char                           name[]    = "Lebron James";
  DFRobot_Biometric::eUserKind_t userKind  = face.ePalmUser;      //choose the user kind
  DFRobot_Biometric::eIsAdmin_t  userclass = face.eRoleNormal;    //choose the class of user,normal user or adminer

  Serial.println("Start user enrollment");
  result = face.enrollUser(userKind, name, &id, userclass);
  //Determine the execution result
  if (result == 1) {
    Serial.println("Successful enrollment!");
    Serial.print("the user id is:");
    Serial.println(id);
    Serial.print("the user name is:");
    Serial.println(name);
    Serial.print("the user kind is:");
    if (userKind == face.eFaceUser) {
      Serial.println("face user");
    } else if (userKind == face.ePalmUser) {
      Serial.println("palm user");
    }
    Serial.print("the userClass is:");
    if (userclass == face.eRoleNormal) {
      Serial.println("Normal user");
    } else if (userclass == face.eRoleAdmin) {
      Serial.println("Adminer");
    }
  } else if (result == 2) {
    Serial.println("User already exists");
  } else if (result == 3) {
    Serial.println("Enrollment timeout");
  } else if (result == NO_ACK) {
    Serial.println("No response from module");
  } else if (result == ERROR) {
    Serial.println("Parameter range error");
  }
  Serial.println("------------------------------------------------");
  Serial.println("");
}

void loop()
{
  delay(2000);
}
