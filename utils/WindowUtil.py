import win32api
import win32con
import win32gui


class WindowUtil:
    @staticmethod
    def enumerate_visible_windows():
        windows = {}  # 用于存储窗口标题和句柄的字典

        # 定义回调函数
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):  # 检查窗口是否可见
                window_title = win32gui.GetWindowText(hwnd)  # 获取窗口标题
                if window_title:  # 如果窗口标题不为空
                    windows[window_title] = hwnd  # 添加到字典中
            return True

        # 枚举所有窗口
        win32gui.EnumWindows(callback, None)

        return windows

    @staticmethod
    def is_scroll_lock_on():
        return win32api.GetKeyState(win32con.VK_SCROLL) & 0x0001
