import keyboard
import time

keyboard.hook(lambda e: print(e.to_json()))

while True:
    time.sleep(60)
