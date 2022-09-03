from helper import *
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import keras

ocr_model = keras.models.load_model('btd6_ocr_net.h5')

locateImages = {}
locateImages['numbers'] = []
locateImages['remove_obstacle_confirm_button'] = cv2.imread('images/remove_obstacle_confirm_button.png')
for i in range(0, 10):
    locateImages['numbers'].append(cv2.imread('images/' + str(i) + '.png'))

# custom ocr:

def custom_ocr(image):
    numbers = []

    for i in range(0, 10):
        result = cv2.matchTemplate(locateImages['numbers'][i], image, cv2.TM_SQDIFF_NORMED)
        it = np.nditer(result, flags=['multi_index'])
        for x in it:
            if x < 0.03:
                # print("%d at %s; %f accuracy" % (i, it.multi_index, x))
                numbers.append([i, it.multi_index, x])

    numbers.sort(key = lambda x: x[1][1])
    number = 0
    lastPos = -100
    for x in numbers:
        if x[1][1] > lastPos + 15:
            number = number * 10 + x[0]
            lastPos = x[1][1]

    return int(number)

def new_custom_ocr(img):
    h = img.shape[0]
    w = img.shape[1]

    resolution = pyautogui.size()

    white = np.array([255, 255, 255])
    black = np.array([0, 0, 0])

    for y in range(0, h):
        for x in range(0, w):
            if not (img[y][x] == white).all():
                img[y][x] = black
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    chrImages = []
    chrImagesMinX = {}
    chrs = {}

    for c in cnts:
        minX = c[0][0][0]
        minY = c[0][0][1]
        maxX = c[0][0][0]
        maxY = c[0][0][1]
        for point in c:
            if point[0][0] < minX:
                minX = point[0][0]
            if point[0][0] > maxX:
                maxX = point[0][0]
            if point[0][1] < minY:
                minY = point[0][1]
            if point[0][1] > maxY:
                maxY = point[0][1]
        # images.append()
        chrImg = img[minY:maxY, minX:maxX]

        if chrImg.shape[0] >= 25 * resolution[0] / 2560 and chrImg.shape[0] <= 60 * resolution[0] / 2560 and chrImg.shape[1] >= 15 * resolution[1] / 1440 and chrImg.shape[1] <= 40 * resolution[1] / 1440:
            chrImg = cv2.resize(chrImg, (50, 50))
            chrImg = cv2.copyMakeBorder(chrImg, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=(0, 0, 0))
            chrImg = chrImg[:,:,0]

            for y in range(0, 60):
                for x in range(0, 60):
                    chrImg[y][x] = int(chrImg[y][x] / 255)

            chrImages.append([minX, chrImg])

    chrImages.sort(key=lambda item: item[0])
    # ignore entries after gap(e. g. explosion particles)
    filteredChrImages = []
    currentX = 0
    for entry in chrImages:
        if currentX + 50 >= entry[0]:
            currentX = entry[0]
            filteredChrImages.append(entry)
    # minXs = list(map(lambda item: item[0], chrImages))
    if len(filteredChrImages) == 0:
        return -1
    chrImages = list(map(lambda item: item[1], filteredChrImages))
    chrImages = np.array(chrImages)
    
    predictions = ocr_model.predict(chrImages, verbose=0)

    number = 0

    for prediction in predictions:
        number = number * 10 + np.argmax(prediction)

    return number

    # print(chrImages)

    # print(chrImages)
    # print(chrImages[:,0])

    # chrImagesMinX = dict(sorted(chrImagesMinX.items(), key=lambda item:item[1]))
    # i = 0
    # for index in chrImagesMinX:
    #     cv2.imwrite('digits/' + matches.group('number')[i] + '_' + str(digitCount[int(matches.group('number')[i])]) + '.png', chrImages[index])
    #     digitCount[int(matches.group('number')[i])] += 1
    #     i += 1