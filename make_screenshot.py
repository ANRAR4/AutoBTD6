from helper import *

if not exists("screenshots"):
    os.mkdir("screenshots")

filename = "screenshots/" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
cv2.imwrite(filename, np.array(pyautogui.screenshot())[:, :, ::-1].copy())
