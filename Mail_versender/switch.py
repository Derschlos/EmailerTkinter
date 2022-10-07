import win32gui
import re
from time import sleep

def switch(name):
    windows =[]
    def window_enumeration_handler(hwnd, windows):
        """Add window title and ID to array."""
        windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(window_enumeration_handler, windows)
    for window in windows:
        winNum, winName = window
        if re.search(name,str(winName)) is not None:
            win32gui.SetForegroundWindow(winNum)
            sleep(1)
            return winNum
