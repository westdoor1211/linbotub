# -*- coding: utf-8 -*-
import requests, json
import re
import random
import configparser
import urllib.request, json
import urllib.parse
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from datetime import datetime,timedelta
import gensim
from gensim import corpora, models, similarities
import codecs
import pickle
import jieba
import csv
import re
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment

import os
import jieba.posseg as pseg
from selenium import webdriver
# import Chatbot.chatbot as chatbot
# from opencc import OpenCC
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import jieba
import csv
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import threading
import functools
import schedule
import time
from FlexMessage import*

BankList=["台灣、土地、合作金庫",
              "第一、華南、彰化",
              "上海、富邦、國泰世華",
              "中國輸出、高雄、兆豐",
              "花旗、王道、台灣企銀",
              "渣打、台中、京城銀行",
              "匯豐、瑞興、華泰",
              "新光、陽信、板信",
              "三信、聯邦、遠東商銀",
              "元大、永豐、玉山",
              "凱基、星辰、台新",
              "日盛、安泰、中國信託"]

ATMList=["台灣、土地、合作金庫ATM",
              "第一、華南、彰化ATM",
              "上海、富邦、國泰世華ATM",
              "中國輸出、高雄、兆豐ATM",
              "花旗、王道、台灣企銀ATM",
              "渣打、台中、京城銀行ATM",
              "匯豐、瑞興、華泰ATM",
              "新光、陽信、板信ATM",
              "三信、聯邦、遠東商銀ATM",
              "元大、永豐、玉山ATM",
              "凱基、星辰、台新ATM",
              "日盛、安泰、中國信託ATM"]

