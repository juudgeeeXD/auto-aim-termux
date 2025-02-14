import cv2
import numpy as np
import os
import time

# Konfigurasi
SCREENSHOT_PATH = "/sdcard/screen.png"  # Lokasi screenshot di HP
TAP_X, TAP_Y = 500, 500  # Koordinat default untuk menembak

# Fungsi untuk mengambil screenshot dari HP ke Termux
def capture_screen():
    os.system(f"adb shell screencap -p {SCREENSHOT_PATH}")
    os.system("adb pull /sdcard/screen.png screen.png")

def detect_enemy(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        return (x + w // 2, y + h // 5)  # Kembaliin koordinat kepala musuh
    return None

def auto_aim():
    capture_screen()
    enemy_pos = detect_enemy("screen.png")
    if enemy_pos:
        x, y = enemy_pos
        print(f"Menembak di posisi: {x}, {y}")
        os.system(f"adb shell input tap {x} {y}")
    else:
        print("Musuh tidak ditemukan.")

while True:
    auto_aim()
    time.sleep(0.1)  # Loop setiap 100ms
