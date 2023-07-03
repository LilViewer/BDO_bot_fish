import numpy as np
import cv2
import pytesseract
import mss.tools
from mss import tools
from time import sleep, perf_counter
from threading import Timer
from InterceptionWrapper import InterceptionMouseState,InterceptionMouseStroke
from  AutoHotPy  import  AutoHotPy
from ctypes  import *

#с каким монитором работаем
monitor=0

# Монтирование координат под разрешение экрана
x1, y1 = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

x2,y2 = 1280,720

x, y = (x1 - x2) // 2, (y1 - y2) // 2

#координаты для скриншотов под каждую задачу
expectationCord = {"top": y + 53, "left": x + 631, "width": 57, "height": 31,"mon": monitor,}
miniGameOneCord = {"top": y+268, "left":x+680, "width": 102, "height": 13,"mon": monitor,}
miniGameTwoCord = {"top": y+320, "left":x+508, "width": 270, "height": 40,"mon": monitor,}
miniGameThreeCord = {"top": y+270, "left":x+483, "width": 311, "height": 61,"mon": monitor,}
CheckStrengthCord = {"top": y+146, "left":x+1003, "width": 12, "height": 14,"mon": monitor,}
CheckInventoryCord = {"top": y+175, "left":x+1230, "width": 36, "height": 13,"mon": monitor,}
SearchNipCord = {"top": y+127, "left":x+667, "width": 344, "height": 130,"mon": monitor,}


#Шаблоны для сравнения
CheckStrenghtShablon = cv2.imread('Images/CheckStrenght.png')
SerchToShablonShablon = cv2.imread('Images/SerchToShablon.png')

#Переключатель повтора
repeat = True

#подключение библиотеки pytesseract для распознования текста
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

#Вкл/Выкл бега по нипам(торг, ремонт, обратно к точке рыбалки)
Nips = True

#Кол-во слотов когда бежать на продажу
inventary = 35



def stack_operation(cord):
    with mss.mss() as sct:
        img = sct.grab(cord)  # Делаю скриншот
        img = tools.to_png(img.rgb, img.size)  # Кодирую в байты
        img = np.frombuffer(img, np.uint8)  # Преобразую байты в numpy-массив
        return cv2.imdecode(img, cv2.IMREAD_COLOR)  # Перевожу в понятный cv2 формат

def start(autohopty):
    start = perf_counter()
    # sleep(.2)
    autohopty.SPACE.press()
    print(f'{perf_counter() - start}')

def enableStart(autohotpy,event):
    print('enableStart')
    start = perf_counter()
    sleep(4)
    print(f'{perf_counter() - start}')
    autohotpy.run(superCombo, event)


def SerchToShablon()->bool:
    screen = stack_operation(miniGameOneCord)

    res = cv2.matchTemplate(SerchToShablonShablon, screen, cv2.TM_CCOEFF_NORMED) == 1

    return bool(res)


def TextToScreen(current_operation,text:str)->str:
    screen = stack_operation(current_operation)
    img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('s',img)
    # cv2.waitKey(1)
    text = pytesseract.image_to_string(img, config=f'--psm 8 --oem 3 -c tessedit_char_whitelist={text}')#--psm 8
    # print(text)
    return text


def expectation(autohopty):
    start = perf_counter()
    while True:

        text = TextToScreen(expectationCord, 'Space')
        # print(text)
        match text:
            case 'Space\n':
                autohopty.SPACE.press()
                print(f'{perf_counter() - start}')
                break




def miniGameOne(autohotpy):
    start = perf_counter()
    while True:
        match SerchToShablon():
            case res if not res:
                autohotpy.SPACE.press()
                print(f'{perf_counter() - start}')
                break

def miniGameTwo(autohotpy):
    start = perf_counter()
    while True:

        text = TextToScreen(miniGameTwoCord, 'BADGOPERFCT')
        print(text)
        if  'B' in text \
            and 'A' in text \
            and 'D' in text \
            and Nips:
            print('BAD')

            print(f'{perf_counter() - start}')
            return 'CheckStrength',CheckStrenght()


        if  'G' in text \
            and 'O' in text \
            and 'D' in text:
            print('GOOD')

            sleep(1.5)
            miniGameThree(autohotpy)

            if Nips:
                print(f'{perf_counter() - start}')
                return 'CheckInventory',CheckInventory(autohotpy)

        if  'P' in text \
            and 'E' in text \
            and 'R' in text \
            and 'F' in text  \
            and Nips:
            print('PERFECT')

            sleep(6)
            print(f'{perf_counter() - start}')
            return 'CheckInventory',CheckInventory(autohotpy)

