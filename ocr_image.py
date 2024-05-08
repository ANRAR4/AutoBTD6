from ocr import custom_ocr
from replay import *

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
segmentCoordinates = data["segmentCoordinates"]

images = [
    img[
        segmentCoordinates[segment][1] : segmentCoordinates[segment][3],
        segmentCoordinates[segment][0] : segmentCoordinates[segment][2],
    ]
    for segment in segmentCoordinates
]

print(f"detected value: {custom_ocr(images[2], resolution = (w, h))}")

cv2.imwrite(str(argv[1]).replace(".png", "_area.png"), images[2])
