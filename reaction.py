import time

import win32gui
from pymouse import PyMouse
from pykeyboard import PyKeyboard

k = PyKeyboard()
m = PyMouse()


def get_app_name():
    appName = win32gui.GetWindowText(win32gui.GetForegroundWindow())  # 获取当前最靠前并且是激活得窗口不用传参数
    print(appName)
    return appName


def get_app_index():
    name = get_app_name()
    if "照片" in name:
        return 1
    elif "PowerPoint" in name:
        return 2
    else:
        print("未在支持程序内执行手势")
        return 99


def catch():
    print('Done：抓取')


def tap():
    m.click(m.position()[0], m.position()[1])
    print('Done：点击')


def rotate(app_index: int):
    if app_index == 1:
        k.press_key(k.control_key)
        k.tap_key('r')
        k.release_key(k.control_key)
    print('Done：旋转')


def move(app_index: int):
    if app_index == 1 or app_index == 2:
        k.tap_key(k.right_key)
    print('Done：平移')


def zoom(app_index: int, signal: str):
    if app_index == 1:
        k.press_key(k.control_key)
        k.tap_key(signal)
        k.release_key(k.control_key)
    elif app_index == 2:
        k.tap_key(signal)
    print('Done：', "缩放" if signal == '-' else "放大")


def screenshot():
    k.press_key(k.windows_l_key)
    k.tap_key(k.print_screen_key)
    k.release_key(k.windows_l_key)
    print("Done：截图")


class Reaction:
    def __init__(self):
        pass

    def react(self, target: str):
        appIndex = get_app_index()
        if target == "点击":
            tap()
        elif target == "平移":
            move(appIndex)
        elif target == "旋转":
            rotate(appIndex)
        elif target == "抓取":
            catch()
        elif target == "缩放":
            zoom(appIndex, '-')
        elif target == "放大":
            zoom(appIndex, '+')
        elif target == "截图":
            screenshot()
        else:
            print("未添加此动作")


if __name__ == '__main__':
    time.sleep(3)
    react = Reaction()
    react.react("放大")

