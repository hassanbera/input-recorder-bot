from recorder import KeyboardMouseRecorder
from replayer import replay_records
import os

def main():
    """
    Kullanıcı seçim yapar:
    - 1: Girdileri kaydet ve dosyaya yaz.
    - 2: Kaydedilen girdileri uygula.
    """
    print("Seçim yapınız:")
    print("1: Girdileri kaydet")
    print("2: Kaydedilen girdileri uygula")
    choice = input("Seçiminiz (1/2): ")

    if choice == "1":
        # Kayıt işlemini başlat
        recorder = KeyboardMouseRecorder()
        recorder.start_recording()  # Kaydı başlat

        # Kaydedilen girdileri al
        records = recorder.get_records()
        print(records)  # Konsolda kaydedilen girdiler gösterilir

        # Eğer kayıt varsa dosyaya yaz
        if records:
            with open("recorded_inputs.txt", "w") as file:
                for record in records:
                    file.write(f"{record}\n")
            print("Kayıt tamamlandı ve 'recorded_inputs.txt' dosyasına yazıldı.")
        else:
            print("Herhangi bir girdi kaydedilmedi.")

    elif choice == "2":
        # Kaydedilen girdileri tekrar uygula
        if os.path.exists("recorded_inputs.txt"):
            with open("recorded_inputs.txt", "r") as file:
                records = [eval(line.strip()) for line in file]

            print("Kaydedilen girdiler uygulanıyor...")
            replay_records(records)  # Kaydedilen girdileri uygula
        else:
            print("Kaydedilen girdiler bulunamadı! Lütfen önce kayıt yapın.")
    else:
        print("Geçersiz seçim. Lütfen 1 veya 2 giriniz.")

if __name__ == "__main__":
    main()

