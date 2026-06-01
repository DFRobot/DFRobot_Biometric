'''!
@file DFRobot_Biometric.py
@brief UART driver for DFRobot biometric module on Raspberry Pi 2/3/4 (pyserial).
@details Mirrors DFRobot_Biometric Arduino library framing, checksum, and command flow.
@n Connect module UART to Pi GPIO serial (e.g. /dev/serial0); disable serial console if needed.
@copyright   Copyright (c) 2026 DFRobot Co.Ltd (http://www.dfrobot.com)
@license     The MIT License (MIT)
@author      [Olive](feng.yang@dfrobot.com)
@version     V1.0.0
@date        2026-05-07
@url         https://github.com/DFRobot/DFRobot_Biometric
'''

import time


def wire_xor_checksum_inplace(data, length):
  '''!
  @brief Same XOR rule as DFRobot_Biometric.__calculate_checksum (module-level for tests / REPL).
  @details XOR bytes from index 2 through length-2, result written to data[length-1].
  @param data bytearray or mutable sequence of int 0..255
  @param length int Total frame length including checksum byte position
  '''
  if length < 3:
    raise ValueError('length must be at least 3')
  check_sum = 0
  for i in range(2, length - 1):
    check_sum ^= data[i]
  data[length - 1] = check_sum


class SId:
  '''!
  @brief Recognition result container (same role as sId_t in C++).
  @details Filled by get_recognition_result on success.
  '''

  def __init__(self):
    self.id = 0
    self.kind = 0
    self.is_admin = 0
    self.user_name = ''

  def __str__(self):
    return f'id={self.id}\nkind={"Face" if self.kind == DFRobot_Biometric.FACE_USER else "Palm"}\nis_admin={"Administrator" if self.is_admin == DFRobot_Biometric.ROLE_ADMIN else "Normal user"}\nuser_name="{self.user_name}"'


