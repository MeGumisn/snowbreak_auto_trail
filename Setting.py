import cv2


def make_setting(left: int, top: int, width: int, height: int):
    return {"left": left, "top": top, "width": width, "height": height}


def read_img(filename):
    return cv2.imread(filename, cv2.IMREAD_GRAYSCALE)


# 主页面开始战斗按钮
HOME_PAGE = make_setting(1500, 400, 420, 210)
# 悖论迷宫按钮
MAZE_BUTTON = make_setting(1450, 230, 415, 150)
# 验证战场按钮
BATTLE_GROUND = make_setting(10, 140, 300, 120)
# 增益试炼按钮
TRAIL_BUTTON = make_setting(1515, 910, 410, 200)
# 试炼循环
# 厄险关卡按钮
EXTREME_TRAIL = make_setting(1380, 275, 300, 130)
# 开始作战按钮
START_BUTTON = make_setting(1600, 975, 325, 135)
# 确认 buff 按钮
CONFIRM_BUFF_BUTTON = make_setting(750, 980, 450, 120)
# 单人buff 栏位
BUFF_SLOT = make_setting(1170, 275, 570, 555)
# 确认单人buff 按钮
BUFF_SLOT_CONFIRM = make_setting(1400, 985, 355, 100)
# 丢弃单人buff 按钮
BUFF_SLOT_CANCEL = make_setting(100, 985, 355, 100)
# 确认丢弃BUFF按钮
CONFIRM_CANCEL_BUTTON = make_setting(1275,750,415,130)
# 退出按钮
QUIT_BUTTON = make_setting(790, 970, 430, 120)


class ImageTemplates:
    # 主页面开始战斗按钮
    HOME_PAGE = read_img("templates/HomePage.png")
    # 悖论迷宫按钮
    MAZE_BUTTON = read_img("templates/MazeButton.png")
    # 验证战场按钮
    BATTLE_GROUND = read_img("templates/BattleGround.png")
    # 增益试炼按钮
    TRAIL_BUTTON = read_img("templates/TrailButton.png")
    # 试炼循环
    # 厄险关卡按钮
    EXTREME_TRAIL = read_img("templates/ExtremeTrail.png")
    # 开始作战按钮
    START_BUTTON = read_img("templates/StartButton.png")
    # 确认 buff 按钮
    CONFIRM_BUFF_BUTTON = read_img("templates/ConfirmBuffButton.png")
    # 单人buff 栏位
    BUFF_SLOT = read_img("templates/BuffSlot.png")
    # 确认单人buff 按钮
    BUFF_SLOT_CONFIRM = read_img("templates/BuffSlotConfirm.png")
    # 丢弃单人buff 按钮
    BUFF_SLOT_CANCEL = read_img("templates/BuffSlotCancel.png")
    # 确认丢弃BUFF按钮
    CONFIRM_CANCEL_BUTTON = read_img("templates/ConfirmCancelButton.png")
    # 退出按钮
    QUIT_BUTTON = read_img("templates/QuitButton.png")
