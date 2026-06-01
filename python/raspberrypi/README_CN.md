# DFRobot_Biometric

- [English Version](./README.md)

FP001和FP002是人脸掌静脉识别模组，搭载仿生人脸识别算法，支持 UVC/UAC 方式传输，MJPEG 视
频格式，既实现了安全性，又兼具了良好的用户体验，具有功耗低、成本低、快速识别、外观
精致、产品结构小巧等特点，采用了高算力芯片，快速完成人脸识别和掌静脉识别的完整过程

Biometric库是对于这两个模块的功能进行统一的封装，SEN0736和SEN0737都具有人脸录入，人脸识别，用户查询，用户删除等功能。此外，SEN0737还具有三种颜色的指示灯，为其封装了三通不同颜色等的控制功能。算法在模块内完成，本库主要进行指令交互，下达命令，接受反馈，命令响应及时。



![产品效果图片](../../resources/images/SEN0736_black.png)
![产品效果图片](../../resources/images/SEN0736_white.png)
![产品效果图片](../../resources/images/SEN0737.png)
![产品效果图片](../../resources/images/SEN0736_use.png)
![产品效果图片](../../resources/images/SEN0737_use.png)


## 产品链接（链接到中文商城）

    SKU：SEN0736 FP001和SEN0737FP002人脸与掌静脉识别模块

## 目录

  * [概述](#概述)
  * [库安装](#库安装)
  * [方法](#方法)
  * [兼容性](#兼容性)
  * [历史](#历史)
  * [创作者](#创作者)

## 概述

本库实现了人脸与掌静脉注册用户，用户识别，用户的删除管理，获取用户数量，控制指示灯等功能

## 库安装

要使用这个库，首先将库下载到Raspberry Pi，然后打开例程文件夹。要执行一个例程demox.py，请在命令行中输入python demox.py。例如，要执行enrollUser.py例程,你需要输入:

```python
python enroll_user.py
```



## 方法

```python
    '''!
      @brief 检查模块是否就绪且空闲 (CMD_BEGIN, STATUS_STANDBY)
      @return bool 模块是否就绪
      @retval True 模块就绪
      @retval False 模块未就绪
    '''
  def check_state(self):

  '''!
      @brief 获取掌静脉用户数量
      @return int 成功时返回数量
      @retval nums>0 掌静脉用户数量
      @retval NO_ACK 无响应
    '''
  def get_all_nums_palm_user_ids(self):

  '''!
      @brief 获取人脸用户数量
      @return int 成功时返回数量
      @retval nums>0 人脸用户数量
      @retval NO_ACK 无响应
    '''
  def get_all_nums_face_user_ids(self):

  '''!
      @brief 获取人脸用户的具体id信息
      @param id_buffer 存储id信息的数组
      @param length 用户传入的数组长度
      @return int RESULT_OK 成功, ERROR 数组太小, NO_ACK 主模块未回应
    '''
  def get_all_face_user_ids(self, id_buffer, length):


  '''!
      @brief 录入人脸或掌静脉用户
      @param kind FACE_USER 或 PALM_USER
      @param user_name str 1~32 个字符
      @param is_admin ROLE_NORMAL 或 ROLE_ADMIN
      @return tuple (retval, new_id) retval: 1 成功, 2 重复, 3 超时, NO_ACK 无响应, ERROR 用户传的参数错误; new_id int 或 None
    '''
  def enroll_user(self, kind, user_name, is_admin):

  '''!
      @brief 识别用户；成功时填充 sid
      @param sid 用于填充的 SId 实例
      @return 执行结果
      @retval  1 成功, 2 超时, 3 未找到, NO_ACK 无响应, ERROR 用户传的参数错误
    '''
  def get_recognition_result(self, sid):

  '''!
      @brief 根据 ID 删除用户（范围与 C++ 相同：1~800）
      @param user_id int
      @return 执行结果
      @retval  1 成功, 2 未找到, 3 未知错误, NO_ACK 无响应, ERROR 用户传的参数错误
    '''
  def delete_user(self, user_id):

    '''!
      @brief 删除所有用户
      @return 执行结果
      @retval  1 成功, 2 未知错误, NO_ACK 无响应
    '''
  def delete_all_user(self):

    '''!
      @brief LED 颜色控制（开/关）
      @param color COLOR_GREEN, COLOR_RED, COLOR_WHITE
      @param kind LED_ON 或 LED_OFF
      @return 执行结果
      @retval  1 成功, NO_ACK 无响应, ERROR 用户传的参数错误
    '''
  def led_color(self, color, kind):

    '''!
      @brief 关闭串口
    '''
  def close(self):
```

## 兼容性



| 主板         | 通过 | 未通过 | 未测试 | 备注 |
| ------------ | :--: | :----: | :----: | :--: |
| RaspberryPi2 |      |        |   √    |      |
| RaspberryPi3 |      |        |   √    |      |
| RaspberryPi4 |  √   |        |        |      |
| RaspberryPi5 |  √   |        |        |      |

* Python 版本

| Python  | 通过 | 未通过 | 未测试 | 备注 |
| ------- | :--: | :----: | :----: | ---- |
| Python2 |      |        |    √   |      |
| Python3 |  √   |        |        |      |

## 历史

- 2026/05/22 - 1.0.0 版本

## 创作者

Written by Olive-hy(feng.yang@dfrobot.com), 2026-5-11 (Welcome to our [website](https://www.dfrobot.com/))
