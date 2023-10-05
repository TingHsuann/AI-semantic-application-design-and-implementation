import sentDir
x=32
#讓螢幕上的文字可以用跑馬燈呈現
def movingWord(display, n, posY=12):
    global x
    if n<0:
        display.fill_rect(0, 0, 128, 20, 0)
        return
    if n>=len(sentDir.names):
        display.fill_rect(0, 44, 128, 20, 0)
        return
    words=sentDir.names[n]
    long=sentDir.lens[n]

    display.fill_rect(0, posY, 128, 16, 0) #畫出一個黑色實心矩形
    display.drawtext(words, x, posY) #在最後的地方加上1，就可以讓她反白

    x-=4
    if x<-(long-128):
        display.drawtext(words, x+long+8, posY)
    if x<-(long):
        x=4
    display.show()