def color_segmentation(hsv_image):
    # сегментация для синего
    min_blue = np.array((118, 177, 69), np.uint8)
    max_blue = np.array((255, 243, 182), np.uint8)
    thresh_blue = cv2.inRange(hsv_image, min_blue, max_blue)
    momens_blue = cv2.moments(thresh_blue, 1)['m00']

    # сегментация для фиолетового
    min_purple = np.array((128, 69, 88), np.uint8)
    max_purple = np.array((144, 134, 201), np.uint8)
    thresh_purple = cv2.inRange(hsv_image, min_purple, max_purple)
    momens_purple = cv2.moments(thresh_purple, 1)['m00']

    # сегментация для голубого
    # min_ocean = np.array((114, 127, 73), np.uint8)
    # max_ocean = np.array((255, 203, 203), np.uint8)
    min_ocean = np.array((71, 82, 56), np.uint8)
    max_ocean = np.array((75, 141, 217), np.uint8)
    thresh_ocean = cv2.inRange(hsv_image, min_ocean, max_ocean)
    momens_ocean = cv2.moments(thresh_ocean, 1)['m00']

    # сегментация для ярко-синего
    min_Hblue = np.array((99, 102,  69), np.uint8)
    max_Hblue = np.array((255, 180, 208), np.uint8)
    thresh_Hblue = cv2.inRange(hsv_image, min_Hblue, max_Hblue)
    momens_Hblue = cv2.moments(thresh_Hblue, 1)['m00']

    # сегментация для темно-синего
    min_Gblue = np.array((116, 118, 42), np.uint8)
    max_Gblue = np.array((255, 203, 206), np.uint8)
    #min_Gblue = np.array((116, 132, 52), np.uint8)
    #max_Gblue = np.array((255, 206, 208), np.uint8)
    thresh_Gblue = cv2.inRange(hsv_image, min_Gblue, max_Gblue)
    momens_Gblue = cv2.moments(thresh_Gblue, 1)['m00']

    #сегментация для розового
    min_chery = np.array((168, 121, 83), np.uint8)
    max_chery = np.array((172, 180, 180), np.uint8)
    thresh_chery = cv2.inRange(hsv_image, min_chery, max_chery)
    momens_chery = cv2.moments(thresh_chery, 1)['m00']


    # callback в зависимости от сегментации
    if momens_purple>300:
        return 54,cv2.THRESH_BINARY
    elif momens_chery>300:
        return 54,cv2.THRESH_BINARY
    if momens_blue > 230:
        return 47, cv2.THRESH_BINARY_INV
    elif momens_ocean>300:
        return 57,cv2.THRESH_BINARY
    elif momens_Hblue>300:
        return 85,cv2.THRESH_BINARY
    elif momens_Gblue>300:
        return 54,cv2.THRESH_BINARY
    else:
        return 60,cv2.THRESH_BINARY

def miniGameThree(autohotpy):
    start = perf_counter()
    print('Поиск символов')
    #скриншот по параметрам miniGameThree
    screen = stack_operation(miniGameThreeCord)
    cv2.imwrite('Images/img23.png',screen)
    #перевод в фильтр серого и hsv для сигментации
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

    # фильтр для создание котрара мини игры
    ret, thresh = cv2.threshold(gray, 71, 255, cv2.THRESH_BINARY)  # 80, 255

    # создание контара
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # размер мини-игры самый большой, так что... да
    cnt1 = max(contours, key=len)

    x, y, w, h = cv2.boundingRect(cnt1)

    # Обрезаем область под пол высоты для избегания лишних элементов для обработки
    cropped = gray[y + 5:y + h // 2 + 1, x:x + w]  # gray[y:y + h // 2 + 2, x:x + w]


    #получение параметров по цветовой сегмантации
    pos, bin = color_segmentation(hsv)

    ret, thresh2 = cv2.threshold(cropped, pos, 255, bin)


    # повышение контраста фильтров
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
    dilation = cv2.dilate(thresh2, rect_kernel, iterations=1)

    # создание отдельных изображений по конторам
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in reversed(contours):
        match cv2.boundingRect(cnt):
            case x, y, w, h if w * h > 160 and w * h < 400:
                cropped = thresh2[y:y + h, x:x + w]

                # ищем текст по вайт-листу = ASDW
                text = pytesseract.image_to_string(cropped, config='--psm 10 --oem 3 -c tessedit_char_whitelist=ASWD')
                print(text)
                # в соответствии имулируем нажатие клавиши
                match text:
                    case "W\n":
                        autohotpy.W.press()
                        continue
                    case "D\n":
                        autohotpy.D.press()
                        continue
                    case "S\n":
                        autohotpy.S.press()
                        continue
                    case "A\n":
                        autohotpy.A.press()
                        continue

    print(f'{perf_counter() - start}')


def leftButton(autohotpy):
    stroke = InterceptionMouseStroke()

    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)

    sleep(0.2)

    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)

    sleep(0.1)
    print('left button')

def rightButton(autohotpy):
    stroke = InterceptionMouseStroke()

    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
    autohotpy.sendToDefaultMouse(stroke)

    sleep(0.2)

    stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
    autohotpy.sendToDefaultMouse(stroke)

    sleep(0.1)
    print('right button')


def swapWeopen(autohotpy,click):
    # смена удочка/оружие
    if click:
        autohotpy.I.press()
    sleep(.3)
    autohotpy.moveMouseToPosition(1033, 310)
    sleep(.2)
    rightButton(autohotpy)
    sleep(.4)
    autohotpy.ESC.press()
    sleep(.2)


