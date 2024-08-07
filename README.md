# ExchangeCoin
Call of dragons exchange coins for gold, wood and stone.

Python Kurulumu // Install python
Python'ı indirin: https://www.python.org/downloads/

Gerekli kütüphaneler: // Necessary libraries
```
pip install Pillow
pip install pyautogui
pip install pytesseract
```

Tesseract OCR Kurulumu // Installation of Tesseract OCR
https://github.com/UB-Mannheim/tesseract/wiki

Kurulum yolunu pytesseract.pytesseract.tesseract_cmd değişkeninde belirtin: // Don't forget to change destination of files on pytesseract.pytesseract.tesseract_cmd variable.

```
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
```
