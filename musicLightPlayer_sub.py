#邏輯和字串處理功能函式庫
import json
import random
#物聯網相關函式庫匯入
from umqtt.simple import MQTTClient
from machine import SoftI2C,Pin ,ADC , Timer
from dfplayermini import Player
import machine, network, neopixel, utime, ntptime, config, time, ssd1306,gfx
#跑馬燈函式庫
import chineseWords

###定義函式
#螢幕初始化
def set_monitor(i2c):
    global display
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    graphics = gfx.GFX(128, 64, display.pixel)
    display.invert(0)      # 螢幕顏色正常
    display.rotate(True)   #  螢幕旋轉180度
#初始化並做MQTT_subscriber
def set_mqtt():
    global mqClient0
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True) 
    wlan.connect('Little_fox', 'kk900930')
    while not wlan.isconnected():
        pass
    mqClient0 = MQTTClient('Test00','140.127.218.172')
    mqClient0.set_callback(sub_cb)
    mqClient0.connect()
    mqClient0.subscribe("shuan")
#設定顏色
def set_color(r, g, b):
    for i in range(LED_NUM/2):
        np[i*2-1] = (r, g, b)
    np.write()
#設定音樂
def set_music(track):
    time.sleep_ms(500)
    music.volume(15)  #Set volume value. From 0 to 30
    music.pause()
    time.sleep_ms(100)
    music.play(track)
    time.sleep_ms(500)
#控制音量大小
def set_vol():
    global music
    val_ori = vr.read()  # 讀取0-4095中讀原始模擬值
    val_vol = map(val_ori,0,4095,0, 30)    #實際改變音量的控制
    music.volume(val_vol)  #將類比的數值丟進dfplayermini的音量控制中
#將旋鈕的值改成喇吧播放的實際值
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
#json檔處理
def sub_cb(topic, msg):
    global data
    print((topic, msg))
    try:
        data = json.loads(msg)
        shuanhihii = data['shuanhihii']
        data=[shuanhihii]
        print(f'{shuanhihii}')
    except ValueError:
        print('Invalid JSON')
        
###資料宣告
#ws2812 初始化
LED_NUM = 60  # 燈環 LED數量
np = neopixel.NeoPixel(Pin(33), LED_NUM)
#宣告DFPlayer mini腳位，DFPlayer的RX接ESP32的GPIO17
music = Player(pin_TX=17, pin_RX=16)
#宣告按鈕的腳位
Music_OFF = Pin(4,Pin.IN,Pin.PULL_UP)
#可變電阻宣告
vr = ADC(Pin(32))
vr.atten(ADC.ATTN_11DB)
#設定LED一開始的亮度
LEDbright = 1
#OLED的腳位
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
set_monitor(i2c)
#設定曲目
nag_track=[2]
pos_track=[4,6]
angry_track=[3,8]
nor_travk=[5,7]

###主程式
#初始化並做MQTT_subscriber
set_mqtt()
#待機中，等使用者按按鈕
while (Music_OFF.value()==1):
    print("待機中....",Music_OFF.value())
    time.sleep(1)
#開機和使用者打招呼
set_music(1)
print("早安呀~情緒就像是一個滑板，你需要找到平衡點，才能讓自己在不同的場合中保持穩定。\n用一句話來表達現在的情緒吧")
#設定初始狀態為:normal
set_color(10, 10, 10)
data=[-1]
sentence_num = -1
while True:
    data=[-1]
    set_vol()   
    mqClient0.check_msg()#隨時確認有沒有Publish訊息出來
    if(data[0]==0):#nag
        set_color(0, 0, 10)
        set_music(nag_track[random.randrange(1)])
        sentence_num = 0        
    elif(data[0]==1):#positive
        set_color(0, 10, 0)
        set_music(pos_track[random.randrange(2)])
        sentence_num = 1
    elif(data[0]==2):#angry
        set_color(10, 0, 0)
        set_music(angry_track[random.randrange(2)])
        sentence_num = 2
    elif(data[0]==3):#normal
        set_color(10, 10, 10)
        set_music(nor_travk[random.randrange(2)])
        sentence_num = 3
    chineseWords.movingWord(display,sentence_num,12)
    time.sleep(0.01)
        
