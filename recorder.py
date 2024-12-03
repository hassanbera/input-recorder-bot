from pynput import keyboard, mouse
import time

class KeyboardMouseRecorder:
    """
    Klavye ve fare girdilerini kaydeden sınıf.
    """
    def __init__(self):
        self.records = []  # Girdiler için liste
        self.press_times = {}  # Tuşların basılma zamanları
        self.is_recording = True  # Kaydı devam ettirme durumu

    def on_key_press(self, key):
        """
        Tuş basıldığında çağrılır.
        """
        try:
            # ESC tuşu tetikleyici olarak kullanılır
            if key == keyboard.Key.esc:
                print("ESC tuşuna basıldı. Kayıt durduruluyor...")
                self.is_recording = False
                return False  # Listener'ı durdur
            key_name = key.char if hasattr(key, 'char') else str(key)
            self.press_times[key_name] = time.time()  # Basılma zamanını kaydet
        except Exception as e:
            print(f"Tuş kaydedilemedi: {e}")

    def on_key_release(self, key):
        """
        Tuş bırakıldığında çağrılır.
        """
        try:
            # ESC tuşu kaydedilmeyecek
            if key == keyboard.Key.esc:
                return
            key_name = key.char if hasattr(key, 'char') else str(key)
            press_time = self.press_times.pop(key_name, None)
            if press_time is not None:
                duration = time.time() - press_time
                self.records.append(('key_press', key_name, duration))  # Listeye ekle
                print(f"Tuş: {key_name}, Süre: {duration:.2f} saniye")
        except Exception as e:
            print(f"Tuş bırakma kaydedilemedi: {e}")

    def on_mouse_click(self, x, y, button, pressed):
        """
        Mouse tıklandığında çağrılır.
        """
        if pressed and self.is_recording:
            self.records.append(('mouse_click', (x, y), time.time()))
            print(f"Mouse tıklaması: ({x}, {y}) koordinatında")

    def start_recording(self):
        """
        Kayıt işlemine başlar.
        """
        print("Kayıt başlıyor... 'ESC' tuşuna basarak kaydı durdurabilirsiniz.")
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release) as key_listener, \
             mouse.Listener(on_click=self.on_mouse_click) as mouse_listener:
            key_listener.join()  # Klavye dinleyicisini başlat

    def get_records(self):
        """
        Kaydedilen girdileri döner.
        """
        return self.records
