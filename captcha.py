# coding: utf8

import base64
from io import BytesIO
from functools import wraps
from string import ascii_letters, digits
from random import randint, sample as random_sample
from PIL import Image, ImageDraw, ImageFont


def captcha_exception_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return False, False
    return wrapper


class ImageCaptcha:
    def __init__(self, img_size=(100, 46), char_list=None, font_size=(29, 36),
                 font_file='SourceCodePro-Medium.ttf', captcha_length=4):
        self.img_size = img_size
        if char_list is None:
            # 大小写字母 +　数字，删除易混淆的 o & O
            self.char_list = ascii_letters.replace('o', '').replace('O', '') + digits
        else:
            self.char_list = char_list
        self.font_size = font_size
        import platform
        if platform.system().lower() == 'windows':
            self.font = font_file
        else:
            self.font = '/usr/share/fonts/' + font_file
        self.captcha_length = captcha_length

        self.background_color = None
        self.background_color_range = (140, 255)
        self.chars_list_len = len(self.char_list)
        self.img_width, self.img_height = self.img_size
        self.lines_color_range = (0, 135)
        self.text_color_range = self.lines_color_range

    @captcha_exception_wrap
    def generate(self):
        self.background_color = self.randint_tuple(self.background_color_range)
        img = Image.new('RGB', self.img_size, self.background_color)
        img_draw = ImageDraw.Draw(img)
        if self.draw_lines(img_draw):
            ch = self.draw_str(img_draw)
            if ch:
                return ch, img

    @captcha_exception_wrap
    def generate_base64(self):
        # 生成 base64 字符串
        ch, img = self.generate()
        if False in [ch, img]:
            return False, False
        img_buff = BytesIO()
        img.save(img_buff, format='JPEG')
        return ch, base64.b64encode(img_buff.getvalue()).decode()

    @staticmethod
    def randint_tuple(randint_range, count=3):
        return tuple(randint(*randint_range) for _ in range(count))

    def draw_lines(self, img_draw):
        lines_num = randint(5, 8)
        for i in range(lines_num):
            begin_end_point = self.random_line_begin_end()
            img_draw.line(xy=begin_end_point,
                          width=randint(3, 5),
                          fill=self.randint_tuple(self.lines_color_range))
        return True

    def random_line_begin_end(self):
        # 尽量在图片中央画线
        begin = (randint(self.img_width * 0.1, self.img_width * 0.8),
                 randint(self.img_width * 0.1, self.img_height))
        begin_x = begin[0]
        end_x = randint(begin_x, begin_x + 40)
        end = (end_x, randint(self.img_width * 0.1, self.img_height))
        return [begin, end]

    def random_char_xy(self, index):
        center = int(self.img_width / 2)
        left = center + (index - 2) * 12
        return left, randint(0, 12)

    def draw_str(self, img_draw):
        random_chr = random_sample(self.char_list, self.captcha_length)
        for i in range(self.captcha_length):
            font = ImageFont.truetype(self.font, randint(*self.font_size))
            img_draw.text(xy=self.random_char_xy(i),
                          text=random_chr[i],
                          font=font,
                          fill=self.randint_tuple(self.text_color_range))
        return ''.join(random_chr)


if __name__ == "__main__":
    import time
    buffer = BytesIO()
    code, code_img = ImageCaptcha().generate()
    print(code)
    code_img.save("my_code_{}.jpg".format(int(time.time())), "JPEG")
