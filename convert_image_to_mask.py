from helper import *

# converts all red pixels to white, all other to black

argv = np.array(sys.argv)
if len(argv) < 2:
    print("Usage: py " + argv[0] + " <filename>")
    exit()
if not str(argv[1]).endswith('.png'):
    print("Format must be .png!")
    exit()
if not exists(argv[1]):
    print("Image not found!")
    exit()

img = cv2.imread(argv[1])

h = img.shape[0]
w = img.shape[1]

white = np.array([255, 255, 255])
black = np.array([0, 0, 0])
red = np.array([0, 0, 255])

for y in range(0, h):
    for x in range(0, w):
        if (img[y][x] == red).all():
            img[y][x] = white
        else:
            img[y][x] = black
cv2.imwrite(str(argv[1]).replace('.png', '_masked.png'), img)