#!/usr/bin/env python3

import time
import ctypes
from ctypes import wintypes
import struct
import threading


# --- Windows API Setup ---

# User32\SendMessage
SendMessage = ctypes.windll.user32.SendMessageW
SendMessage.restype = wintypes.LPARAM # LRESULT
SendMessage.argtypes = (
    wintypes.HWND,   # hWnd
    wintypes.UINT,   # Msg
    wintypes.WPARAM, # wParam
    wintypes.LPARAM, # lParam
)

# User32\PostMessage
PostMessage = ctypes.windll.user32.PostMessageW
PostMessage.restype = SendMessage.restype

# User32\CreateWindowEx
CreateWindowEx = ctypes.windll.user32.CreateWindowExW
CreateWindowEx.restype = wintypes.HWND
CreateWindowEx.argtypes = (
    wintypes.DWORD,     # dwExStyle
    wintypes.LPWSTR,    # lpClassName
    wintypes.LPWSTR,    # lpWindowName
    wintypes.DWORD,     # dwStyle
    wintypes.INT,       # X
    wintypes.INT,       # Y
    wintypes.INT,       # nWidth
    wintypes.INT,       # nHeight
    wintypes.HWND,      # hWndParent
    wintypes.HWND,      # hMenu
    wintypes.HINSTANCE, # hInstance
    wintypes.LPVOID,    # lpParam
)

# User32\GetMessage
GetMessage = ctypes.windll.user32.GetMessageW
GetMessage.restype = wintypes.BOOL
GetMessage.argtypes = (
    wintypes.LPMSG, # lpMsg
    wintypes.HWND,  # hWnd
    wintypes.UINT,  # wMsgFilterMin
    wintypes.UINT,  # wMsgFilterMax
)

# User32\TranslateMessage
TranslateMessage = ctypes.windll.user32.TranslateMessage
TranslateMessage.restype = wintypes.BOOL
TranslateMessage.argtypes = (wintypes.LPMSG,)

# User32\DispatchMessage
DispatchMessage = ctypes.windll.user32.DispatchMessageW
DispatchMessage.restype = wintypes.LPARAM # LRESULT

# Constants
TOOLTIPS_CLASSW = "tooltips_class32"
TTF_TRACK = 0x20
WM_USER = 0x400
TTM_ADDTOOLW = WM_USER + 50
TTM_TRACKACTIVATE = WM_USER + 17
TTM_TRACKPOSITION = WM_USER + 18
TTS_NOPREFIX = 0x2
TTS_ALWAYSTIP = 0x1
WS_EX_TOPMOST = 0x8


# --- Class Definitions ---

class ToolTip():
    class TOOLINFOW(ctypes.Structure):
        _fields_ = [
            ("cbSize",     wintypes.UINT),
            ("uFlags",     wintypes.UINT),
            ("hwnd",       wintypes.HWND),
            ("uId",        wintypes.LPVOID),
            ("rect",       wintypes.RECT),
            ("hinst",      wintypes.HINSTANCE),
            ("lpszText",   wintypes.LPWSTR),
            ("lParam",     wintypes.LPARAM),
            ("lpReserved", wintypes.LPVOID),
        ]

    def __init__(self, text, x=0, y=0):
        # Save configuration data
        self.text = text
        self.x, self.y = x, y

        # Start the creation thread
        self.evt_created = threading.Event()
        threading.Thread(target=self.create, daemon=True).start()

        # Wait for the tooltip to be created
        self.evt_created.wait()

    def create(self):
        # Create a window to house the tooltip
        self.hwnd = CreateWindowEx(
            WS_EX_TOPMOST,   # DWORD     dwExStyle
            TOOLTIPS_CLASSW, # LPCWSTR   lpClassName
            None,            # LPCWSTR   lpWindowName
            TTS_NOPREFIX |
            TTS_ALWAYSTIP,   # DWORD     dwStyle
            0,               # int       X
            0,               # int       Y
            0,               # int       nWidth
            0,               # int       nHeight
            None,            # HWND      hWndParent
            None,            # HWND      hMenu
            None,            # HINSTANCE hInstance
            None,            # LPVOID    lpParam
        )

        # Create the tooltip information
        ti = self.TOOLINFOW(ctypes.sizeof(self.TOOLINFOW))
        ti.uFlags = TTF_TRACK
        ti.lpszText = self.text

        # Configure the window with the tooltip data
        SendMessage(self.hwnd, TTM_ADDTOOLW, 0, ctypes.addressof(ti))
        self.update_pos(self.x, self.y, True)
        SendMessage(self.hwnd, TTM_TRACKACTIVATE, 1, ctypes.addressof(ti))

        # Raise the tooltip created event
        self.evt_created.set()

        # Process messages for that window
        x = wintypes.MSG()
        while True:
            bRet = GetMessage(ctypes.byref(x), self.hwnd, 0, 0)
            if bRet in (0, -1): break
            TranslateMessage(ctypes.byref(x))
            DispatchMessage(ctypes.byref(x))

    def destroy(self):
        PostMessage(self.hwnd, 0x10, 0, 0)

    def update_pos(self, x, y, wait=False):
        self.x, self.y = x, y
        long_words = struct.unpack('L', struct.pack('hh', x, y))[0]
        Message = SendMessage if wait else PostMessage
        Message(self.hwnd, TTM_TRACKPOSITION, 0, long_words)


# --- Entry Point ---

def main():
    GetCursorPos = ctypes.windll.user32.GetCursorPos
    GetCursorPos.restype = wintypes.BOOL
    GetCursorPos.argtypes = (wintypes.LPPOINT,)

    # Create a tooltip
    tt = ToolTip('Hello World!')

    # Make tooltip follow cursor
    pt = wintypes.POINT()
    for i in range(100):
        GetCursorPos(ctypes.byref(pt))
        tt.update_pos(pt.x + 8, pt.y + 16)
        time.sleep(0.05)

    # Destroy the tooltip
    tt.destroy()

    # Wait forever
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
