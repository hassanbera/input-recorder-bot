import ctypes
import time

# Windows API yapılandırmaları
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def hold_key(hexKeyCode, duration):
    """
    Belirtilen tuşa belirtilen süre boyunca basılı tutar.
    Args:
        hexKeyCode: Tuşun hexadecimal kodu.
        duration: Tuşun basılı kalacağı süre (saniye cinsinden).
    """
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    time.sleep(duration)
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def mouse_click(duration=0.1):
    """
    Fare sol tuşuna tıklama işlemini gerçekleştirir.
    Args:
        duration: Tıklama süresi (saniye cinsinden).
    """
    extra = ctypes.c_ulong(0)
    mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))  # Sol tuş basma
    x = Input(ctypes.c_ulong(0), Input_I(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    time.sleep(duration)
    mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))  # Sol tuş bırakma
    x = Input(ctypes.c_ulong(0), Input_I(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def replay_records(records):
    """
    Kaydedilen girdileri tekrar uygular.
    Args:
        records (list): Kaydedilen girdilerin listesi.
    """
    for inp in records:
        if inp[0] == 'key_press':  # Tuş basma girdisi
            scancode = ord(inp[1])  # Karakteri scancode’a çevir
            hold_key(scancode, inp[2])  # Tuşa belirtilen süre boyunca bas
            print(f"Tuş basıldı: {inp[1]} (Süre: {inp[2]:.2f} saniye)")
        elif inp[0] == 'mouse_click':  # Mouse tıklama girdisi
            x, y = inp[1]
            mouse_click(0.1)  # Mouse tıklamasını uygula
            print(f"Mouse tıklaması: ({x}, {y}) koordinatında uygulandı.")
        time.sleep(0.1)  # Bir sonraki girdiye geçmeden önce bekleme
