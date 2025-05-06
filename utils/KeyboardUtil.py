import logging
from time import sleep

import win32api
import win32con
import win32gui


class KeyboardUtil:
    @staticmethod
    def foreground_window(hwnd):
        current = win32gui.GetForegroundWindow()
        if current and not current == hwnd:
            win32gui.SetForegroundWindow(hwnd)

    @staticmethod
    def move_mouse(hwnd, x, y):
        KeyboardUtil.foreground_window(hwnd)
        # 将屏幕坐标转换为窗口坐标
        screen_x, screen_y = win32gui.ClientToScreen(hwnd, (x, y))
        # 移动鼠标到指定位置
        win32api.SetCursorPos((screen_x, screen_y - 30))
        return screen_x, screen_y

    @staticmethod
    def click_mouse(hwnd, x, y, button='left'):
        screen_x, screen_y = KeyboardUtil.move_mouse(hwnd, x, y)
        logging.info(f"Click mouse at {screen_x}, {screen_y}")
        if button == 'left':
            # 模拟鼠标左键按下和弹起
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
            sleep(0.03)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
        elif button == 'right':
            # 发送鼠标右键按下消息
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, screen_x, screen_y, 0, 0)
            sleep(0.03)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, screen_x, screen_y, 0, 0)

    @staticmethod
    def press_key(hwnd, key_code, delay=0.03):
        # 发送按键按下消息
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
        sleep(delay)
        # 发送按键释放消息
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, key_code, 0)

    @staticmethod
    def press_alt_3(hwnd):
        # 按下alt键
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_MENU, 0)
        # 按下主键盘3
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, ord('3'), 0)
        sleep(0.03)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_MENU, 0)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, ord('3'), 0)