line_bot_api = LineBotApi("Kr0MqFFqWrpQjPZVsSlPwxWpPUl2FP6x2mu9wjfhaA2Z/M7Jl9QNlQEyC+caP8vTX6xqU2qPaFBb6xmaXmS3yaN0LERn2wXx5Nv5bLNADz2BUEZkwc5jgEXUK3xj6enUCO2aZGjHLYXJbJGQMC8MsgdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('00456b5ad1316c2a1fd6141a3e1b670c')

NGWords=["、","。","，",",","?",".","!"," "," ",":","-",";",")","(","...","的",'1','2','3','4','5','6','7','8','9','0','．','/',', ','（','）','·',' · ',' ·',">","<","；",
                 "：",'|','！',"『","』","---","僅","供","必","是","也","@","【","】","\n"," "]

#------------------------Load-----------------------------
def LoadData():
    with open("UserData.json", 'r',encoding="utf-8") as reader:
        Data=json.loads(reader.read())
    return Data

#----------------------AddNew------------------------------
def AddNewUser(event,Data):
    UserID=event.source.user_id
    Message = event.message.text
    if Data.get(UserID)==None:
        Data.update({UserID:{"TotalWords":0,
                             "Text":[],
                             "TextFrequency":[],
                             "MaxWord":"無",
                             "TrackCash":"",
                             "DayAlarm":"尚未設定",
                             "WeekCycle":[],
                             "NewsDaySwitch":"關閉"}
                })
        line_bot_api.push_message(UserID, TextSendMessage(text="您目前沒有設定推播通知時間，設定之後將根據您的搜尋紀錄，在您設定的時間推播相關新聞給您，如需設定請點選 '功能面板 ' 的 ' 推播設定 '"))
    with open("UserData.json", 'w',encoding="utf-8") as outfile:
        json.dump(Data, outfile,ensure_ascii=False)
    
#-----------------------Record------------------------------------
def RecordUser(event,Data,Command):
    Message = event.message.text
    print(Message)
    if Message.find("新聞")!=-1 and Message.find("MoneyDJ理財網新聞")==-1 and Message.find("新聞查詢")==-1 and Message.find("新聞服務")==-1:
        Message=Message.replace(" 新聞","")
        Command=0
    if Command==0:
        UserID=event.source.user_id
        words=jieba.cut(Message,cut_all=False)
        for word in words:
            Data[UserID]["TotalWords"]+=1
            if word not in NGWords:
                if word not in Data[UserID]["Text"]:
                    Data[UserID]["Text"].append(word)
                    Data[UserID]["TextFrequency"].append(1)
                else:
                    TextIndex=Data[UserID]["Text"].index(word)
                    Data[UserID]["TextFrequency"][TextIndex]+=1
        TotalWords=Data[UserID]['TotalWords']
        MaxIndex=Data[UserID]['TextFrequency'].index(max(Data[UserID]['TextFrequency']))
        MaxWord=Data[UserID]['Text'][MaxIndex]
        Data[UserID]["MaxWord"]=MaxWord
        
    with open("UserData.json", 'w',encoding="utf-8") as outfile:
        json.dump(Data, outfile,ensure_ascii=False)

#---------------------週期轉換成顯示文字-------------------------------- 
def ProcessPeriod(Input):
    a=[0,0,0,0,0,0,0]
    for i in Input:
        if i=="一":
            a[0]=1
        elif i=="二":
            a[1]=1
        elif i=="三":
            a[2]=1
        elif i=="四":
            a[3]=1
        elif i=="五":
            a[4]=1
        elif i=="六":
            a[5]=1
        elif i=="日":
            a[6]=1
    return a

#--------------------------------新聞爬蟲---------------------------------
def news(strs):
    content=""
    co=0
    if strs=="MoneyDJ理財網新聞":
        url = "https://www.ettoday.net/news_search/doSearch.php?keywords=%E6%96%B0%E8%81%9E%E9%9B%B2&kind=17&idx=1"
        response = requests.get(url,timeout=30)
        response.encoding = 'UTF-8-sig'
        input_html = response.text
        soup = BeautifulSoup(input_html,"html.parser")
        SearchResult=soup.findAll("div",{"class":"archive clearfix"})
        for i in SearchResult:
            title=i.find("h2").text
            link=i.find("a")["href"]
            content+=title+"\n"+link+"\n\n"
            co+=1
            if co==7:
                break;
  
    else:
        today=datetime.now().date()
        url = "https://www.ettoday.net/news_search/doSearch.php?search_term_string="+strs
        response = requests.get(url,timeout=30)
        response.encoding = 'UTF-8-sig'
        input_html = response.text
        soup = BeautifulSoup(input_html,"html.parser")
        SearchResult=soup.findAll("div",{"class":"archive clearfix"})
        for i in SearchResult:
            title=i.find("h2").text
            link=i.find("a")["href"]
            tt=i.find("span",{"class":"date"}).text
            ttindex=tt.find("/")
            tt=tt[ttindex+2:]
            ttindex=tt.find(" ")
            tt=tt[:ttindex]
            date=datetime.strptime(tt, "%Y-%m-%d").date()
            if today-date<=timedelta(days=1):
                content+=title+"\n"
                content+=link+"\n"
                content+=date.strftime("%Y-%m-%d")+"\n\n"
                co+=1
                if co==3:
                    break;
    if content=="":
        content="沒有最近的新聞"
    return content

#----------------------------新聞服務列表-------------------------------------------
def NewsService():
    ServiceList=['新聞查詢','MoneyDJ理財網新聞']
    a=[]
    for i in ServiceList:
        a.append(
                MessageTemplateAction(
                label=i,
                text=i)
        )
    carousel_template_message = TemplateSendMessage(
            alt_text='新聞服務',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/MPCafZS.png',
                        title='新聞服務列表',
                        text='新聞服務列表',
                        actions=a
                    )
                ]
            )
        )
    return carousel_template_message

#----------------------------追蹤貨幣列表-----------------------------------
def ShowCashService():
    CashList=['美金(USD)','港幣(HKD)','英鎊(GBP)',
              '澳幣(AUD)','加拿大幣(CAD)','新加坡幣(SGD)',
              '瑞士法郎(CHF)','日圓(JPY)','人民幣(CNY)',
              '瑞典幣(SEK)','紐元(NZD)','泰幣(THB)',
              '菲國比索(PHP)','印尼幣(IDR)','歐元(EUR)',
              '韓元(KRW)','越南盾(VND)','馬來幣(MYR)']
    columnsList=[]
    for i in range(0,len(CashList),3):
        a=[]
        for j in range(i,i+3):
            a.append(
                    MessageTemplateAction(
                    label=CashList[j],
                    text="追蹤"+CashList[j]
                    )
            )
        columnsList.append(
            CarouselColumn(
                thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                title='請問您要追蹤哪個貨幣?',
                text='貨幣列表',
                actions=a
            )
        )
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=columnsList
                )
    )
    return carousel_template_message

