import cv2
import numpy as np
from mss import mss
import subprocess
import time
import os
import win32api, win32con
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def getMousePos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def takeScreenShot():
    with mss() as sct:
        sct.shot()
    time.sleep(0.1)
    return cv2.imread("monitor-1.png")

img = takeScreenShot()

# option: 0-center 1-topleft 2-bottomright
def findImage(smallImg, bigImg, option = 0):
    h, w = smallImg.shape[:-1]
    res = cv2.matchTemplate(bigImg, smallImg, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)
    ret = []
    mask = np.zeros(bigImg.shape[:2], np.uint8)
    for pt in zip(*loc[::-1]):  # Switch columns and rows
        if mask[pt[1] + h//2, pt[0] + w//2] != 255:
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            #cv2.rectangle(bigImg, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            if option == 0:
                ret.append((pt[0] + w // 2, pt[1]+ h // 2))
            elif option == 1:
                ret.append((pt[0], pt[1]))
            else:
                ret.append((pt[0] + w, pt[1] + h))
    return ret

n0 = cv2.imread("n0.bmp")
n1 = cv2.imread("n1.bmp")
n2 = cv2.imread("n2.bmp")
n3 = cv2.imread("n3.bmp")
n4 = cv2.imread("n4.bmp")
n5 = cv2.imread("n5.bmp")
n6 = cv2.imread("n6.bmp")
n7 = cv2.imread("n7.bmp")
n8 = cv2.imread("n8.bmp")
n9 = cv2.imread("n9.bmp")
nx = cv2.imread("nx.bmp")
nums = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,nx]
texts = ["0","1","2","3","4","5","6","7","8","9","/"]
banthangImg = cv2.imread("banthang.png")
coinImg = cv2.imread("coin.png")
luachonImg = cv2.imread("luachon.png")
pauseImg = cv2.imread("pause.png")
xImg = cv2.imread("x.png")
xangsangImg = cv2.imread("xangsang.png")
xangtoiImg = cv2.imread("xangtoi.png")
playImg = cv2.imread("play.png")
stopImg = cv2.imread("stop.png")
phaiduoimain = cv2.imread("phaiduoimain.png")
capdoImg = cv2.imread("capdo.png")
capdo144Img = cv2.imread("capdo144.png")
vaochoiImg = cv2.imread("vaochoi.png")
x5vaochoiImg = cv2.imread("x5vaochoi.png")
previousImg = cv2.imread("previous.png")
map14Img = cv2.imread("map14.png")
donghoImg = cv2.imread("dongho.png")
gonextImg = cv2.imread("gonext.png")
choilaiImg = cv2.imread("choilai.png")
bocuocImg = cv2.imread("bocuoc.png")

def getText(img):
    textMap = []
    for i in range(len(nums)):
        ps = findImage(nums[i], img)
        textMap.extend([(p[0], texts[i]) for p in ps])
    textMap.sort(key = lambda x : x[0])
    ret = ""
    lastX = -10
    for tm in textMap:
        if tm[0] - lastX > 5:
            ret += tm[1]
            lastX = tm[0]
    return ret

#imgText = cv2.imread("1235.bmp")

#print(getText(imgText))

#subprocess.call("TASKKILL /F /IM MuratectSupporter.exe", shell=True)
#os.startfile("C:\Users\Thuy\OneDrive\Máy tính\JackalSquad.lnk")

playPostion = (0, 0)
stopPostion = (0, 0)
mainGameRect = (0,0,0,0)    # left top right bottom
xangRect = (0,0,0,0)        # left top right bottom

def getPosition():
    global playPostion
    global stopPostion
    global mainGameRect
    global xangRect
    screen = takeScreenShot()
    pl = findImage(playImg, screen)
    if len(pl) > 0:
        playPostion = pl[0]
    st = findImage(stopImg, screen)
    if len(st) > 0:
        stopPostion = st[0]
    tl = findImage(xangsangImg, screen, 1)
    if len(tl) == 0:
        tl = findImage(xangtoiImg, screen, 1)
    br = findImage(phaiduoimain, screen, 2)
    if len(tl) > 0 and len(br) > 0:
        mainGameRect = (tl[0][0], tl[0][1], br[0][0], br[0][1])
        xangRect = (mainGameRect[0] + 40, mainGameRect[1], mainGameRect[0] + 140, mainGameRect[1] + 40)
    #xangImg = screen[xangRect[1]:xangRect[3], xangRect[0]:xangRect[2]]

    print("playPostion", playPostion)
    print("stopPostion", stopPostion)
    print("mainGameRect", mainGameRect)
    print("xangRect", xangRect)

def resetGame():
    subprocess.call("TASKKILL /F /IM HD-Player.exe", shell=True)
    time.sleep(0.2)
    os.startfile("C:/Users/Thuy/OneDrive/Máy tính/JackalSquad.lnk")
    time.sleep(30)

    while True:
        screen = takeScreenShot()
        xPos = findImage(xImg, screen)
        tl = findImage(xangsangImg, screen, 1)
        if len(xPos) > 0 or len(tl) > 0:
            break
        time.sleep(2)
    for i in range (4):
        screen = takeScreenShot()
        xPos = findImage(xImg, screen)
        if(len(xPos) > 0):
            click(xPos[0][0],xPos[0][1])
        else:
            break
        time.sleep(4)

    getPosition()

    screen = takeScreenShot()
    xPos = findImage(vaochoiImg, screen)
    if(len(xPos) > 0):
        click(xPos[0][0],xPos[0][1])
        time.sleep(2)

    screen = takeScreenShot()
    prevPos = findImage(previousImg, screen)
    if(len(prevPos) == 0):
        return

    for i in range(50):
        screen = takeScreenShot()
        xPos = findImage(map14Img, screen)
        if(len(xPos) > 0):
            click(xPos[0][0],xPos[0][1])
            time.sleep(1)
            break
        else:
            click(prevPos[0][0],prevPos[0][1])
            time.sleep(1)

def playGame(_needReset = True):
    global playPostion
    global stopPostion
    global mainGameRect
    global xangRect

    playPostion = (40, 89)
    stopPostion = (168, 94)
    mainGameRect = (1320, 32, 1884, 1034)
    xangRect = (1360, 32, 1460, 72)

    count = 0
    needReset = _needReset
    xang = 0

    while True:
        if needReset:
            needReset = False
            resetGame()

        time.sleep(2)
        screen = takeScreenShot()
        xangImg = screen[xangRect[1]:xangRect[3], xangRect[0]:xangRect[2]]
        xangText = getText(xangImg)
        if "/" in xangText:
            print("xang", xangText)
            if len(xangText.split("/")[0])>0:
                xang = int(xangText.split("/")[0])
            else:
                xang = 0
        if xang < 5:
            time.sleep(180)
            click(stopPostion[0], stopPostion[1])
            continue

        xPos = findImage(capdo144Img, screen)
        if len(xPos) == 0:
            needReset = True
            continue
        xPos = findImage(x5vaochoiImg, screen)
        if(len(xPos) > 0):
            click(xPos[0][0],xPos[0][1])
            time.sleep(1)

        time.sleep(10)
        screen = takeScreenShot()
        if len(findImage(donghoImg, screen)) == 0:
            print("Khong co dong ho")
            needReset = True
            continue
        count = count + 1
        print("Thuc hien lan thu", count)
        click(playPostion[0], playPostion[1])

        startRecordTime = time.time()
        while True:
            time.sleep(2)
            curTime = time.time()
            if curTime - startRecordTime > 180:
                break
            pos = getMousePos()
            if abs(pos[0] - playPostion[0]) < 20 and abs(pos[1] - playPostion[1]) < 20:
                break

        screen = takeScreenShot()
        xPos = findImage(gonextImg, screen)
        if(len(xPos) > 0):
            click(xPos[0][0],xPos[0][1])
            time.sleep(6)
            for i in range (4):
                screen = takeScreenShot()
                xPos = findImage(xImg, screen)
                if(len(xPos) > 0):
                    click(xPos[0][0],xPos[0][1])
                else:
                    break
                time.sleep(2)
            screen = takeScreenShot()
            xPos = findImage(map14Img, screen)
            if(len(xPos) > 0):
                click(xPos[0][0],xPos[0][1])
                time.sleep(1)
        else:
            screen = takeScreenShot()
            xPos = findImage(luachonImg, screen)
            if(len(xPos) > 0):
                print("Click lua chon")
                click(xPos[0][0],xPos[0][1])
                time.sleep(2)

            screen = takeScreenShot()
            xPos = findImage(pauseImg, screen)
            if(len(xPos) > 0):
                print("Click pause")
                click(xPos[0][0],xPos[0][1])
                time.sleep(3)
                screen = takeScreenShot()
                xPos = findImage(bocuocImg, screen)
                if(len(xPos) > 0):
                    print("Click bo cuoc")
                    click(xPos[0][0],xPos[0][1])
                    time.sleep(3)

            screen = takeScreenShot()
            xPos = findImage(choilaiImg, screen)
            if(len(xPos) > 0):
                print("Click choi lai")
                click(xPos[0][0],xPos[0][1])
                time.sleep(6)

import sys
if len(sys.argv) > 1:
    playGame(False)
else:
    playGame(True)

'''
running = True
while running:
    #os.system('clear')
    print("1. Init position")
    print("2. Start")
    #print("3. Reserve")
    cmd = input("command: ")
    if cmd == 'q':
        running = False
        continue
    elif cmd == '1':
        getPosition()
        print(xangRect)
        print(mainGameRect)
        continue
    elif cmd == '2':
        playGame()
        continue
    #elif cmd == '3':
    #    continue
    else:
        continue
'''