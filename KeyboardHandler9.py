from pynput import keyboard

lastkeyf20 = False


def keyboard_listener():
    global listener

    def win32_event_filter(msg, data):
        global lastkeyf20
        # - verifica se a tecla esta a ser pressionada ou solta
        if msg == 256:
            if (lastkeyf20 == False):
                # if data.vkCode == 131:
                # - verifica se a tecla pressionada é o "F20"
                if data.vkCode in range(131, 135):
                    listener._suppress = True
                    lastkeyf20 = True
                else:
                    listener._suppress = False
            else:
                print(data.vkCode)
                listener._suppress = True
                lastkeyf20 = False  # set last key pressed as NOT "F20"
        return True

    return keyboard.Listener(win32_event_filter=win32_event_filter, suppress=False)

listener = keyboard_listener()


if __name__ == '__main__':
    with listener as ml:
        ml.join()
