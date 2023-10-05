#相關函式庫匯入
import paho.mqtt.client as mqtt
import json  
import time
import requests 

#詢問使用者
def ask_mood():
    global s
    s = input('請對我說一句話，我可以辨識你的心情好壞...')
    return s
#使用ChatGPT辯識心情
def GPT_regmood():
    global GPT_response,ans
    prompt = ""
    prompt='「'+str(ans)+'」，請幫我判斷這句話屬於「開心、難過、生氣、平淡」哪一種心情，請只回答心情不要其他敘述，如果無法判斷請直接回答「無法判斷」。並且請讓回答只有「開心、難過、生氣、平淡、無法判斷」之一，不要有其他敘述或符號'
    #print(prompt)#檢查輸入GPT語句是否有錯誤
    payload={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type":"application/json"
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    try:
        GPT_response=analyze_res(r.content)  
        print("你現在的狀態是:"+GPT_response)
    except:
        print("發生錯誤:",r.content)
#解析回傳資料 僅取出data中 json格式中的content
def analyze_res(data):
    # 將 bytes 轉換為 string
    data_str = data.decode('utf-8')
    # 解析 JSON 資料
    json_data = json.loads(data_str)
    # 取出 choices 中的回應內容
    #print(json_data)
    #print(json_data['choices'][0])
    response = json_data['choices'][0]['message']['content']
    return response
#初始化並做MQTT_publisher
def set_mqtt():
    global client
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()
    # 設定登入帳號密碼
    client.username_pw_set('Little_fox', 'kk900930')
    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("140.127.218.172", 1883, 60)
    
###資料宣告
#導入GPT用來判斷心情
api_key = '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'
url='https://api.openai.com/v1/chat/completions'
###主程式
set_mqtt()
print("早安呀~情緒就像是一個滑板，你需要找到平衡點，才能讓自己在不同的場合中保持穩定。\n用一句話來表達現在的情緒吧")
while True:
    ans = ask_mood()
    GPT_regmood()
    mood = 3
    if "難過" in GPT_response:
        mood = 0
    elif "開心" in GPT_response :
        mood = 1
    elif "生氣" in GPT_response :
        mood = 2

    payload = {'shuanhihii' : mood}
    #print (json.dumps(payload))#查看MQTT發布的訊息
    #要發布的主題和內容
    #for i in range(0,2):#除錯用
    client.publish("shuan", json.dumps(payload))
    time.sleep(1)
