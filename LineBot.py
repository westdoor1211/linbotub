# -*- coding: utf-8 -*-
from ProcessData import*
stopwords = []
f = open('stopwords.txt',encoding='utf-8-sig')
string=f.read()
stopwords=string.strip().split("\n")
f.close()

QA={}
Q=pd.read_csv("QADB.csv",encoding = "big5").fillna("nan")
for index,row in Q.iterrows():
    if row["Query"]!="nan" or row["Response"]!="nan":
        QA.update({row["Query"]:row["Response"]})
global Data
Data=LoadData()

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

# new_model = gensim.models.Word2Vec.load('word2vec.model')

@app.route("/callback", methods=['POST'])
def callback():
    
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


@handler.add(MessageEvent, message=AudioMessage)  # 取得聲音時做的事情
def handle_message_Audio(event):
    UserID = event.source.user_id
    path="./"+UserID+".wav"
    audio_content = line_bot_api.get_message_content(event.message.id)
    with open(path, 'wb') as fd:
        for chunk in audio_content.iter_content():
            fd.write(chunk)        
    fd.close()
    AudioSegment.converter = '/app/vendor/ffmpeg/ffmpeg'
    sound = AudioSegment.from_file_using_temporary_files(path)
    path = os.path.splitext(path)[0]+'.wav'
    sound.export(path, format="wav")
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    text = r.recognize_google(audio,language='zh-Hant')
    event.message.text=text
    handle_message(event)
    
    

@handler.add(MessageEvent, message=StickerMessage)
def handle_message_img(event):  # 當取得貼圖時做的事情
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=str(random.randint(100, 139))  # 隨機傳送貼圖
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)


@handler.add(MessageEvent, message=ImageMessage)  # 當取得照片時做的事情 這邊也是設計成隨機傳送貼圖
def handle__img(event):
    # 隨機傳送貼圖
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=str(random.randint(100, 139))
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)


@handler.add(MessageEvent, message=LocationMessage)
def handle_message_loc(event):
    print(event.message.address)  # print 位置
    locate = quote(event.message.address)  # 起始位置名稱
    global site
    site = locate
    latitude = str(event.message.latitude)  # 緯度
    longitude = str(event.message.longitude)  # 經度
    FC = FCtype()
    line_bot_api.reply_message(event.reply_token, FC)
    return '0'