def SearchNip(autohotpy,num):
    print('Searct nip',num)


    #вызов панели поиск нипов через hot-key alt+v
    autohotpy.LEFT_ALT.down()
    autohotpy.V.press()
    sleep(.2)
    autohotpy.LEFT_ALT.up()

    #скрин окна поиск нипов в разделе избраное(1.торговец,2.ремонт,3.рыбалка)
    screen = stack_operation(SearchNipCord)

    #перевод в серый и перевод пикселей в ч/б с контрастом
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 61, 255, cv2.THRESH_BINARY)
    #повышение контраста для конторов
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)
    #определение конторов и получение координат
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cikl = 0

    #цыкл на поиск кнопки автопути
    for cnt in reversed(contours):


        match cv2.boundingRect(cnt):
            case x,y,w,h if (w * h >= 2000 and w * h <= 3000 ) and (num == 1 and cikl == 1 or num == 2 and cikl == 2 or num == 0):
                # перевод мышки на корды
                autohotpy.moveMouseToPosition(747 + x + w // 4, 217 + y + h // 2)

                break
            case _:
                cikl+=1

    #перевод мышки на корды
    autohotpy.moveMouseToPosition(747 + x + w // 4, 217 + y + h // 2)


def ToRun(autohotpy):
    print('TO RUN')
    swapWeopen(autohotpy, False)

    # бег до торговца и продажа всего
    SearchNip(autohotpy, 0)
    sleep(.2)
    leftButton(autohotpy)
    sleep(1)
    autohotpy.T.press()
    sleep(60)
    autohotpy.R.press()
    sleep(1)
    autohotpy.N1.press()
    autohotpy.moveMouseToPosition(1250, 743)
    leftButton(autohotpy)
    sleep(1)
    autohotpy.moveMouseToPosition(646, 398)
    leftButton(autohotpy)
    sleep(0.4)
    autohotpy.ESC.press()
    sleep(0.4)
    autohotpy.ESC.press()

    sleep(5)

    # Бег до ремонта
    SearchNip(autohotpy, 1)
    sleep(.2)
    leftButton(autohotpy)
    sleep(1)
    autohotpy.T.press()
    sleep(5)
    autohotpy.R.press()
    sleep(1)
    autohotpy.N2.press()
    autohotpy.moveMouseToPosition(728, 801)  # Починка всего
    leftButton(autohotpy)
    sleep(1)
    autohotpy.moveMouseToPosition(633, 450)  # Починить
    leftButton(autohotpy)
    sleep(0.4)
    autohotpy.ESC.press()
    sleep(0.4)
    autohotpy.ESC.press()

    sleep(2)

    # Бег до рыбалки
    SearchNip(autohotpy, 2)
    sleep(.2)
    leftButton(autohotpy)
    sleep(1)
    autohotpy.T.press()
    sleep(40)

    swapWeopen(autohotpy, True)


def CheckStrenght()->list:
    start = perf_counter()
    print('Определение прочности удочки')
    sleep(8)
    screen = stack_operation(CheckStrengthCord)

    res = cv2.matchTemplate(CheckStrenghtShablon, screen, cv2.TM_CCOEFF_NORMED) == 1
    print(f'{perf_counter() - start}')
    return res

def CheckInventory(autohopty)->int:
    start = perf_counter()
    print('Определение кол-во слотов')
    sleep(8)
    autohopty.I.press()
    sleep(.3)
    screen = stack_operation(CheckInventoryCord)

    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray,config='--psm 7 --oem 3 -c tessedit_char_whitelist=1234567890/')

    print('Inventory:', text)
    print(f'{perf_counter() - start}')
    try:
        return int(text.split('/')[0])
    except:
        return 0


def exitAutoHotKey(autohotpy, event):
    autohotpy.stop()

def superCombo(autohotpy,event):
    global repeat

    print('Start script')

    start(autohotpy)

    print('Ожидание клева')
    sleep(7)
    expectation(autohotpy)

    print('Ловля на крючек')
    sleep(1.2)

    t = Timer(40, enableStart)
    t.start()
    miniGameOne(autohotpy)

    print('Определение результата: ')

    result, element = miniGameTwo(autohotpy)

    t.cancel()
    if Nips:
        match (result, element):
            case ['CheckStrenght', element] if element:
                ToRun(autohotpy)
            case ['CheckInventory', element] if element > 35:
                ToRun(autohotpy)

    if repeat:
        sleep(3)
        autohotpy.R.press()
        autohotpy.run(superCombo, event)


def enableDisableSuperCombo(autohotpy, event):
    global repeat

    if repeat:
        repeat = False
    else:
        repeat = True
        superCombo(autohotpy, event)


if __name__=="__main__":
    auto = AutoHotPy()
    auto.registerExit(auto.ESC, exitAutoHotKey)
    auto.registerForKeyDown(auto.F4, enableDisableSuperCombo)
    auto.start()