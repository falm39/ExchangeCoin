import tkinter as tk
from tkinter import Canvas, Button, Label, Entry, Toplevel, messagebox, filedialog
from PIL import Image, ImageTk, ImageGrab
import pyautogui
import time
import pytesseract
import random
import json

# Tesseract OCR için program dosyasının yolu (Windows için örnek yol)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class ScreenAreaSelector:
    def __init__(self, master, label_text, callback):
        self.master = master
        self.label_text = label_text
        self.callback = callback

        self.top = Toplevel(master)
        self.top.title(label_text)

        # Tüm ekranları kapsayan bir ekran görüntüsü al
        self.screenshot = ImageGrab.grab(all_screens=True)
        self.img = ImageTk.PhotoImage(self.screenshot)

        self.canvas = Canvas(self.top, width=self.img.width(), height=self.img.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.top.destroy()
        self.callback((self.start_x, self.start_y, end_x - self.start_x, end_y - self.start_y))

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Ayarları")

        self.coords = {
            "Filtre": None,
            "Altın": None,
            "Odun": None,
            "Cevher": None,
            "Çoklu Seçim": None,
            "Tümünü Seç": None,
            "Satın Al": None,
            "Sonuç Kontrol": None
        }

        self.create_widgets()
        self.root.bind('<Control-q>', self.stop)  # Ctrl + Q kısayolunu bağlar
        self.running = False

    def create_widgets(self):
        for idx, (text, coord) in enumerate(self.coords.items()):
            label = Label(self.root, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5)

            button = Button(self.root, text="Ayarla", command=lambda t=text: self.open_selector(t))
            button.grid(row=idx, column=1, padx=5, pady=5)

        Label(self.root, text="Döngü Aralığı (Min - Max)").grid(row=8, column=0, padx=5, pady=5)
        self.entry_loop_min = Entry(self.root, width=5)
        self.entry_loop_min.grid(row=8, column=1, padx=5, pady=5)
        self.entry_loop_max = Entry(self.root, width=5)
        self.entry_loop_max.grid(row=8, column=2, padx=5, pady=5)

        Label(self.root, text="Bekleme Süresi Aralığı (Dakika)").grid(row=9, column=0, padx=5, pady=5)
        self.entry_wait_min = Entry(self.root, width=5)
        self.entry_wait_min.grid(row=9, column=1, padx=5, pady=5)
        self.entry_wait_max = Entry(self.root, width=5)
        self.entry_wait_max.grid(row=9, column=2, padx=5, pady=5)

        self.start_button = Button(self.root, text="Başlat", command=self.start)
        self.start_button.grid(row=10, column=0, pady=10)

        self.save_button = Button(self.root, text="Kaydet", command=self.save_coords)
        self.save_button.grid(row=10, column=1, pady=10)

        self.load_button = Button(self.root, text="Yükle", command=self.load_coords)
        self.load_button.grid(row=10, column=2, pady=10)

    def open_selector(self, text):
        ScreenAreaSelector(self.root, text, lambda coords: self.set_coords(text, coords))

    def set_coords(self, label_text, coords):
        self.coords[label_text] = coords
        print(f"{label_text} koordinatları ayarlandı: {coords}")

    def start(self):
        if None in self.coords.values():
            messagebox.showwarning("Uyarı", "Lütfen tüm koordinatları ayarlayın.")
            return

        try:
            loop_min = int(self.entry_loop_min.get() or 5)
            loop_max = int(self.entry_loop_max.get() or 20)
            wait_min = int(self.entry_wait_min.get() or 5)
            wait_max = int(self.entry_wait_max.get() or 20)
        except ValueError:
            messagebox.showwarning("Uyarı", "Lütfen geçerli sayısal değerler girin.")
            return

        print("Ayarlar kaydedildi:")
        print(f"Döngü aralığı: {loop_min} - {loop_max}")
        print(f"Bekleme süresi aralığı: {wait_min} - {wait_max} dakika")
        print("Koordinatlar:")
        for key, value in self.coords.items():
            print(f"{key}: {value}")

        # Burada main_loop fonksiyonunu başlatıyoruz
        self.running = True
        self.run_main_loop(loop_min, loop_max, wait_min, wait_max)

    def stop(self, event=None):
        self.running = False
        self.root.quit()

    def save_coords(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.coords, f)
            messagebox.showinfo("Bilgi", "Koordinatlar başarıyla kaydedildi.")

    def load_coords(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as f:
                self.coords = json.load(f)
            messagebox.showinfo("Bilgi", "Koordinatlar başarıyla yüklendi.")
            print("Koordinatlar yüklendi:")
            for key, value in self.coords.items():
                print(f"{key}: {value}")

    def run_main_loop(self, loop_min, loop_max, wait_min, wait_max):
        resources = [
            {"name": "Altın", "coord": self.coords["Altın"]},
            {"name": "Odun", "coord": self.coords["Odun"]},
            {"name": "Cevher", "coord": self.coords["Cevher"]}
        ]

        while self.running:
            loop_count = random.randint(loop_min, loop_max)
            print(f"Bu döngüde tekrar sayısı: {loop_count}")

            # Başta filtreye tıklayın
            self.click_at(*self.coords["Filtre"], description="Filtre", double_click=False, long_click=True)

            for _ in range(loop_count):
                for resource in resources:
                    self.click_at(*resource["coord"], description=resource["name"])
                    self.click_at(*self.coords["Filtre"], description="Filtre", double_click=False, long_click=True) # filtreyi kapat

                    if self.check_result_exists(*self.coords["Sonuç Kontrol"]):
                        print(f"{resource['name']} için sonuç bulundu.")
                        self.select_multiple()
                        time.sleep(0.1)
                        self.select_all()
                        time.sleep(0.1)
                        self.buy()
                        time.sleep(0.1)
                        self.select_all()
                        time.sleep(0.1)
                        self.select_multiple()
                        time.sleep(0.1)
                        self.click_at(*self.coords["Filtre"], description="Filtre", double_click=False, long_click=True)
                        break
                    else:
                        print(f"{resource['name']} için sonuç bulunamadı. Sonraki kaynağa geçiliyor.")
                        self.click_at(*self.coords["Filtre"], description="Filtre", double_click=False, long_click=True)
                        time.sleep(0.1)

            wait_time = random.randint(wait_min, wait_max)  # Dakikayı saniyeye çevir
            print(f"{loop_count} tekrar tamamlandı. {wait_time // 60} saniye bekleniyor.")
            self.click_at(*self.coords["Filtre"], description="Filtre")
            time.sleep(wait_time)

    def click_at(self, x, y, width, height, description="", double_click=False, long_click=False):
        random_x = random.randint(x, x + width)
        random_y = random.randint(y, y + height)
        print(f"Tıklanıyor: {description} ({random_x}, {random_y})")
        pyautogui.moveTo(random_x, random_y, duration=0.1)
        if double_click:
            pyautogui.doubleClick()
        elif long_click:
            pyautogui.mouseDown()
            pyautogui.mouseUp()
        else:
            pyautogui.click()

    def check_result_exists(self, x, y, width, height):
        # OCR işlemi için alınan ekran görüntüsünün siyah olmamasını sağlamak için, 
        # ekranın doğru şekilde yakalandığından emin olun.
        print(f"Kontrol ediliyor: ({x}, {y}, {width}, {height})")
        region = ImageGrab.grab(bbox=(x, y, x + width, y + height), all_screens=True)
        region.save("screenshot.png")  # Ekran görüntüsünü kaydet
        text = pytesseract.image_to_string(region, lang='eng')
        print(f"OCR tarafından okunan metin: {text}")

        if "100" in text:
            return True
        else:
            return False

    def select_multiple(self):
        self.click_at(*self.coords["Çoklu Seçim"], description="Çoklu seçim")

    def select_all(self):
        self.click_at(*self.coords["Tümünü Seç"], description="Tümünü seç")

    def buy(self):
        self.click_at(*self.coords["Satın Al"], description="Satın al")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