@handler.add(PostbackEvent)
def handle_postback(event):
    UserID = event.source.user_id
    richm1 = "richmenu-bb2270da0f654aad47e54ac3bf64e45f"
    if event.postback.data:
        try:
            rich_menu_id = line_bot_api.get_rich_menu_id_of_user(UserID)
        except:
        # link default rich menu
            line_bot_api.link_rich_menu_to_user(UserID, richm1)
    
        if rich_menu_id == richm1:
            line_bot_api.link_rich_menu_to_user(UserID, "richmenu-9751caeea6f1fc234b64aad0d18ed7c7") # 放2其他1
        else:
            line_bot_api.link_rich_menu_to_user(UserID, richm1)
            
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    #print("event.message.text:", event.message.text)
    msg = str(event.message.text).upper().strip().replace(" ","")
    profile = line_bot_api.get_profile(event.source.user_id)
    UserName=profile.display_name
    UserID=event.source.user_id
    #設定介面顯示User目前的設定
    rep=[]
    rep.append(TextSendMessage(text=event.message.text))
    Command=0
    global Data
    AddNewUser(event,Data)
    
    
    #--------------------------------推播設定------週期設定-------weekdaycheck------------------------------
    CheckWeekWord=['一','二','三','四','五','六','日','周','週','星期','禮拜']
    CheckWeekFlag=0
    for checkword in event.message.text:
        if checkword not in CheckWeekWord:
            CheckWeekFlag=1
    
    #-----------------------------------貨幣追蹤----追蹤方式--------百分比或某個部位cjeck-------------------------
    checkExceptRateFlag=1
    if (event.message.text[0]>="0" and event.message.text[0]<="9")\
            and ((event.message.text[-1]>="0" and event.message.text[-1]<="9") or event.message.text[-1]=="%"):
        CurrentPercentWord=['0','1','2','3','4','5','6','7','8','9','.']
        if event.message.text[-1]=="%":
            Text=event.message.text[:-1]
        else:
            Text = event.message.text
        for checkword in Text:
            if checkword in CurrentPercentWord:
                checkExceptRateFlag=0
            else:
                checkExceptRateFlag=1
    
    #---------------------------------------------功能選單----------------------------------------
    carousel_template_message = TemplateSendMessage(
        alt_text='功能選單',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                    title='功能選單',
                    text='頁面一',
                    actions=[
                        MessageTemplateAction(
                            label='外幣服務',
                            text='外幣服務'
                        ),
                        MessageTemplateAction(
                            label='銀行分行位置服務',
                            text='找銀行分行'
                        ),
                        MessageTemplateAction(
                            label='財務金融討論版',
                            text='財務金融討論版'
                        )
                    ]
                )
            ]
        )
    )
                    #問題與回報 URL https://docs.google.com/forms/d/1IUf_7V2AWcpETmCzbu1Ho7_H3-rIPmzIejYb4p3P2CQ/edit
    t = []

    #-----------------------------貨幣分析-------------現在買...好嗎----------------------------------
    if event.message.text.find("現在") != -1 and event.message.text.find("買") != -1 or event.message.text.find(
            "幫") != -1 and event.message.text.find("分析") != -1:
        Command=1
        resp = requests.get("https://rate.bot.com.tw/xrt")
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.find('table', 'table').tbody.find_all('tr')
        
        for a in rows:
            ab = a.find_all('td')[0]
            dolname = ab.find_all('div')[2].text.replace(" ", "").replace("\r\n", "").replace("\n", "").split('(')[0]
 
            if dolname in event.message.text.replace("日幣", "日圓"):
                resp = requests.get("https://rate.bot.com.tw/xrt/quote/ltm/" +
                                    ab.find_all('div')[2].text.replace(" ", "").replace("\r\n", "").replace("\n",
                                                                                                            "").split(
                                        '(')[1].replace(')', ''))
                soup = BeautifulSoup(resp.text, 'html.parser')
                rows = soup.find('table', 'table').tbody.find_all('tr')
                count = 0
                first_rate = 0
                rate_count = 0
                count_week = []
                now_rate = 0
                for a in rows:
                    count = count + 1
                    ab = a.find_all('td')
                    rate_count = rate_count + float(ab[2].text)
                    print(count)
                    
                    if count < 8:
                        count_week.append(float(ab[2].text))
                    if count == 1:
                        first_rate = float(ab[2].text)
                    if count == 30:
                        now_rate = first_rate - rate_count / count
                        print(now_rate)
                    if now_rate > 0:
                        rep.append(TextSendMessage(
                            text="現在" + dolname + "匯率：" + str("%.2f" % round(first_rate, 2)) + "\n較過去30天平均高: " + str(
                                "%.2f" % round(now_rate, 2))))
                        rep.append(TextSendMessage(text="一周內最低匯率為：" + str("%.2f" % round(min(count_week), 2))))
                        rep.append(TextSendMessage(text="建議可以先再觀察看看"))
                    if now_rate < 0:
                        rep.append(TextSendMessage(
                            text="現在" + dolname + "匯率：" + str("%.2f" % round(first_rate, 2)) + "\n較過去30天平均低: " + str(
                                "%.2f" % round(now_rate, 2))))
                        rep.append(TextSendMessage(text="一周內最低匯率為：" + str("%.2f" % round(min(count_week), 2))))
                        rep.append(TextSendMessage(text="或許可以考慮購買"))
        if len(rep) > 0:
            line_bot_api.reply_message(event.reply_token, rep)

    #銀行服務
    elif re.match("銀行服務", msg):
        Command = 1
        rep.append(BankService())
        line_bot_api.reply_message(event.reply_token,rep )
    #外幣服務
    elif re.match("外幣服務", msg):
        Command = 1
        rep.append(FScrvice())
        line_bot_api.reply_message(event.reply_token,rep )


    elif re.match("其他資訊", msg):
        Command = 1
        rep.append(OtherInfo())
        line_bot_api.reply_message(event.reply_token,rep )

    #----------------------------------------------------維修中------------------------------------
    elif event.message.text.find("維修中") != -1:
        Command = 1
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='功能維修中'))

    #--------------------------------------------------貨幣分析  -------------------------------------
    elif event.message.text=="貨幣分析":

        ptt_list = []
        resp = requests.get("https://rate.bot.com.tw/xrt")
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.find('table', 'table').tbody.find_all('tr')
        for a in rows:
            ab = a.find_all('td')
            dolname = ab[0].find_all('div')[2].text.replace(" ", "").replace("\r\n", "").replace("\n", "").split('(')[0]
            if dolname in event.message.text:
                buttons_template_message = TemplateSendMessage(
                    alt_text=dolname + "匯率",
                    template=ButtonsTemplate(
                        text=dolname      
                    )
                )
                ptt_list.append(buttons_template_message)
                line_bot_api.reply_message(event.reply_token, ptt_list)
        if len(ptt_list) < 1:
            carousel_template_message=CashAnaylis()

            line_bot_api.reply_message(event.reply_token, carousel_template_message)
    
    #---------------------------------------------取消訂閱-------------------------------------------------
    elif (event.message.text.find("取消") != -1 and event.message.text.find("訂閱") != -1) or (event.message.text.find("取消") != -1 and event.message.text.find("追蹤") != -1) or (event.message.text.find("刪除") != -1 and event.message.text.find("追蹤") != -1):
        Command=1
        old_data_list = []
        try:
            original_file = codecs.open(".\\user\\" + event.source.user_id + ".txt", "r", "utf-8-sig")
            old_data = original_file.read()
            old_data_list = old_data.split(' ')
        except:
            rep.append(TextSendMessage(text="您好" + profile.display_name + " 您已訂閱完成"))
            # rep.append(TextSendMessage(text="目前訂閱類別為："+'、'.join(list(set(str_lod)))+"之新聞"))
            rep.append(TextSendMessage(text="您目前還沒有訂閱，趕快先去訂閱吧"))
            line_bot_api.reply_message(event.reply_token, rep)
            print("新來的")
            return 0
 
        with codecs.open(".\\user\\" + event.source.user_id + ".txt", "w", "utf-8-sig") as temp:
            str_lod = []
            str_lod.extend(old_data_list)
            resp = requests.get("https://rate.bot.com.tw/xrt")
            soup = BeautifulSoup(resp.text, 'html.parser')
            rows = soup.find('table', 'table').tbody.find_all('tr')
            for a in rows:
                ab = a.find_all('td')[0]
                dolname = ab.find_all('div')[2].text.replace(" ", "").replace("\r\n", "").replace("\n", "").split('(')[
                    0]
                if dolname in event.message.text:
                    str_lod.remove(dolname)
            if event.message.text.find("全部") != -1:
                str_lod = []
            temp.write(' '.join(list(set(str_lod))))
            
            rep.append(TextSendMessage(text="您好" + profile.display_name + ""))
            if (len(set(str_lod)) > 1):
                str_wri = ""
                if len(list(set(str_lod))) > 1:
                    str_wri = '、'.join(list(set(str_lod)))[1:]
                else:
                    str_wri = '、'.join(list(set(str_lod)))
                rep.append(TextSendMessage(text="已經幫您取消，目前剩下的訂閱類別為：" + str_wri + ""))
                rep.append(TextSendMessage(text="本系統會持續為您關注"))
            else:
                rep.append(TextSendMessage(text="目前已經沒有訂閱了"))
        line_bot_api.reply_message(event.reply_token, rep)

    #---------------------------------------------------訂閱貨幣---------------------------------------------
    elif event.message.text.find("要") != -1 and event.message.text.find("訂閱") != -1 or event.message.text.find(
            "幫") != -1 and event.message.text.find("訂閱") != -1 or event.message.text.find(
            "想") != -1 and event.message.text.find("訂閱") != -1 or event.message.text.find(
            "要") != -1 and event.message.text.find("追蹤") != -1 or event.message.text.find(
            "幫") != -1 and event.message.text.find("追蹤") != -1 or event.message.text.find(
            "想") != -1 and event.message.text.find("追蹤") != -1:
 
        old_data_list = []
        try:
            original_file = codecs.open(".\\user\\" + event.source.user_id + ".txt", "r", "utf-8-sig")
            old_data = original_file.read()
            old_data_list = old_data.split(' ')
        except:
            print("新來的")
 
        with codecs.open(".\\user\\" + event.source.user_id + ".txt", "w", "utf-8-sig") as temp:
            str_lod = []
            str_lod.extend(old_data_list)
            # --模組
            resp = requests.get("https://rate.bot.com.tw/xrt")  # 利用台灣銀行現有表格來取得貨幣名稱(dolname)
            soup = BeautifulSoup(resp.text, 'html.parser')
            rows = soup.find('table', 'table').tbody.find_all('tr')
            for a in rows:
                ab = a.find_all('td')[0]
                dolname = ab.find_all('div')[2].text.replace(" ", "").replace("\r\n", "").replace("\n", "").split('(')[
                    0]
                if dolname in event.message.text:
                    str_lod.append(dolname)
            if event.message.text.find("全部") != -1:
                str_lod = []
            temp.write(' '.join(list(set(str_lod))))
            
            str_wri = ""
            # --模組
            if len(list(set(str_lod))) > 1:
                str_wri = '、'.join(list(set(str_lod)))[1:]
                
            else:
                str_wri = '、'.join(list(set(str_lod)))
            rep.append(TextSendMessage(text="您好" + profile.display_name + " 已幫您訂閱完成"))
            rep.append(TextSendMessage(text="目前您訂閱了：" + '、'.join(list(set(str_lod)))[1:] + ""))
            rep.append(TextSendMessage(text="本系統會持續為您關注這些"))
        line_bot_api.reply_message(event.reply_token, rep)

    #------------------------------------------目前匯率--------------------------------------------
    elif (event.message.text.find("目前")!=-1 or event.message.text.find("現在")!= -1) and event.message.text.find("匯率") != -1:
        Cash=SearchCash()
        print(Cash)
        Found={}
        EngCash=""
        ChCash=""
        for i in Cash:
            leftindex=i.find("(")
            rightindex=i.find(")")
            cash=i[:leftindex]
            if cash in event.message.text:
                ChCash=cash
                EngCash=i[leftindex+1:rightindex]
                Found={ChCash:Cash[i]}
                break
        if ChCash=="":
            carousel_template_message=SearchExchangeRate()
            line_bot_api.reply_message(event.reply_token, carousel_template_message)
        else:
            buttons_template_message = TemplateSendMessage(
                alt_text=ChCash + "匯率",
                template=ButtonsTemplate(
                    text="目前" + ChCash + "匯率\n" +
                    "現金買入:" + str(Found[ChCash]["本行現金買入"]) + "\n"+ 
                    "現金賣出:" + str(Found[ChCash]["本行現金賣出"]) + "\n\n"+
                    "即期買入:" + str(Found[ChCash]["本行即期買入"]) + "\n"+
                    "即期賣出:" + str(Found[ChCash]["本行即期賣出"]),
                    actions=[
                        URITemplateAction(
                            label='查看歷史匯率',
                            uri='https://rate.bot.com.tw/xrt/forward/'+EngCash
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, buttons_template_message)
 
    #-------------------------------------------------查詢訂閱內容-------------------------------------------------------
    elif event.message.text.find("我") != -1 and event.message.text.find("訂閱") != -1 and event.message.text.find(
            "什麼") != -1 or (event.message.text.find("查看") != -1 and event.message.text.find("訂閱") != -1) or (
            event.message.text.find("查看") != -1 and event.message.text.find("訂閱") != -1) or (
            event.message.text.find("訂閱") != -1 and event.message.text.find("類別") != -1) or (
            event.message.text.find("訂閱") != -1 and event.message.text.find("內容") != -1):

        old_data_list = []
        try:
            original_file = codecs.open(".\\user\\" + event.source.user_id + ".txt", "r", "utf-8-sig")
            old_data = original_file.read()
            old_data_list = old_data.split(' ')
        except:
            print("新來的")

        with codecs.open(".\\user\\" + event.source.user_id + ".txt", "w", "utf-8-sig") as temp:
            str_lod = []
            str_lod.extend(old_data_list)
            temp.write(' '.join(list(set(str_lod))))
            
            str_wri = ""
            if len(list(set(str_lod))) > 1:
                str_wri = '、'.join(list(set(str_lod)))[1:]
            else:
                str_wri = '、'.join(list(set(str_lod)))
            rep.append(TextSendMessage(text="您好" + profile.display_name + ""))
            rep.append(TextSendMessage(text="您目前訂閱了：" + str_wri + ""))
            # rep.append(TextSendMessage(text="本系統會持續為您關注這些討論文章"))
        line_bot_api.reply_message(event.reply_token, rep)
        
    # 使用者留言
    elif str(event.message.text).find("留言 ") != -1:
        Command=1
        f = open('C:\\Program Files\\VertrigoServ\\www\\re.txt', 'a+', encoding='UTF-8')
        profile = line_bot_api.get_profile(event.source.user_id)
        f.write(profile.display_name + ':' + event.message.text + '\r\n')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='感謝您的留言'))

    # 可以改成語言模型回應
    elif event.message.text == "你能做什麼":
        Command=1
        
        content = '我是一個能提供基本金融服務的對話機器人。 \r\n我目前正在學習外幣價格追蹤的功能'
        carousel_template_message = TemplateSendMessage(
            alt_text='功能選單',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                    thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                    title='功能選單',
                    text='頁面一',
                    actions=[
                        MessageTemplateAction(
                            label='外幣服務',
                            text='外幣服務'
                        ),
                        MessageTemplateAction(
                            label='銀行分行與ATM位置服務',
                            text='找銀行分行'
                        ),
                        MessageTemplateAction(
                            label='財務金融討論版',
                            text='財務金融討論版'
                        )
                    ]
                )
                ]
            )
        )
        rep.append(TextSendMessage(text=content))
        rep.append(TextSendMessage(text="以下是我的功能"))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)

    # chatter = chatbot.Chatbot(w2v_model_path='model/word2vec.model' ,unicode_errors='ignore')
    elif ''.join(event.message.text).find("功能選單") != -1 or ''.join(event.message.text).find("功能") != -1:
        Command=1
        
        rep.append(TextSendMessage(text="您好" + profile.display_name + "，以下是目前的服務選單："))

        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)


    #---------------------------------------找銀行或ATM互動圖-----------------------------------------
    elif event.message.text == "找銀行或ATM":
        Command=1
        
        findbank = '您要找銀行分行還是ATM呢?'
        carousel_template_message = TemplateSendMessage(
            alt_text='銀行 or ATM',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://image.freepik.com/free-vector/bank-counter-currency-exchange-service-atm-with-customer-vector-illustration_40816-84.jpg',
                        title='請選擇',
                        text='  ',
                        actions=[
                            MessageTemplateAction(
                                label='找銀行分行',
                                text='找銀行分行'
                            ),
                            MessageTemplateAction(
                                label='找ATM',
                                text='ATM查詢'
                            ),
                            LocationAction(
                                label='外幣ATM(定位)',
                            )          
                        ]                         
                    )              
                ]
            )
        )                   
        rep.append(TextSendMessage(text=findbank))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)

    # --------------------------------------找外幣ATM---------------------------------
    elif event.message.text in FCList and event.message.text == '美金ATM' or event.message.text == '日幣ATM':
        rep.append(FATMLists0())
        line_bot_api.reply_message(event.reply_token,rep)
    elif event.message.text in FCList and event.message.text == '港幣ATM':
        rep.append(FATMLists1())
        line_bot_api.reply_message(event.reply_token,rep)
    elif event.message.text in FCList and event.message.text == '歐元ATM':
        rep.append(FATMLists2())
        line_bot_api.reply_message(event.reply_token,rep)
    elif event.message.text in FCList and event.message.text == '人民幣ATM':
        rep.append(FATMLists3())
        line_bot_api.reply_message(event.reply_token,rep)
    # --------------------------------------找外幣ATM前往地圖---------------------------------
    elif event.message.text in FCATMList:
        bks = event.message.text
        rep.append(banksmap(bks,site))
        line_bot_api.reply_message(event.reply_token,rep)

    #--------------------------------------找ATM---------------------------------
    elif (event.message.text.find("ATM")!=-1 or event.message.text.find("Atm")!=-1 or event.message.text.find("atm")!=-1) and (event.message.text.find("查詢")!=-1 or event.message.text.find("找")!=-1):
        Command=1
        
        findbank = '請選取您要找的ATM'
        findATM = '如須查詢銀行位置，請輸入:找銀行分行'
        flexmessage=BankListService("ATM")
        rep.append(TextSendMessage(text=findbank))
        rep.append(flexmessage)
        rep.append(TextSendMessage(text=findATM))
        line_bot_api.reply_message(event.reply_token, rep)
     

    #----------------------------------找銀行廣範圍---------------------------------
    elif event.message.text.find("銀行分行")!=-1 and (event.message.text.find("查詢")!=-1 or event.message.text.find("找")!=-1):
        Command=1
        
        findbank = '請選取您要找的銀行'
        findATM = '如須查詢 ATM 位置，請輸入:找ATM'
        flexmessage=BankListService("銀行")
        rep.append(TextSendMessage(text=findbank))
        rep.append(flexmessage)
        rep.append(TextSendMessage(text=findATM))
        line_bot_api.reply_message(event.reply_token, rep)

    #--------------------------------找銀行細部-------------------------------------
    elif event.message.text in BankList:
        carousel_template_message=BankSecondService(event.message.text,"")
        
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------找ATM列表---------------------------------------
    elif event.message.text in ATMList:
        carousel_template_message=BankSecondService(event.message.text,"ATM")
        
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
        
    #-----------------------------------討論版---------------------------------------
    elif event.message.text == "財務金融討論版":
        
        onlinediscuss = '歡迎進入財務金融討論版'
        carousel_template_message = TemplateSendMessage(
            alt_text='財務金融討論版',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPzHddHhcEi3DDEzeFQSXTrYMYyizZugsI29c9xmFDAZhs8kBJ',
 
                        title='財務金融討論版',
                        text='Dcard 、 PTT',
                        actions=[
                             URITemplateAction(
                                label='PTT匯率版',
                                uri='https://www.ptt.cc/bbs/ForeignEX/index.html'
                            ),
                            URITemplateAction(
                                label='Dcard理財版',
                                uri='https://www.dcard.tw/f/money'
                            )
                        ]
                    )
                ]
            )
        )
        rep.append(TextSendMessage(text=onlinediscuss))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)


    #-----------------------------------新聞服務---------------------------------------------------------------
    elif event.message.text == "新聞服務":
        Command=1
        

        onlinediscuss = '以下為新聞之服務'
        carousel_template_message=NewsService()
        rep.append(TextSendMessage(text=onlinediscuss))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #-----------------------------------新聞查詢---------------------------------------------------------------
    elif event.message.text == "新聞查詢":
        Command=1
        
        rep.append(TextSendMessage(text="請輸入想查詢的新聞，例如:匯率 新聞，即會推播匯率相關新聞"))
        line_bot_api.reply_message(event.reply_token, rep)
    
    #-----------------------------------MoneyDJ理財網新聞---------------------------------------------------------------
    elif event.message.text=="MoneyDJ理財網新聞":
        Command=1
        
        rep.append(TextSendMessage(text=news("MoneyDJ理財網新聞")))
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------****** 新聞-------------------------------------------------------------
    elif event.message.text.find("新聞")!=-1 and len(event.message.text)>=2:
        Command=1
        
        rep.append(TextSendMessage(text=news(event.message.text.replace("新聞",""))))
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------信用卡情報-------------------------------------------------------------
    elif event.message.text=="信用卡情報":
        Command=1
        carousel_template_message=CreditCard()
        rep.append(TextSendMessage(text="來自PTT的信用卡情報:"))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token,rep)
        
    #--------------------------------------財經節目-------------------------------------------------------------
    elif re.match("財經節目", msg):

        Command = 1
        rep = [youtube_channel(), YoutubeKeys()]
        line_bot_api.reply_message(event.reply_token, rep)

    elif event.message.text.upper()[0] == 'K' and event.message.text.find("K") != -1:
        Command = 1
        line_bot_api.reply_message(event.reply_token, [NewsKeys(msg[1:])])

    #----------------------------------------推播設定----------------------------------------------------------------
    elif event.message.text=="推播設定" or event.message.text=="證券服務" or event.message.text=="保險服務":
        Data=LoadData()
        Command=1
        '''
        DayAlarm=Data[UserID]["DayAlarm"]
        Period=Data[UserID]["WeekCycle"]
        MaxWord=Data[UserID]["MaxWord"]
        NewsDaySwitch=Data[UserID]["NewsDaySwitch"]
        
        flexmessage=ShowPushSetting(DayAlarm,Period,MaxWord,NewsDaySwitch)
        rep.append(flexmessage)
        '''
        
        onlinediscuss = '開發中'
        rep.append(TextSendMessage(text=onlinediscuss))
        line_bot_api.reply_message(event.reply_token, rep)
        
    #----------------------------推播設定------推播時間設定---------------------------------------------------
    elif event.message.text == "推播時間設定":

        Command=1
        
        #flexmessage=TimeService()
        #rep.append(flexmessage)
        onlinediscuss = '開發中，目前設定在早上9點'
        rep.append(TextSendMessage(text=onlinediscuss))
        line_bot_api.reply_message(event.reply_token, rep)
        
    #----------------------------推播設定------週期設定------------------------------------------------
    elif event.message.text == "週期設定":
        Command=1
        
        rep.append(TextSendMessage(text="輸入您想推播的週期，例如:一二六日"))
        line_bot_api.reply_message(event.reply_token, rep)
        
    #----------------------------推播設定------00:00-----------------------------------------------------
    elif len(event.message.text)<=5 and event.message.text.find(":")!=-1 \
            and event.message.text[0]>="0" and event.message.text[0]<="9":
        Command=1
        
        Data=LoadData()
        Data[UserID]["DayAlarm"]=event.message.text
        rep.append(TextSendMessage(text="已將您的推播時間設定在"+event.message.text))
        
        DayAlarm=Data[UserID]["DayAlarm"]
        Period=Data[UserID]["WeekCycle"]
        MaxWord=Data[UserID]["MaxWord"]
        NewsDaySwitch=Data[UserID]["NewsDaySwitch"]
        flexmessage=ShowPushSetting(DayAlarm,Period,MaxWord,NewsDaySwitch)
        rep.append(flexmessage)
        line_bot_api.reply_message(event.reply_token, rep)
        
    #----------------------------推播設定-------一二四五-----------------------------------------------
    elif len(event.message.text) <=9 and CheckWeekFlag==0:
        Command=1
        
        Data=LoadData()
        Data[UserID]["WeekCycle"]=ProcessPeriod(event.message.text)
        rep.append(TextSendMessage(text="已將您的推播週期設定在每個禮拜的"+event.message.text))
        DayAlarm=Data[UserID]["DayAlarm"]
        Period=Data[UserID]["WeekCycle"]
        MaxWord=Data[UserID]["MaxWord"]
        NewsDaySwitch=Data[UserID]["NewsDaySwitch"]
        flexmessage=ShowPushSetting(DayAlarm,Period,MaxWord,NewsDaySwitch)
        rep.append(flexmessage)
        line_bot_api.reply_message(event.reply_token, rep)
        
    #----------------------------推播設定--------推播開關設定----------------------------------------------
    elif event.message.text=="推播開關設定":
        Command=1
        
        Data=LoadData()
        DayAlarm=Data[UserID]["DayAlarm"]
        Period=Data[UserID]["WeekCycle"]
        MaxWord=Data[UserID]["MaxWord"]
        NewsDaySwitch=Data[UserID]["NewsDaySwitch"]
        
        flexmessage=NewsDaySwitchSetting(DayAlarm,Period,MaxWord,NewsDaySwitch)
        rep.append(flexmessage)
        line_bot_api.reply_message(event.reply_token, rep)
        
    #----------------------------推播設定------開啟or關閉------------------------------------------------
    elif event.message.text=="推播通知開啟" or event.message.text=="推播通知關閉":
        sett=event.message.text.replace("推播通知","")
        Command=1
        
        Data=LoadData()
        Data[UserID]["NewsDaySwitch"]=sett
        
        DayAlarm=Data[UserID]["DayAlarm"]
        Period=Data[UserID]["WeekCycle"]
        MaxWord=Data[UserID]["MaxWord"]
        NewsDaySwitch=Data[UserID]["NewsDaySwitch"]
        rep.append(TextSendMessage(text="已"+sett))
        flexmessage=ShowPushSetting(DayAlarm,Period,MaxWord,NewsDaySwitch)
        rep.append(flexmessage)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #-------------------------------------------外幣服務----------------------------------------
    elif event.message.text == "外幣服務":
        Command=1
        
        onlinediscuss = '以下為外幣之服務'
        carousel_template_message = TemplateSendMessage(
            alt_text='外幣服務',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/MPCafZS.png',
                        title='外幣服務列表',
                        text='匯率、貨幣與新聞',
                        actions=[
                            MessageTemplateAction(
                                label='目前匯率查詢',
                                text='目前匯率查詢'
                            ),
                            MessageTemplateAction(
                                label='貨幣分析',
                                text='貨幣分析'
                            ),
                            MessageTemplateAction(
                                label='貨幣追蹤',
                                text='貨幣追蹤'
                                # URITemplateAction(label='匯率新聞', uri='https://news.cnyes.com/news/cat/forex?exp=a')
                            )

                        ]

                    )
                ]
            )
        )
        rep.append(TextSendMessage(text=onlinediscuss))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------貨幣追蹤----------------------------------------
    elif event.message.text == "貨幣追蹤":
        Command=1
        

        onlinediscuss = '開發中'
        #carousel_template_message=TrackCashService(Data[UserID])
        rep.append(TextSendMessage(text=onlinediscuss))
        #rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------貨幣追蹤----貨幣列表----------------------------
    elif event.message.text == "貨幣列表":
        Command=1
        
        
        onlinediscuss = '以下為貨幣列表'
        carousel_template_message=ShowCashService()
        rep.append(TextSendMessage(text=onlinediscuss))
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------貨幣追蹤----追蹤*****-------------------------------
    elif event.message.text[0:2]=="追蹤" and len(event.message.text)>8 and len(event.message.text)<12:
        Command=1
        Data=LoadData()
        
        TrackCurrency=event.message.text[2:]
        Data[UserID]["TrackCash"]={TrackCurrency:{"CashSpot":"","TrackWay":"",
                                                    "StartDay":"","EndDay":"",
                                                    "BuySell":"","ExceptRate":"",
                                                    "TrackRate":"","CashDaySwitch":"關閉"}}
        
        cash=SearchCash()
        SpotBuy=str(cash[TrackCurrency]["本行即期買入"])
        SpotSell=str(cash[TrackCurrency]["本行即期賣出"])
        CashSell=str(cash[TrackCurrency]["本行現金賣出"])
        CashBuy=str(cash[TrackCurrency]["本行現金買入"])
        
        ShowTemText="目前"+TrackCurrency+"\n"
        ShowTemText+="現金買入:"+CashBuy+"，現金賣出:"+CashSell+"\n"
        ShowTemText+="即期買入:"+SpotBuy+"，即期賣出:"+SpotSell+"\n"
        
        carousel_template_message=TrackCashOrSpot(ShowTemText)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    
    #--------------------------------------貨幣追蹤---現金或即期---------------------------
    elif event.message.text=="現金或即期":
        Command=1
        Data=LoadData()
        rep.append(CheckTrackCash(Data[UserID][0]))
        CheckTrackCashFlag=CheckTrackCash(Data[UserID])[1]
        if CheckTrackCashFlag==0:
            cash=SearchCash()
            TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
            SpotBuy=str(cash[TrackCurrency]["本行即期買入"])
            SpotSell=str(cash[TrackCurrency]["本行即期賣出"])
            CashSell=str(cash[TrackCurrency]["本行現金賣出"])
            CashBuy=str(cash[TrackCurrency]["本行現金買入"])
            
            ShowTemText="目前"+TrackCurrency+"\n"
            ShowTemText+="現金買入:"+CashBuy+"，現金賣出:"+CashSell+"\n"
            ShowTemText+="即期買入:"+SpotBuy+"，即期賣出:"+SpotSell+"\n"
            
            carousel_template_message=TrackCashOrSpot(ShowTemText)
            rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------貨幣追蹤------選擇現金or即期-----------------------------
    elif event.message.text=="現金" or event.message.text=="即期":
        Command=1
        Data=LoadData()
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        ShowTemText="目前"+TrackCurrency+"\n"
        cash=SearchCash()
        if event.message.text=="現金":
            CashSell=str(cash[TrackCurrency]["本行現金賣出"])
            CashBuy=str(cash[TrackCurrency]["本行現金買入"])

            ShowTemText+="現金買入:"+CashBuy+"\n"
            ShowTemText+="現金賣出:"+CashSell
        else:
            SpotBuy=str(cash[TrackCurrency]["本行即期買入"])
            SpotSell=str(cash[TrackCurrency]["本行即期賣出"])

            ShowTemText+="即期買入:"+SpotBuy+"\n"
            ShowTemText+="即期賣出:"+SpotSell
        Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]=event.message.text
        carousel_template_message=HowToTrackChoose(ShowTemText)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    #--------------------------------------貨幣追蹤-----追蹤方式------------------------------
    elif event.message.text == "追蹤方式":
        Command = 1
        Data = LoadData()
        
        rep.append(CheckTrackCash(Data[UserID])[0])
        CheckTrackCashFlag=CheckTrackCash(Data[UserID][1])
        if CheckTrackCashFlag==0:
            rep.append(CheckCashSpot(Data[UserID])[0])
            CheckCashSpotFlag=CheckCashSpot(Data[UserID])[1]
            if CheckCashSpotFlag==0:
                cash = SearchCash()
                TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
                ShowTemText = "目前" + TrackCurrency + "\n"
                SpotBuy = str(cash[TrackCurrency]["本行即期買入"])
                SpotSell = str(cash[TrackCurrency]["本行即期賣出"])
                CashSell = str(cash[TrackCurrency]["本行現金賣出"])
                CashBuy = str(cash[TrackCurrency]["本行現金買入"])
    
                ShowTemText += "現金買入:" + CashBuy + "，現金賣出:" + CashSell + "\n"
                ShowTemText += "即期買入:" + SpotBuy + "，即期賣出:" + SpotSell + "\n"
                carousel_template_message = HowToTrackChoose(ShowTemText)
                rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #--------------------------------------貨幣追蹤------選擇升(降)百分比or升(降)至某個部位----------------------------------
    elif event.message.text=="升(降)百分比" or event.message.text=="升(降)至某個部位":
        Command=1
        Data=LoadData()
        cash=SearchCash()
        
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        ShowTemText = "目前" + TrackCurrency + "\n"
        Data[UserID]["TrackCash"][TrackCurrency]["TrackWay"]=event.message.text
        CashSpot=Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]
        CashSell=str(cash[TrackCurrency]["本行"+CashSpot+"賣出"])
        CashBuy=str(cash[TrackCurrency]["本行"+CashSpot+"買入"])
        ShowTemText+=CashSpot+"買入:"+CashBuy+"\n"
        ShowTemText+=CashSpot+"賣出:"+CashSell
        
        carousel_template_message=ProcessBuySell(ShowTemText)
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    #--------------------------------------貨幣追蹤------買入或賣出----------------------------------
    elif event.message.text=="買入或賣出":
        Command = 1
        Data = LoadData()
        
        rep.append(CheckTrackCash(Data[UserID])[0])
        CheckTrackCashFlag=CheckTrackCash(Data[UserID])[1]
        if CheckTrackCashFlag==0:
            rep.append(CheckCashSpot(Data[UserID])[0])
            CheckCashSpotFlag=CheckCashSpot(Data[UserID])[1]
            if CheckCashSpotFlag==0:
                rep.append(CheckTrackWay(Data[UserID])[0])
                CheckTrackWayFlag=CheckTrackWay(Data[UserID])[1]
                if CheckTrackWayFlag==0:
                    cash=SearchCash()
                    
                    TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
                    ShowTemText = "目前" + TrackCurrency + "\n"
                    Data[UserID]["TrackCash"][TrackCurrency]["TrackWay"]=event.message.text
                    CashSpot=Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]
                    CashSell=str(cash[TrackCurrency]["本行"+CashSpot+"賣出"])
                    CashBuy=str(cash[TrackCurrency]["本行"+CashSpot+"買入"])
                    ShowTemText+=CashSpot+"買入:"+CashBuy+"\n"
                    ShowTemText+=CashSpot+"賣出:"+CashSell
                    
                    carousel_template_message=ProcessBuySell(ShowTemText)
                    rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
                    
    
    #--------------------------------------貨幣追蹤-----選擇買入or賣出-----------------------------------
    elif  event.message.text=="買入" or event.message.text=="賣出":
        Command=1
        Data=LoadData()
        cash=SearchCash()
        
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        Data[UserID]["TrackCash"][TrackCurrency]["BuySell"]=event.message.text
        TrackWay=Data[UserID]["TrackCash"][TrackCurrency]["TrackWay"]
        CashSpot=Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]
        BuySell=Data[UserID]["TrackCash"][TrackCurrency]["BuySell"]
        TrackRate=cash[TrackCurrency]["本行"+CashSpot+BuySell]
        ShowTemText="目前"+TrackCurrency+"\n"
        ShowTemText+="本行"+CashSpot+BuySell+":"+str(TrackRate)+"\n"

        Data[UserID]["TrackCash"][TrackCurrency]["TrackRate"]=TrackRate
        if TrackWay=="升(降)百分比":
            rep.append(TextSendMessage(text=ShowTemText+"\n請輸入要升(降)的百分比\n，例:輸入 5%"))
        else:
            rep.append(TextSendMessage(text=ShowTemText+"\n請輸入要升(降)至的部位\n，例:輸入 32.5"))
        line_bot_api.reply_message(event.reply_token, rep)
    
     #--------------------------------------貨幣追蹤-----目標匯率設定-----------------------------------
    elif  event.message.text=="目標匯率設定":
        Command=1
        Data=LoadData()
        cash=SearchCash()
        
        rep.append(CheckTrackCash(Data[UserID])[0])
        CheckTrackCashFlag=CheckTrackCash(Data[UserID])[1]
        if CheckTrackCashFlag==0:
            rep.append(CheckCashSpot(Data[UserID])[0])
            CheckCashSpotFlag=CheckCashSpot(Data[UserID])[1]
            if CheckCashSpotFlag==0:
                rep.append(CheckTrackWay(Data[UserID])[0])
                CheckTrackWayFlag=CheckTrackWay(Data[UserID])[1]
                if CheckTrackWayFlag==0:
                    rep.append(CheckBuySell(Data[UserID])[0])
                    CheckBuySellFlag=CheckBuySell(Data[UserID])[1]
                    if CheckBuySellFlag==0:
                        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
                        TrackWay=Data[UserID]["TrackCash"][TrackCurrency]["TrackWay"]
                        CashSpot=Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]
                        BuySell=Data[UserID]["TrackCash"][TrackCurrency]["BuySell"]
                        TrackRate=cash[TrackCurrency]["本行"+CashSpot+BuySell]
                        ShowTemText="目前"+TrackCurrency+"\n"
                        ShowTemText+="本行"+CashSpot+BuySell+":"+str(TrackRate)+"\n"
                
                        Data[UserID]["TrackCash"][TrackCurrency]["TrackRate"]=BuySell
                        if TrackWay=="升(降)百分比":
                            rep.append(TextSendMessage(text=ShowTemText+"\n請輸入要升(降)的百分比\n，例:輸入 5%"))
                        else:
                            rep.append(TextSendMessage(text=ShowTemText+"\n請輸入要升(降)至的部位\n，例:輸入 32.5"))
        line_bot_api.reply_message(event.reply_token, rep)
        
    #--------------------------------------貨幣追蹤-------*** or ***%---------------------------------
    elif checkExceptRateFlag==0:
        Command=1
        
        Data=LoadData()
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        Data[UserID]["TrackCash"][TrackCurrency]["ExceptRate"]=event.message.text
        rep.append(TextSendMessage(text="請問追蹤幾天?(例:14天)"))
        line_bot_api.reply_message(event.reply_token, rep)
    
     #--------------------------------------貨幣追蹤-----追蹤天數設定-----------------------------------
    elif event.message.text=="追蹤天數設定":
        Command=1
        Data=LoadData()
        cash=SearchCash()
        
        rep.append(CheckTrackCash(Data[UserID])[0])
        CheckTrackCashFlag=CheckTrackCash(Data[UserID])[1]
        if CheckTrackCashFlag==0:
            rep.append(CheckCashSpot(Data[UserID])[0])
            CheckCashSpotFlag=CheckCashSpot(Data[UserID])[1]
            if CheckCashSpotFlag==0:
                rep.append(CheckTrackWay(Data[UserID])[0])
                CheckTrackWayFlag=CheckTrackWay(Data[UserID])[1]
                if CheckTrackWayFlag==0:
                    rep.append(CheckBuySell(Data[UserID])[0])
                    CheckBuySellFlag=CheckBuySell(Data[UserID])[1]
                    if CheckBuySellFlag==0:
                        rep.append(CheckTrackRate(Data[UserID])[0])
                        CheckTrackRateFlag==CheckTrackRate(Data[UserID])[1]
                        if CheckTrackRateFlag==0:
                            TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
                            rep.append(TextSendMessage(text="請問追蹤幾天?(例:14天)"))
        line_bot_api.reply_message(event.reply_token, rep)
      
    #--------------------------------------貨幣追蹤--------***天-------------------------
    elif event.message.text[0]>="0" and  event.message.text[0]<="9" and event.message.text[-1]=="天" and len(event.message.text)<5:
        Command=1
        
        Data=LoadData()
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        CashSpot=Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]
        BuySell=Data[UserID]["TrackCash"][TrackCurrency]["BuySell"]
        TrackRate=Data[UserID]["TrackCash"][TrackCurrency]["TrackRate"]
        
        CurrentPercentWord=['0','1','2','3','4','5','6','7','8','9']
        flag=0
        for checkpercent in event.message.text[0:-1]:
            if checkpercent not in CurrentPercentWord:
                flag=1
                rep.append(TextSendMessage(text="請輸入正確的格式"))
                break;
                
        if rep==[]:
            cash=SearchCash()
            
            Data[UserID]["TrackCash"][TrackCurrency]["StartDay"]=datetime.today().strftime("%Y-%m-%d")
            EndDay=datetime.today()+timedelta(days=int(event.message.text[:-1]))
            Data[UserID]["TrackCash"][TrackCurrency]["EndDay"]=EndDay.strftime("%Y-%m-%d")
            ShowTemText="目前"+TrackCurrency+"\n"
            ShowTemText+=CashSpot+BuySell+":"+str(TrackRate)
            carousel_template_message=PushSwitch(ShowTemText)
            rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
     #--------------------------------------貨幣追蹤-----通知開關設定-----------------------------------
    elif event.message.text=="通知開關設定":
        cash=SearchCash()
        Command=1
        
        Data=LoadData()
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        CashSpot=Data[UserID]["TrackCash"][TrackCurrency]["CashSpot"]
        BuySell=Data[UserID]["TrackCash"][TrackCurrency]["BuySell"]
        TrackRate=Data[UserID]["TrackCash"][TrackCurrency]["TrackRate"]
        
        ShowTemText="目前"+TrackCurrency+"\n"
        ShowTemText+=CashSpot+BuySell+":"+str(TrackRate)
        carousel_template_message=PushSwitch(ShowTemText)
        rep.append(carousel_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
        
    #--------------------------------------貨幣追蹤--------設定每天匯率通知---------------------
    elif event.message.text=="開啟每天匯率通知" or event.message.text=="關閉每天匯率通知":
        Command=1

        Data=LoadData()
        TrackCurrency=list(Data[UserID]["TrackCash"].keys())[0]
        Data[UserID]["TrackCash"][TrackCurrency]["CashDaySwitch"]=event.message.text[:2]
        Word=ShowWords(Data[UserID])
        Text="已"+event.message.text[:2]+"，追蹤設定完畢\n"
        Text+="您目前追蹤的貨幣為:"+Word[0]+"\n"
        Text += "開始日期為:"+Word[1] + "\n"
        Text += "結束日期為:"+Word[2]+"\n"
        Text += "追蹤方式為:"+Word[3]+"   "+Word[4] + "\n"
        Text += "現金或即期:"+Word[5] + "\n"
        Text += Word[0]+"目前"+Word[5]+Word[3]+"為:"+Word[6]
        rep.append(TextSendMessage(text=Text))
        line_bot_api.reply_message(event.reply_token, rep)
    
    #-------------------------------------------錢線百分百----------------------------------------
    elif event.message.text == "錢線百分百":
        buttons_template_message=Money()
        
        rep.append(buttons_template_message)
        line_bot_api.reply_message(event.reply_token, rep)
    
    #------------------------------------------會員中心----------------------------------------
    elif event.message.text == "會員中心":
        Command=1
        flexmessage=MemberCenter(UserName)
        
        rep.append(flexmessage)
        line_bot_api.reply_message(event.reply_token, rep)
    
    elif event.message.text == "我的收藏":
        Command=1
        
        onlinediscuss = '開發中'
        rep.append(TextSendMessage(text=onlinediscuss))
        line_bot_api.reply_message(event.reply_token, rep)
        
    elif event.message.text == "回饋":
        Command=1
        
        onlinediscuss = '開發中'
        rep.append(TextSendMessage(text=onlinediscuss))
        line_bot_api.reply_message(event.reply_token, rep)
    
    #-------------------------------------------其他----------------------------------------
    else:
        
        text=""
        if QA.get(event.message.text)!=None:
            text+=event.message.text+":"+QA[event.message.text]+"\n"
        else:
            Input=jieba.cut(event.message.text)
            for index in Input:
                if index not in stopwords and QA.get(index)!=None:
                    text+=index+":"+QA[index]+"\n"
        if text=="":
            text="不好意思我不太懂，" + profile.display_name + "，以上是目前的服務選單："
            rep.append(carousel_template_message)
        rep.append(TextSendMessage(text))

        line_bot_api.reply_message(event.reply_token, rep)

    RecordUser(event,Data,Command)
    Data=LoadData()
    print(Data[UserID])
    return 0

if __name__ == '__main__':
    app.run()