#----------------------接收FTrackCashService用-------------------------------------
def TrackCashService(UserData):
    Words=ShowWords(UserData)
    flexmessage=FlexTrackCashService(Words)
    return flexmessage

#------------------------匯率爬蟲---------------------------------------------
def SearchCash():
    cash={}
    resp = requests.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")
    soup = BeautifulSoup(resp.text, 'html.parser')
    rows = soup.find('table', 'table').tbody.find_all('tr')
    for checkcash in rows:
        Sp=checkcash.find('div',{"class":"visible-phone print_hide"}).text.replace(' ',"").replace('\r\n',"")
        a=checkcash.find('td',{"data-table":"本行現金買入"}).text.replace('\r\n',"").replace(" ","",50).replace("\n","",50).replace("結售","",50)
        b=checkcash.find('td',{"data-table":"本行現金賣出"}).text.replace('\r\n',"").replace(" ","",50).replace("\n","",50).replace("結購","",50)
        c=checkcash.find('td',{"data-table":"本行即期買入"}).text.replace('\r\n',"").replace(" ","",50).replace("\n","",50).replace("結售","",50)
        d=checkcash.find('td',{"data-table":"本行即期賣出"}).text.replace('\r\n',"").replace(" ","",50).replace("\n","",50).replace("結購","",50)
        cash.update({Sp:{"本行現金買入":a,"本行現金賣出":b,"本行即期買入":c,"本行即期賣出":d}})
        
        for checkcash in cash[Sp]:
            if type(cash[Sp][checkcash])!=str:
                cash[Sp][checkcash]=float(cash[Sp][checkcash])
    return cash

#------------------------貨幣追蹤--------------------現金或即期----------------------------------
def TrackCashOrSpot(ShowTemText):
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                            title='追蹤現金或即期',
                            text=ShowTemText,
                            actions=[
                                MessageTemplateAction(
                                    label='現金',
                                    text='現金'
                                ),
                                MessageTemplateAction(
                                    label='即期',
                                    text='即期'
                                )
                            ]
                        )
                    ]
                )
    )
    return carousel_template_message

#------------------------貨幣追蹤--------------------追蹤方式----------------------------------
def HowToTrackChoose(ShowTemText):
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                            title='如何追蹤',
                            text=ShowTemText,
                            actions=[
                                MessageTemplateAction(
                                    label='升(降)百分比',
                                    text='升(降)百分比'
                                ),
                                MessageTemplateAction(
                                    label='升(降)至某個部位',
                                    text='升(降)至某個部位'
                                )
                            ]
                        )
                    ]
                )
    )
    return carousel_template_message

#------------------------貨幣追蹤--------------------買入或賣出----------------------------------
def ProcessBuySell(ShowTemText):
    carousel_template_message = TemplateSendMessage(
                    alt_text='功能選單',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                                title='買入或賣出',
                                text=ShowTemText,
                                actions=[
                                    MessageTemplateAction(
                                        label='買入',
                                        text='買入'
                                    ),
                                    MessageTemplateAction(
                                        label='賣出',
                                        text='賣出'
                                    )
                                ]
                            )
                        ]
                    )
            )
    return carousel_template_message

#------------------------貨幣追蹤--------------------匯率推播開關----------------------------------
def PushSwitch(ShowTemText):
    carousel_template_message = TemplateSendMessage(
                    alt_text='功能選單',
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                                title='設定每天匯率通知',
                                text=ShowTemText,
                                actions=[
                                    MessageTemplateAction(
                                        label='開啟每天匯率通知',
                                        text='開啟每天匯率通知'
                                    ),
                                    MessageTemplateAction(
                                        label='關閉每天匯率通知',
                                        text='關閉每天匯率通知'
                                    )
                                    
                                ]
                            )
                        ]
                    )
    )
    return carousel_template_message

#------------------------貨幣追蹤--------------------顯示文字----------------------------------
def ShowWords(UserData):
    if UserData["TrackCash"]=="":
        Words="無"
    else:
        TrackCurrency=list(UserData["TrackCash"].keys())[0]
        StartDay=UserData["TrackCash"][TrackCurrency]["StartDay"]
        EndDay=UserData["TrackCash"][TrackCurrency]["EndDay"]
        BuySell=UserData["TrackCash"][TrackCurrency]["BuySell"]
        TrackWay=UserData["TrackCash"][TrackCurrency]["TrackWay"]
        CashSpot=UserData["TrackCash"][TrackCurrency]["CashSpot"]
        ExceptRate=str(UserData["TrackCash"][TrackCurrency]["ExceptRate"])
        TrackRate=str(UserData["TrackCash"][TrackCurrency]["TrackRate"])
        
        Words=[TrackCurrency,StartDay,EndDay,BuySell,ExceptRate,CashSpot,TrackRate]
    return Words

