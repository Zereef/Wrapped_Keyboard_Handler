from pynput import keyboard
from win10toast import ToastNotifier
from infi.systray import SysTrayIcon
import pyautogui as pya
import requests



def on_quit_callback(systray):
    systray.shutdown()

def keyboard_listener():
    global lastkeyf24
    global listener

    def win32_event_filter(msg, data):
        global lastkeyf24
        if msg == 256: # verifica se a tecla esta a ser pressionada ou solta
            if (lastkeyf24 == False):
                match data.vkCode:
                    case 135: # verifica se a tecla pressionada Ã© o "F24"
                        listener._suppress = True
                        lastkeyf24 = True
                    case _:
                        listener._suppress = False
            else:
                lastkeyf24 = False  # Removes the next key replacement
                listener._suppress = True
                key_Replacement(data.vkCode)                 
            
        return True

    return keyboard.Listener(win32_event_filter=win32_event_filter, suppress=True)

def key_Replacement(KeyPressed):
    match KeyPressed:
        case 65: # key pressed is A (layer 1)
            # Self_Request("http://localhost:6969/mute")
            print(KeyPressed)
        case 66: # key pressed is B (layer 1)
            print(KeyPressed)
        case 67: # key pressed is C (layer 1)
            print(KeyPressed)
        case 68: # key pressed is D (layer 1)
            print(KeyPressed)
        case 69: # key pressed is E (layer 1)
            pya.hotkey('ctrl', 'c')
            listener._suppress = True
        case 70: # key pressed is F (layer 1)
            # Self_Request("http://localhost:6969/mute")
            print(KeyPressed)
        case 71: # Virtual layer 1 "G" Visible C
            pya.hotkey('ctrl', 'v')
            listener._suppress = True
        case 72: # key pressed is H (layer 1)
            print(KeyPressed)
        case _:
            print("key number '" + str(KeyPressed) + "' not implemented")

def WinToast(KeyPressed):
        toaster.show_toast("Example two", "a tecla foi " + str(KeyPressed), icon_path=None, duration=5, threaded=True)

def Self_Request(url):
    r = requests.get(url)
    print(r.text)

lastkeyf24 = False
toaster = ToastNotifier()

menu_options = (("Close", None, on_quit_callback),)
systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)

listener = keyboard_listener()

if __name__ == '__main__':
    # os.system('adb tcpip 5555')
    # os.system('adb connect 192.168.1.99')
    print("first run")
    systray.start()
    with listener as ml:
        ml.join()