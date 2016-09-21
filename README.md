# Simple Captcha

简单的验证码生成程序。

## Requirements
* Python 3
* Pillow

## Preview
![image](https://raw.githubusercontent.com/BlowingDust/SimpleCaptcha/master/image/my_code_y1JY.jpg)

``code: y1JY``

## Usage
默认字体：Source Code Pro

默认图片尺寸：100 × 46 px

平均图片文件大小：2 KB
```python
# 返回验证码答案和图片
code, img = ImageCaptcha().generate()

# 返回验证码答案和经过 base64 编码的图片
code, base64_img = ImageCaptcha().generate_base64()

# 若生成失败，返回两个 False
# 暂未进行充分测试，使用自定义参数时请注意验证码图片的可识别性
```