#------------------------匯率查詢----------------------------------
def SearchExchangeRate():
    CashList=['美金','港幣','英鎊',
              '澳幣','加拿大幣','新加坡幣',
              '瑞士法郎','日圓','南非幣',
              '瑞典幣','紐元','泰幣',
              '菲國比索','印尼幣','歐元',
              '韓元','越南盾','馬來幣',
              '人民幣','黃金','台灣銀行公告總匯率']
    c=[]
    for i in range(0,len(CashList),3):
        a=[]
        for j in range(i,i+3):
            if CashList[j]=='黃金':
                a.append(URITemplateAction(
                                label=CashList[j],
                                uri='https://rate.bot.com.tw/gold?Lang=zh-TW'
                        ))
            elif CashList[j]=='台灣銀行公告總匯率':
                a.append(URITemplateAction(
                                label=CashList[j],
                                uri='https://rate.bot.com.tw/xrt?Lang=zh-TW'
                        ))
            else:
                a.append(MessageTemplateAction(
                               label=CashList[j],
                               text="目前"+CashList[j]+"匯率"
                        ))
        c.append(CarouselColumn(
                    thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                    title='請選擇欲查詢的匯率項目',
                    text='貨幣頁面',
                    actions=a))
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=c
            )
    )
    return carousel_template_message

#------------------------貨幣分析---------------------------------------------------
def CashAnaylis():
    CashList=['美金','港幣','英鎊',
              '澳幣','加拿大幣','新加坡幣',
              '瑞士法郎','日圓','瑞典幣',
              '紐元','泰幣','菲國比索',
              '印尼幣','歐元','韓元',
              '人民幣','越南盾','馬來幣']
    c=[]
    for i in range(0,len(CashList),3):
        a=[]
        for j in range(i,i+3):
            a.append(MessageTemplateAction(
                           label=CashList[j],
                           text="現在買"+CashList[j]+"好嗎?"
                    ))
        c.append(CarouselColumn(
                    thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                    title='請選擇欲分析的貨幣',
                    text='貨幣頁面',
                    actions=a))
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=c
            )
    )
    return carousel_template_message

#------------------------匯率推播----------------------------------
def PushCash():
    cash=SearchCash()
    Data=LoadData()
    today=datetime.now().date()
    for i in Data:
        if Data[i]['TrackCash']!="":
            TrackCurrency=list(Data[i]['TrackCash'].keys())[0]
            IterData=Data[i]["TrackCash"][TrackCurrency]
            if all(list(IterData.values()))==True:
                PushFlag=0
                print(Data[i])
                TrackCurrency=list(Data[i]['TrackCash'].keys())[0]
                StartDay=datetime.strptime(Data[i]["TrackCash"][TrackCurrency]["StartDay"],"%Y-%m-%d").date()
                EndDay=datetime.strptime(Data[i]["TrackCash"][TrackCurrency]["EndDay"],"%Y-%m-%d").date()
                BuySell=Data[i]["TrackCash"][TrackCurrency]["BuySell"]
                TrackWay=Data[i]["TrackCash"][TrackCurrency]["TrackWay"]
                CashSpot=Data[i]["TrackCash"][TrackCurrency]["CashSpot"]
                ExceptRate=Data[i]["TrackCash"][TrackCurrency]["ExceptRate"]
                TrackRate=float(Data[i]["TrackCash"][TrackCurrency]["TrackRate"])
                
                Rate=cash[TrackCurrency]["本行"+CashSpot+BuySell]
                if Rate!="-":
                    Rate=float(Rate)
                    per=0
                    ReplyText="目前"+TrackCurrency+BuySell+"為:"+str(Rate)
                    print(ReplyText)
                    if ExceptRate[-1]=="%":
                        ExceptRate=float(ExceptRate[:-1])/100
                        if Rate>=TrackRate*(1+ExceptRate):
                            ReplyText=ReplyText+"\n"+CashSpot+BuySell+"已達標!!"
                            PushFlag=1
                        else:
                            per=(Rate/TrackRate)/100
                    else:
                        ExceptRate=float(ExceptRate)
                        if Rate>=ExceptRate:
                            ReplyText=ReplyText+CashSpot+BuySell+"已達標!!"
                            PushFlag=1
                            
                    if Data[i]["TrackCash"][TrackCurrency]["CashDaySwitch"]=="開啟":
                        PushFlag=1
                    if today>EndDay:
                        PushFlag=1
                        Data[i]["TrackCash"][TrackCurrency]["StartDay"]=""
                        Data[i]["TrackCash"][TrackCurrency]["EndDay"]=""
                        Data[i]["TrackCash"][TrackCurrency]["CashDaySwitch"]="關閉"
                    print(ReplyText)
                    if PushFlag>0:
                        line_bot_api.push_message(i, TextSendMessage(text=ReplyText))
                
    with open("UserData.json", 'w',encoding="utf-8") as outfile:
        json.dump(Data, outfile,ensure_ascii=False)

