from helper import *
from replay import getResolutionDependentData

argv = np.array(sys.argv)
if len(argv) < 2:
    print("Usage: py " + argv[0] + " <filename>")
    exit()
if not str(argv[1]).endswith(".png"):
    print("Format must be .png!")
    exit()
if not exists(argv[1]):
    print("Image not found!")
    exit()

img = cv2.imread(argv[1])

h = img.shape[0]
w = img.shape[1]

data = getResolutionDependentData((w, h))

print("screen " + recognizeScreen(img, data["comparisonImages"], True).name + "!")