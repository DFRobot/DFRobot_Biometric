/*!
 * @file sen0737GetDeleteId.ino
 * @brief This routine implements user lookup and deletion
 * @details This routine sends string commands over serial to the host controller
 * @n which parses and executes the corresponding actions on the module.
 * @n Supported commands: AT+GETUSERS (get number of users), AT+DELUSER=<ID> (delete user by ID), and AT+DELALLUSERS (delete all users).
 * @n After each command is successfully executed, the indicator light will display different colors corresponding to the command result.
 * @copyright Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [Olive](feng.yang@dfrobot.com)
 * @version V1.0
 * @date 2026-04-30
 * @url https://github.com/DFRobot/DFRobot_Biometric
 */

#include "DFRobot_Biometric.h"
#include "string.h"

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
  delay(1500);             //Wait for module to start
}
uint8_t j = 0;
void    loop()
{
  // put your main code here, to run repeatedly:
  while (face.checkState() == false) {    //Determine whether the module is ready
    Serial.println("Module not ready !");
  }
  if (j++ < 1) {
    Serial.println("Module ready !");
    Serial.println("-----------------------------");
    //Command Introduction
    Serial.println("Available commands:");
    Serial.println("AT+GETUSERS       # Get all user information");
    Serial.println("AT+DELUSER=ID     # Delete the specified user (e.g. AT+DELUSER=0x1001)");
    Serial.println("AT+DELALLUSERS    # Delete all users");
    Serial.println("-----------------------------");
  }
  char    data[20] = { 0 };
  int16_t nums = 0, id = 0;
  while (!Serial.available()) {
    ;
  }
  //Read the user's command
  String input = Serial.readStringUntil('\n');
  input.trim();
  input.toCharArray(data, 30);
  //Match the command of user
  if (strcmp(data, "AT+GETUSERS") == 0) {
    nums = face.getAllNumsFaceUserIDs();
    Serial.print("the nums of face id:");
    Serial.println(nums);
    delay(100);
    uint16_t id[50];
    face.getAllFaceUserIDs(id, 50);
    if (nums > 0) {
      Serial.print("face user ids:");
      for (int16_t i = 0; i < nums; i++) {
        Serial.print(id[i]);
        Serial.print(" ");
      }
      Serial.println("");
      delay(100);
    }
    nums = face.getAllNumsPalmUserIDs();
    Serial.print("the nums of palm id:");
    Serial.println(nums);
    face.ledColor(COLOR_WHITE, LED_OFF);
    face.ledColor(COLOR_RED, LED_OFF);
    face.ledColor(COLOR_GREEN, LED_ON);
  } else if (strncmp(data, "AT+DELUSER=", 11) == 0) {
    id   = atoi(&data[11]);
    nums = face.deleteUser(id);
    if (nums == 1) {
      Serial.print("Successful delete user:");
      Serial.println(id);
      face.ledColor(COLOR_RED, LED_OFF);
      face.ledColor(COLOR_GREEN, LED_OFF);
      face.ledColor(COLOR_WHITE, LED_ON);
    } else {
      Serial.println("Fail");
    }
  } else if (strcmp(data, "AT+DELALLUSERS") == 0) {
    nums = face.deleteAllUser();
    if (nums == 1) {
      Serial.println("Successful delete all");
      face.ledColor(COLOR_GREEN, LED_OFF);
      face.ledColor(COLOR_WHITE, LED_OFF);
      face.ledColor(COLOR_RED, LED_OFF);
    } else {
      Serial.println("Fail");
    }
  }
  Serial.println("");
  Serial.println("please continue:");
  delay(3000);
}