#------------------------新聞推播----------------------------------    
def PushMessage():
    today=datetime.now().weekday()
    NewsCan={}

    Data=LoadData()
    #now=datetime.now().strftime("%H:%M")
    for i in Data:
        print(Data[i]['DayAlarm'])
        MaxWord=Data[i]['MaxWord']
        if NewsCan.get(MaxWord)==None:
            NewsCan.update({MaxWord:news(MaxWord)})
        if len(Data[i]['WeekCycle'])!=0 and Data[i]['WeekCycle'][today]==1 and Data[i]['NewsDaySwitch']=="開啟":
            line_bot_api.push_message(i, TextSendMessage(text=NewsCan[MaxWord]))

#------------------------銀行列表-廣範圍---------------------------------
def BankListService(atm):
    bankList=BankList
    if atm=="ATM":
        bankList=ATMList
    c=[]
    for i in range(0,len(bankList),3):
        a=[]
        for j in range(i,i+3):
            a.append(MessageTemplateAction(
                            label=bankList[j],
                            text=bankList[j]
                        ))
        
        c.append(CarouselColumn(
                    thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                    title='請選擇欲查詢的'+atm,
                    text='貨幣頁面',
                    actions=a))
        print(c)
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=c
            )
    )
    return carousel_template_message

#------------------------銀行列表細部----------------------------------
def BankSecondService(Input,atm):
    Text=Input+atm
    Bank1=Input[:Input.find("、")]
    if len(Bank1)==2:
        Bank1+="銀行"+atm
    Input=Input.replace(Input[:Input.find("、")+1],"")
    Bank2=Input[:Input.find("、")]
    if len(Bank2)==2:
        Bank2+="銀行"+atm
    Bank3=Input.replace(Input[:Input.find("、")+1],"")
    if len(Bank3)==2:
        Bank3+="銀行"+atm
    
    carousel_template_message = TemplateSendMessage(
                alt_text='功能選單',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2017/01/%E5%8F%B0%E7%81%A3%E5%8C%AF%E7%8E%87%E9%80%9A58988085_m.jpg',
                            title=Text,
                            text=Text,
                            actions=[
                                URITemplateAction(
                                        label=Bank1,
                                        uri='https://www.google.com.tw/maps/search/'+Bank1
                                ),
                                URITemplateAction(
                                        label=Bank2,
                                        uri='https://www.google.com.tw/maps/search/'+Bank2
                                ),
                                URITemplateAction(
                                        label=Bank3,
                                        uri='https://www.google.com.tw/maps/search/'+Bank3
                                        
                                )
                            ]
                        )
                    ]
                )
    )
    return carousel_template_message

#財金節目列表
def financialprogram():
    ServiceList = ['錢線百分百', '財經8點檔', '關鍵字查詢']
    a = []
    for i in ServiceList:
        a.append(
            MessageTemplateAction(
                label=i,
                text=i)
        )
    carousel_template_message = TemplateSendMessage(
        alt_text='財經節目',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    # thumbnail_image_url='https://i.imgur.com/MPCafZS.png',
                    title='財經節目',
                    text='財經節目',
                    actions=a
                )
            ]
        )
    )
    return carousel_template_message

