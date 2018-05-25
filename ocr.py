#!/usr/bin/env python
# coding=utf-8


import os
from urllib import request


TMP_DIR = "./tmp_dir"
TMP_IMG = "./tmp_img.jpg"
EXTENSION = ".txt"

# tesseract 引擎的安装路径
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR"


class Ocr:

    """
    页面切割模式

    Page segmentation modes:
    0    Orientation and script detection (OSD) only.
    1    Automatic page segmentation with OSD.
    2    Automatic page segmentation, but no OSD, or OCR.
    3    Fully automatic page segmentation, but no OSD. (Default)
    4    Assume a single column of text of variable sizes.
    5    Assume a single uniform block of vertically aligned text.
    6    Assume a single uniform block of text.
    7    Treat the image as a single text line.
    8    Treat the image as a single word.
    9    Treat the image as a single word in a circle.
    10   Treat the image as a single character.
    """

    def __init__(
        self,
        tesseract_path=TESSERACT_PATH,
        *,
        out_path=None,
        mode=3,
        delete=True
    ):
        """
        :param tesseract_path: tesseract 引擎的安装路径
        :param out_path: 输出文件路径
        :param mode: 图片的切割模式
        :param delete: 是否保留生成的文本文件
        """
        self._tesseract_path = tesseract_path
        self._outpath = out_path
        self._mode = mode
        self._delete = delete

    def exec(self, *, img_path="", img_url=None):
        """
        执行命令

        :param img_path: 本地图片路径
        :param img_url: 网络图片地址
        """
        save_img = TMP_IMG
        if os.path.exists(img_path):
            save_img = img_path
        else:
            try:
                request.urlretrieve(img_url, save_img)
            except Exception as e:
                print(e)

        if self._outpath is None:
            self._outpath = TMP_DIR
        elif self._outpath.endswith(EXTENSION):
            self._outpath = self._outpath[:-4]
        if self._mode > 10 or self._mode < 0:
            self._mode = 3
        os.chdir(self._tesseract_path)
        cmd = "tesseract.exe {save_img} {out} -psm {mode}".format(
            save_img=save_img, out=self._outpath, mode=self._mode
        )
        os.system(cmd)

        try:
            txt_file = self._outpath + EXTENSION
            with open(txt_file, "r") as f:
                ocr_text = f.read().strip()
            if self._delete:
                os.remove(txt_file)
                os.remove(TMP_IMG)
            return ocr_text
        except IOError:
            print("无法找到该文件!")


if __name__ == "__main__":
    ocr = Ocr()
    result = ocr.exec()