class DFRobot_Biometric:
  '''!
  @brief Biometric module over UART (USART), protocol compatible with DFRobot_Biometric Arduino class.
  '''

  ## NO_ACK means no response received
  NO_ACK = -1
  ## The parameter passed to the function does not meet the requirements
  ERROR = -2

  ## User kinds
  FACE_USER = 0x01  ## Face user
  PALM_USER = 0x02  ## Palm user

  ## Two User roles:
  ## common user
  ROLE_NORMAL = 0
  ## administrator user
  ROLE_ADMIN = 1

  ## LED colors and states
  COLOR_GREEN = 0x00  ## Green light
  COLOR_RED = 0x01  ## Red light
  COLOR_WHITE = 0x02  ## White light
  LED_OFF = 0x01  ## Turn off LED
  LED_ON = 0x00  ## Turn on LED

  ## Check status command
  __CMD_CHECK_STATUS = bytes([0xEF, 0xAA, 0x11, 0x00, 0x00, 0x11])
  ## Get face user count command
  __CMD_GET_FACE_USER_NUMS = bytes([0xEF, 0xAA, 0x24, 0x00, 0x01, 0x01, 0x24])
  ## Get palm user count command
  __CMD_GET_PALM_USER_NUMS = bytes([0xEF, 0xAA, 0x24, 0x00, 0x01, 0x02, 0x27])
  ## Get specific information of the face user command
  __CMD_GET_FACE_USER_SPECIFIC = bytes([0xEF, 0xAA, 0x24, 0x00, 0x01, 0x00, 0x25])
  ## Delete all users command
  __CMD_DELETE_ALL_USER = bytes([0xEF, 0xAA, 0x21, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24])
  ## Identify user command
  __CMD_IDENTIFY_USER = bytes([0xEF, 0xAA, 0x12, 0x00, 0x02, 0x00, 0x0A, 0x1A])

  __STATUS_STANDBY = 0x00  ## Standby status

  __RESULT_OK = 0x00  ## Command executed successfully
  __RESULT_TIMEOUT = 0x0D  ## Command execution timeout
  __RESULT_REPEAT = 0x0A  ## Face already enrolled
  __RESULT_NOT_FOUND = 0x08  ## User not found
  __RESULT_UNKNOWN_ERROR = 0x05  ## Unknown error occurred

  __RECOGNIZED_FACE = 0xC8  ## Face recognized (eyes open)
  __RECOGNIZED_FACE_EYES_CLOSED = 0xCC  ## Face recognized (eyes closed)
  __RECOGNIZED_PALM = 0xFA  ## Palm vein recognized

  def __init__(self, port='/dev/serial0', baudrate=115200, timeout=0, serial_instance=None):
    '''!
    @brief Constructor
    @param port Serial device path (Pi: /dev/serial0 or /dev/ttyAMA0 / USB ttyUSB0)
    @param baudrate UART baud rate (match module; often 115200)
    @param timeout Read timeout in seconds for pyserial (0 = non-blocking reads; reply uses monotonic waits)
    @param serial_instance Optional pre-built serial-like object (in_waiting, read, write, is_open, close) for tests
    '''
    self.__port_path = port
    self.__baudrate = baudrate
    self.__timeout = timeout
    if serial_instance is not None:
      self.__ser = serial_instance
      return
    try:
      import serial as pyserial
    except ImportError as exc:
      raise ImportError('pyserial is required on the Pi: pip install pyserial') from exc
    self.__ser = pyserial.Serial(port=self.__port_path, baudrate=self.__baudrate, timeout=self.__timeout)

  def check_state(self):
    '''!
    @brief Check module is ready and idle
    @return bool True if module ready
    @retval True module ready
    @retval False module not ready
    '''
    data = bytearray(self.__CMD_CHECK_STATUS)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 6, buffer, 1000)
    if state is True:
      if buffer[7] == self.__STATUS_STANDBY:
        return True
    return False

  def get_all_nums_face_user_ids(self):
    '''!
    @brief Get number of face users
    @return int Count on success
    @retval nums>0 collect Number of face users
    @retval NO_ACK -1 no response
    '''
    data = bytearray(self.__CMD_GET_FACE_USER_NUMS)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 7, buffer, 1000)
    if state is True:
      nums = buffer[7] * 256 + buffer[8]
      return nums
    return self.NO_ACK

  def get_all_nums_palm_user_ids(self):
    '''!
    @brief Get number of palm users
    @return int Count on success
    @retval nums>0 collect Number of palm users
    @retval NO_ACK -1 no response
    '''
    data = bytearray(self.__CMD_GET_PALM_USER_NUMS)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 7, buffer, 1000)
    if state is True:
      nums = buffer[7] * 256 + buffer[8]
      return nums
    return self.NO_ACK

  def get_all_face_user_ids(self, id_buffer, length):
    '''!
    @brief Get specific face user IDs
    @param id_buffer writable sequence to receive face IDs
    @param length int Maximum number of IDs the buffer can hold
    @return int RESULT_OK on success, ERROR -2 when buffer is too small, NO_ACK no response
    '''
    data = bytearray(self.__CMD_GET_FACE_USER_SPECIFIC)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 7, buffer, 3000)
    if state is True:
      user_nums = buffer[7] * 256 + buffer[8]
      if length < user_nums:
        return self.ERROR
      for i in range(user_nums):
        id_buffer[i] = buffer[9 + i * 2] * 256 + buffer[9 + i * 2 + 1]
      return self.__RESULT_OK
    return self.NO_ACK

  def enroll_user(self, kind, user_name, is_admin):
    '''!
    @brief Enroll face or palm
    @param kind FACE_USER or PALM_USER
    @param user_name str 1~32 characters
    @param is_admin ROLE_NORMAL or ROLE_ADMIN
    @return tuple (retval, new_id) retval: 1 success, 2 duplicate, 3 timeout, NO_ACK is no response, ERROR parameter error; new_id int or None
    '''
    name_bytes = user_name.encode('utf-8', errors='ignore') if isinstance(user_name, str) else bytes(user_name)
    name_len = len(name_bytes)
    if name_len > 32:
      return (self.ERROR, None)
    if is_admin != self.ROLE_NORMAL and is_admin != self.ROLE_ADMIN:
      return (self.ERROR, None)
    data = bytearray(46)
    data[0:5] = bytes([0xEF, 0xAA, 0x26, 0x00, 0x28])
    data[5] = is_admin & 0xFF
    for i in range(6, 6 + 32):
      if i < 6 + name_len:
        data[i] = name_bytes[i - 6]
      else:
        data[i] = 0
    if kind == self.FACE_USER:
      data[38] = 0x00
    elif kind == self.PALM_USER:
      data[38] = 0xFD
    else:
      return (self.ERROR, None)
    data[39] = 0x01
    data[40] = 0x00
    data[41] = 0x0A
    data[42] = 0x00
    data[43] = 0x00
    data[44] = 0x00
    self.__calculate_checksum(data, 46)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 46, buffer, 16500)
    if state is True:
      if buffer[6] == self.__RESULT_OK:
        new_id = buffer[7] * 256 + buffer[8]
        return (1, new_id)
      if buffer[6] == self.__RESULT_REPEAT:
        return (2, None)
      if buffer[6] == self.__RESULT_TIMEOUT:
        return (3, None)
    return (self.NO_ACK, None)

  def get_recognition_result(self, sid):
    '''!
    @brief Identify user; fills sid on success
    @param sid SId instance to fill
    @return the result
    @retval  1 success,2 timeout,3 not found,NO_ACK no response,ERROR parameter error
    '''
    if not isinstance(sid, SId):
      return self.ERROR
    data = bytearray(self.__CMD_IDENTIFY_USER)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 8, buffer, 12000)
    if state is True:
      if buffer[6] == self.__RESULT_OK:
        sid.id = buffer[7] * 256 + buffer[8]
        sid.is_admin = buffer[41]
        if buffer[42] == self.__RECOGNIZED_FACE or buffer[42] == self.__RECOGNIZED_FACE_EYES_CLOSED:
          sid.kind = self.FACE_USER
        elif buffer[42] == self.__RECOGNIZED_PALM:
          sid.kind = self.PALM_USER
        raw = bytes(buffer[9 : 9 + 32])
        sid.user_name = raw.split(b'\x00', 1)[0].decode('utf-8', errors='replace')
        return 1
      if buffer[6] == self.__RESULT_TIMEOUT:
        return 2
      if buffer[6] == self.__RESULT_NOT_FOUND:
        return 3
    return self.NO_ACK

  def delete_user(self, user_id):
    '''!
    @brief Delete user by id (same bounds and branches as C++: 1~800)
    @param user_id int
    @return the result
    @retval  1 success,2 not found,3 unknown error,NO_ACK no response,ERROR parameter error
    '''
    if user_id < 1 or user_id > 800:
      return self.ERROR
    data = bytearray(9)
    data[0] = 0xEF
    data[1] = 0xAA
    if user_id <= 500:
      data[2] = 0x20
      data[7] = 0x00
    elif user_id > 500:
      data[2] = 0x80
      data[7] = 0x01
    data[3] = 0x00
    data[4] = 0x03
    data[5] = user_id // 256
    data[6] = user_id % 256
    self.__calculate_checksum(data, 9)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 9, buffer, 7000)
    if state is True:
      if buffer[6] == self.__RESULT_OK:
        return 1
      if buffer[6] == self.__RESULT_NOT_FOUND:
        return 2
      if buffer[6] == self.__RESULT_UNKNOWN_ERROR:
        return 3
    return self.NO_ACK

  def delete_all_user(self):
    '''!
    @brief Delete all users
    @return the result
    @retval  1 success,2 unknown err,NO_ACK no response
    '''
    data = bytearray(self.__CMD_DELETE_ALL_USER)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 11, buffer, 5000)
    if state is True:
      if buffer[6] == self.__RESULT_OK:
        return 1
      if buffer[6] == self.__RESULT_UNKNOWN_ERROR:
        return 2
    return self.NO_ACK

  def led_color(self, color, kind):
    '''!
    @brief LED color on/off
    @param color COLOR_GREEN, COLOR_RED, COLOR_WHITE
    @param kind LED_ON or LED_OFF
    @return the result
    @retval  1 success,NO_ACK no response,ERROR parameter error
    '''
    if kind != self.LED_ON and kind != self.LED_OFF:
      return self.ERROR
    if color != self.COLOR_GREEN and color != self.COLOR_RED and color != self.COLOR_WHITE:
      return self.ERROR
    data = bytearray([0xEF, 0xAA, 0x90, 0x00, 0x02, 0x00, 0x00, 0x00])
    data[5] = color
    data[6] = kind
    self.__calculate_checksum(data, 8)
    buffer = bytearray(250)
    state = self.__write_cmd(data, 8, buffer, 2000)
    if state is True:
      if buffer[6] == self.__RESULT_OK:
        return 1
    return self.NO_ACK

  def close(self):
    '''!
    @brief Close serial port
    '''
    if self.__ser is None:
      return
    try:
      if self.__ser.is_open:
        self.__ser.close()
    except AttributeError:
      self.__ser.close()

  def __del__(self):
    try:
      self.close()
    except Exception:
      pass

  def __calculate_checksum(self, data, length):
    wire_xor_checksum_inplace(data, length)

  def __millis(self):
    return int(time.monotonic() * 1000)

  def __wait_for_reply(self, buffer, timeout_ms):
    recmd_len = 0
    buf_len = 0
    start_time = self.__millis()
    while self.__millis() - start_time < timeout_ms:
      if self.__ser.in_waiting:
        rec_data = self.__ser.read(1)[0]
        if buf_len < 3:
          if rec_data == 0xEF and buf_len == 0:
            buffer[buf_len] = rec_data
            buf_len += 1
          elif rec_data == 0xAA and buf_len == 1:
            buffer[buf_len] = rec_data
            buf_len += 1
          elif rec_data == 0x00 and buf_len == 2:
            buffer[buf_len] = rec_data
            buf_len += 1
          elif rec_data == 0x01 and buf_len == 2:
            buf_len = 0
          else:
            buf_len = 0
        else:
          if buf_len == 3:
            buffer[buf_len] = rec_data
            buf_len += 1
          elif buf_len == 4:
            buffer[buf_len] = rec_data
            buf_len += 1
            recmd_len = buffer[3] * 256 + buffer[4]
          elif buf_len > 4 and buf_len <= (4 + recmd_len):
            buffer[buf_len] = rec_data
            buf_len += 1
          elif buf_len == (5 + recmd_len):
            tmp = bytearray(buffer[0 : buf_len + 1])
            self.__calculate_checksum(tmp, buf_len + 1)
            if rec_data == tmp[buf_len]:
              self.__serial_empty()
              buffer[0 : buf_len + 1] = tmp[0 : buf_len + 1]
              return True
    return False

  def __serial_empty(self):
    while self.__ser.in_waiting:
      self.__ser.read(self.__ser.in_waiting)

  def __write_cmd(self, data, length, buffer, out_time_ms):
    self.__serial_empty()
    self.__ser.write(bytes(data[0:length]))
    state = self.__wait_for_reply(buffer, out_time_ms)
    return state