#-----------------貨幣追蹤---------------確認設定追蹤貨幣--------------------------
def CheckTrackCash(UserData):
    lis=[]
    flag=0
    if UserData["TrackCash"]=="":
        onlinediscuss = '尚未追蹤貨幣'
        carousel_template_message=ShowCashService()
        lis.append(TextSendMessage(text=onlinediscuss))
        lis.append(carousel_template_message)
        flag=1
    return lis,flag

#-----------------貨幣追蹤---------------確認設定現金即期--------------------------
def CheckCashSpot(UserData):
    lis=[]
    flag=0
    TrackCurrency=list(UserData["TrackCash"].keys())[0]
    ShowTemText = "目前" + TrackCurrency + "\n"
    cash=SearchCash()
    if UserData["TrackCash"][TrackCurrency]["CashSpot"]=="":
        onlinediscuss = '尚未設定現金或即期'

        SpotBuy=str(cash[TrackCurrency]["本行即期買入"])
        SpotSell=str(cash[TrackCurrency]["本行即期賣出"])
        CashSell=str(cash[TrackCurrency]["本行現金賣出"])
        CashBuy=str(cash[TrackCurrency]["本行現金買入"])
        
        ShowTemText="目前"+TrackCurrency+"\n"
        ShowTemText+="現金買入:"+CashBuy+"，現金賣出:"+CashSell+"\n"
        ShowTemText+="即期買入:"+SpotBuy+"，即期賣出:"+SpotSell+"\n"
        
        carousel_template_message = TrackCashOrSpot(ShowTemText)
        lis.append(TextSendMessage(text=onlinediscuss))
        lis.append(carousel_template_message)
        flag=1
    return lis,flag

#-----------------貨幣追蹤---------------確認設定追蹤方式--------------------------
def CheckTrackWay(UserData):
    lis=[]
    flag=0
    cash = SearchCash()
    TrackCurrency=list(UserData["TrackCash"].keys())[0]
    ShowTemText = "目前" + TrackCurrency + "\n"
    if UserData["TrackCash"][TrackCurrency]["TrackWay"]=="":
        onlinediscuss = '尚未設定追蹤方式'
        SpotBuy = str(cash[TrackCurrency]["本行即期買入"])
        SpotSell = str(cash[TrackCurrency]["本行即期賣出"])
        CashSell = str(cash[TrackCurrency]["本行現金賣出"])
        CashBuy = str(cash[TrackCurrency]["本行現金買入"])
    
        ShowTemText += "現金買入:" + CashBuy + "，現金賣出:" + CashSell + "\n"
        ShowTemText += "即期買入:" + SpotBuy + "，即期賣出:" + SpotSell + "\n"
        carousel_template_message = HowToTrackChoose(ShowTemText)
        lis.append(TextSendMessage(text=onlinediscuss))
        lis.append(carousel_template_message)
        flag=1
    return lis,flag

#-----------------貨幣追蹤---------------確認設定買入賣出--------------------------
def CheckBuySell(UserData):
    lis=[]
    flag=0
    cash = SearchCash()
    TrackCurrency=list(UserData["TrackCash"].keys())[0]
    ShowTemText = "目前" + TrackCurrency + "\n"
    if UserData["TrackCash"][TrackCurrency]["BuySell"]=="":
        onlinediscuss = '尚未設定買入或賣出'
        TrackCurrency=list(UserData["TrackCash"].keys())[0]
        ShowTemText = "目前" + TrackCurrency + "\n"
        CashSpot=UserData["TrackCash"][TrackCurrency]["CashSpot"]
        CashSell=str(cash[TrackCurrency]["本行"+CashSpot+"賣出"])
        CashBuy=str(cash[TrackCurrency]["本行"+CashSpot+"買入"])
        ShowTemText+=CashSpot+"買入:"+CashBuy+"\n"
        ShowTemText+=CashSpot+"賣出:"+CashSell
        lis.append(TextSendMessage(text=onlinediscuss))
        carousel_template_message=ProcessBuySell(ShowTemText)
        lis.append(carousel_template_message)
        flag=1
    return lis,flag

