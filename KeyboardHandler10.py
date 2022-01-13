from pynput import keyboard
from win10toast import ToastNotifier

lastkeyf24 = False
toaster = ToastNotifier()

def keyboard_listener():
    global lastkeyf24
    global listener

    def win32_event_filter(msg, data):
        # - verifica se a tecla esta a ser pressionada ou solta
        if msg == 256:
            # - verifica se a tecla pressionada é o "F24"
            if (lastkeyf24 == False):
                keyBoardSelectionByF(data)
            else:
                KeyboardSelected(data)
        return True

    def keyBoardSelectionByF(data):
        global lastkeyf24
        # Verifica o "data.vkCode" Se for F24
        match data.vkCode:
            case 135:  # F24
                listener._suppress = True
                lastkeyf24 = True
            case _:
                listener._suppress = False

    def KeyboardSelected(data):
        global lastkeyf24
        NextKey_F24(data.vkCode) 
        listener._suppress = True
        lastkeyf24 = False  # set last key pressed as NOT "F24"

    def NextKey_F24(KeyPressed):
        global lastkeyf24
        # print(KeyPressed)
        match KeyPressed:
            case 65:
                print(KeyPressed)
            case _:
                print("key number '" + str(KeyPressed) + "' not implemented")

    def WinToast(KeyPressed):
        toaster.show_toast("Example two", "a tecla foi " + str(KeyPressed), icon_path=None, duration=5, threaded=True)

    return keyboard.Listener(win32_event_filter=win32_event_filter, suppress=False)

listener = keyboard_listener()

if __name__ == '__main__':
    with listener as ml:
        ml.join()