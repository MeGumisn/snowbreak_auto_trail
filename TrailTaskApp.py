import ctypes
import logging
import time
from time import sleep

import cv2
import win32api
import win32con

from capture.DxgiCapture import DxgiCapture
import Setting
from Setting import ImageTemplates
from utils.KeyboardUtil import KeyboardUtil
from utils.WindowUtil import WindowUtil

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')  # 将日志写入文件
    ]
)


class TrailTaskApp:

    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.capture = DxgiCapture(hwnd)

    def check_match_templates(self, grayImg: cv2.Mat, grayTemplateImg: cv2.Mat):
        res = cv2.matchTemplate(grayImg, grayTemplateImg, cv2.TM_CCOEFF_NORMED)
        # 找到最佳匹配位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8:
            # 获取模板的宽度和高度
            w, h = grayTemplateImg.shape[::-1]
            # 计算最佳匹配位置的中心点
            top_left = max_loc
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            center_point = (center_x, center_y)
            logging.info(f"Found template at {center_point}")
            return center_point
        else:
            return None

    def get_image_position(self, capture_setting: dict[str, int], templateImg: cv2.Mat):
        img = self.capture.grab_gray(capture_setting)
        center_point = self.check_match_templates(img, templateImg)
        return center_point

    @staticmethod
    def center_to_client_pos(center_point: (int, int), capture_setting: dict[str, int]):
        center_x, center_y = center_point
        return center_x + capture_setting['left'], center_y + capture_setting['top']

    def click_until_found(self, capture_setting, template, name="", timeout=60):
        start_time = time.time()
        while True:
            logging.info(f"Click until found {name}")
            if time.time() - start_time > timeout:
                raise TimeoutError("Failed to find the target image within the timeout period.")
            center_point = self.get_image_position(capture_setting, template)
            while center_point:
                x, y = self.center_to_client_pos(center_point, capture_setting)
                logging.info(f"Click at client {x}, {y}")
                KeyboardUtil.click_mouse(self.hwnd, x, y)
                sleep(1)
                center_point = self.get_image_position(capture_setting, template)
                if center_point is None:
                    return
                if time.time() - start_time > timeout:
                    raise TimeoutError("Failed to find the target image within the timeout period.")
                if not WindowUtil.is_scroll_lock_on():
                    break
            if not WindowUtil.is_scroll_lock_on():
                break
            sleep(1)

    def back_to_home(self):
        """返回主页面"""
        logging.info("Back to home")
        center_point = self.get_image_position(Setting.HOME_PAGE, ImageTemplates.HOME_PAGE)
        while center_point is None:
            KeyboardUtil.press_key(self.hwnd, win32con.VK_ESCAPE)
            sleep(1)
            center_point = self.get_image_position(Setting.HOME_PAGE, ImageTemplates.HOME_PAGE)

    def setup(self):
        self.back_to_home()
        if not WindowUtil.is_scroll_lock_on():
            return
        # 点击主页面上的“战斗”按钮
        self.click_until_found(Setting.HOME_PAGE, ImageTemplates.HOME_PAGE, "HOME_PAGE")
        # 点击并进入悖论迷宫
        self.click_until_found(Setting.MAZE_BUTTON, ImageTemplates.MAZE_BUTTON, "MAZE_BUTTON")
        # 点击并进入验证战场
        self.click_until_found(Setting.BATTLE_GROUND, ImageTemplates.BATTLE_GROUND, "BATTLE_GROUND")
        # 点击并进入增益试炼
        self.click_until_found(Setting.TRAIL_BUTTON, ImageTemplates.TRAIL_BUTTON, "TRAIL_BUTTON")
        logging.info("Setup finished")

    def start(self):
        # 点击并进入厄险难度关卡
        self.click_until_found(Setting.EXTREME_TRAIL, ImageTemplates.EXTREME_TRAIL, "EXTREME_TRAIL")
        # 点击开始作战按钮
        self.click_until_found(Setting.START_BUTTON, ImageTemplates.START_BUTTON, "START_BUTTON")
        while self.get_image_position(Setting.QUIT_BUTTON, ImageTemplates.QUIT_BUTTON) is None:
            self.battle()
            if not WindowUtil.is_scroll_lock_on():
                break
        self.click_until_found(Setting.QUIT_BUTTON, ImageTemplates.QUIT_BUTTON, "QUIT_BUTTON")

    def battle(self):
        confirmButtonCenter = self.get_image_position(Setting.CONFIRM_BUFF_BUTTON, ImageTemplates.CONFIRM_BUFF_BUTTON)
        while confirmButtonCenter is None:
            KeyboardUtil.press_key(self.hwnd, win32api.VkKeyScan('E') & 0xFF)
            sleep(1)
            confirmButtonCenter = self.get_image_position(Setting.CONFIRM_BUFF_BUTTON,
                                                          ImageTemplates.CONFIRM_BUFF_BUTTON)
            # 检测到任务完成
            if self.get_image_position(Setting.QUIT_BUTTON, ImageTemplates.QUIT_BUTTON) is not None:
                return
            if not WindowUtil.is_scroll_lock_on():
                break
        x, y = self.center_to_client_pos(confirmButtonCenter, Setting.CONFIRM_BUFF_BUTTON)
        KeyboardUtil.click_mouse(self.hwnd, x, y - 500)
        sleep(1)
        KeyboardUtil.click_mouse(self.hwnd, x, y)
        sleep(1)
        buffSlotCenter = self.get_image_position(Setting.BUFF_SLOT, ImageTemplates.BUFF_SLOT)
        if buffSlotCenter is not None:
            x, y = self.center_to_client_pos(buffSlotCenter, Setting.BUFF_SLOT)
            KeyboardUtil.click_mouse(self.hwnd, x, y)
            sleep(0.5)
            try:
                self.click_until_found(Setting.BUFF_SLOT_CONFIRM, ImageTemplates.BUFF_SLOT_CONFIRM)
            except TimeoutError as e:
                logging.info("Buff slot confirm click timeout")
                self.click_until_found(Setting.BUFF_SLOT_CANCEL, ImageTemplates.BUFF_SLOT_CANCEL)
                self.click_until_found(Setting.CONFIRM_CANCEL_BUTTON, ImageTemplates.CONFIRM_CANCEL_BUTTON)

    def run(self):
        self.setup()
        while True:
            if WindowUtil.is_scroll_lock_on():
                self.start()
            else:
                logging.info("Scroll lock is off")
                self.setup()
                pauseTime = time.time()
                while not WindowUtil.is_scroll_lock_on():
                    if time.time() - pauseTime > 60:
                        logging.info("Scroll lock is off")
                    sleep(3)


if __name__ == '__main__':
    ctypes.windll.user32.SetProcessDPIAware()
    hwndMap = WindowUtil.enumerate_visible_windows()
    taskApp = TrailTaskApp(hwndMap['尘白禁区'])
    taskApp.run()