#-----------------貨幣追蹤---------------確認設定目標匯率--------------------------
def CheckTrackRate(UserData):
    lis=[]
    flag=0
    cash = SearchCash()
    TrackCurrency=list(UserData["TrackCash"].keys())[0]
    ShowTemText = "目前" + TrackCurrency + "\n"
    if UserData["TrackCash"][TrackCurrency]["ExceptRate"]=="":
        onlinediscuss = '尚未設定目標匯率'
        TrackWay=UserData["TrackCash"][TrackCurrency]["TrackWay"]
        CashSpot=UserData["TrackCash"][TrackCurrency]["CashSpot"]
        BuySell=UserData["TrackCash"][TrackCurrency]["BuySell"]
        TrackRate=cash[TrackCurrency]["本行"+CashSpot+BuySell]
        ShowTemText="目前"+TrackCurrency+"\n"
        ShowTemText+="本行"+CashSpot+BuySell+":"+str(TrackRate)+"\n"
        lis.append(TextSendMessage(text=onlinediscuss))
        UserData["TrackCash"][TrackCurrency]["TrackRate"]=BuySell
        if TrackWay=="升(降)百分比":
            lis.append(TextSendMessage(text=ShowTemText+"\n請輸入要升(降)的百分比\n，例:輸入 5%"))
        else:
            lis.append(TextSendMessage(text=ShowTemText+"\n請輸入要升(降)至的部位\n，例:輸入 32.5"))
        flag=1
    return lis,flag

def FCtype():
    qrm = TextSendMessage(
        text="請選擇貨幣類別:",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="美金", text="美金ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="日幣", text="日幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="港幣", text="港幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="歐元", text="歐元ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="人民幣", text="人民幣ATM")
                ),
            ]))
    return qrm

def FATMLists0():         #美日
    qrm = TextSendMessage(
        text="請選擇所屬銀行:",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="台銀", text="台銀外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="一銀", text="第一銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="彰銀", text="彰化銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="國泰", text="國泰外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="兆豐", text="兆豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="花旗", text="花旗外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="新光", text="新光外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="元大", text="元大外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="永豐", text="永豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="玉山", text="玉山外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="台新", text="台新外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="中信", text="中信外幣ATM")
                ),
            ]))
    return qrm

def FATMLists1():            #港幣
    qrm = TextSendMessage(
        text="請選擇所屬銀行:",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="台銀", text="台銀外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="一銀", text="第一銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="彰銀", text="彰化銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="兆豐", text="兆豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="花旗", text="花旗外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="永豐", text="永豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="玉山", text="玉山外幣ATM")
                ),
            ]))
    return qrm

def FATMLists2():             #歐元
    qrm = TextSendMessage(
        text="請選擇所屬銀行:",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="彰銀", text="彰化銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="兆豐", text="兆豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="花旗", text="花旗外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="台新", text="台新外幣ATM")
                ),
            ]))
    return qrm
def FATMLists3():            #人民幣
    qrm = TextSendMessage(
        text="請選擇所屬銀行:",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="台銀", text="台銀外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="一銀", text="第一銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="彰銀", text="彰化銀行外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="兆豐", text="兆豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="花旗", text="花旗外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="新光", text="新光外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="永豐", text="永豐外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="玉山", text="玉山外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="台新", text="台新外幣ATM")
                ),
                QuickReplyButton(
                    action=MessageAction(label="中信", text="中信外幣ATM")
                ),
            ]))
    return qrm
# -------------------------銀行、幣別-----------------------------------
def bankfn(num):
    if num == 1:
        name = '美金'
        return name
    elif num == 2:
        name = '日幣'
        return name
    elif num == 3:
        name = '港幣'
        return name
    elif num == 4:
        name = '歐元'
        return name
    elif num == 5:
        name = '人民幣'
        return name

def banksmap(bks,site):
    FCATMStartLocation = "https://www.google.com.tw/maps/dir/{}/{}".format(site, bks)
    GO = TemplateSendMessage(
        alt_text="路線",
        template=ButtonsTemplate(
            text="前往的外幣ATM為:\n{}\n實際可提幣別視實機而定。".format(bks),
            actions=[
                URITemplateAction(
                    label='前往地圖!',
                    uri=FCATMStartLocation
                )
            ]
        )
    )
    return GO

FCATMList = ["台銀外幣ATM", "第一銀行外幣ATM", "彰化銀行外幣ATM", "國泰外幣ATM", "兆豐外幣ATM",
                 "花旗外幣ATM", "新光外幣ATM", "元大外幣ATM", "永豐外幣ATM", "玉山外幣ATM",
                 "台新外幣ATM", "中信外幣ATM"]
FCList = ["美金ATM", "日幣ATM", "港幣ATM", "歐元ATM", "人民幣ATM"]
