import cv2
import numpy as np
import pyautogui
import time
from cryptography.hazmat.primitives import hashes

# Konfigurasi auto-aim
AIM_THRESHOLD = 0.8  # Tingkat kecocokan yang dianggap musuh
DELAY_BETWEEN_SHOTS = 0.1  # Delay antar tembakan
HEAD_OFFSET_Y = -20  # Offset ke kepala musuh

# Fungsi untuk mengambil screenshot
def capture_screen():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Fungsi untuk mendeteksi musuh
def detect_enemy(frame, template_path="enemy_template.png"):
    template = cv2.imread(template_path, 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= AIM_THRESHOLD:
        head_pos = (max_loc[0], max_loc[1] + HEAD_OFFSET_Y)  # Sesuaikan ke kepala
        return head_pos
    return None

# Fungsi untuk menempelkan aim ke kepala musuh saat menembak
def aim_and_shoot(target_pos):
    screen_width, screen_height = pyautogui.size()
    x, y = target_pos
    pyautogui.moveTo(x, y, duration=0.02)  # Lebih cepat menuju kepala
    pyautogui.click()  # Tembak
    time.sleep(DELAY_BETWEEN_SHOTS)

# Loop utama
while True:
    frame = capture_screen()
    target = detect_enemy(frame)
    
    if target and pyautogui.mouseDown():  # Menempelkan aim saat menembak
        aim_and_shoot(target)
    
    time.sleep(0.05)  # Delay kecil untuk menghindari penggunaan CPU tinggi
