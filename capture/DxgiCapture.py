import ctypes
from ctypes import *

import cv2
import numpy as np
import win32gui


class DxgiCapture(object):
    def __init__(self, hwnd):
        self.hwnd = hwnd
        # 后续存放图片数据
        self.dxgi = ctypes.windll.LoadLibrary("./dxgi4py.dll")
        self.dxgi.grab.argtypes = (POINTER(ctypes.c_ubyte), ctypes.c_int, c_int, c_int, c_int)
        self.dxgi.grab.restype = POINTER(c_ubyte)
        self.dxgi.init_dxgi(self.hwnd)

    def grab(self, capture_settings: dict[str, int]):
        width, height = capture_settings.get('width'), capture_settings.get('height')
        shot_left = capture_settings.get('left')
        shot_top = capture_settings.get('top')

        shot = np.ndarray((height, width, 4), dtype=np.uint8)
        shot_ptr = shot.ctypes.data_as(POINTER(c_ubyte))
        buffer = self.dxgi.grab(shot_ptr, shot_left, shot_top, width, height)
        image = np.ctypeslib.as_array(buffer, (height, width, 4))
        img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        return img

    def grab_gray(self,capture_settings: dict[str, int]):
        img = self.grab(capture_settings)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
