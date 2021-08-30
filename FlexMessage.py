# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
from linebot.models import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

#------------------推播設定所顯示之文字---------------------------------
def ShowPushSetting(DayAlarm,WeekCycle,MaxWord,NewsDaySwitch):
    if MaxWord=="無":
        Message="尚未到達推播所需次數"
    else:
        Message=MaxWord
    a=""
    co=0
    for i in range(0,len(WeekCycle)):
        if WeekCycle[i]==1:
            co=1
            if i==0:
                a+="一"
            elif i==1:
                a+="二"
            elif i==2:
                a+="三"
            elif i==3:
                a+="四"
            elif i==4:
                a+="五"
            elif i==5:
                a+="六"
            elif i==6:
               a+="日"
    if co==0:
        a="尚未設定"
    
    
    flex_message = FlexSendMessage(
            alt_text='推播設定列表',
            contents={
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "推播設定",
                    "weight": "bold",
                    "size": "xl"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您現在的推播時間是:早上9點",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您現在的推播週期為:"+a,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您現在的推播字詞為:"+Message,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                          {
                            "type": "text",
                            "text": "您現在的推播開關為:"+NewsDaySwitch,
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md",
                            "flex": 0
                          }
                        ]
                      }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "時間設定",
                      "text": "推播時間設定"
                    }
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "週期設定",
                      "text": "週期設定"
                    }
                  },
                    {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "推播開關設定",
                      "text": "推播開關設定"
                    }
                  }
                ]
              }
        }
    )
    return flex_message

#--------------------------推播通知開關設定----------------------------------------
def NewsDaySwitchSetting(DayAlarm,WeekCycle,MaxWord,NewsDaySwitch):
    if MaxWord=="無":
        Message="尚未到達推播所需次數"
    else:
        Message=MaxWord
    a=""
    co=0
    for i in range(0,len(WeekCycle)):
        if WeekCycle[i]==1:
            co=1
            if i==0:
                a+="一"
            elif i==1:
                a+="二"
            elif i==2:
                a+="三"
            elif i==3:
                a+="四"
            elif i==4:
                a+="五"
            elif i==5:
                a+="六"
            elif i==6:
               a+="日"
    if co==0:
        a="尚未設定"
    
    
    flex_message = FlexSendMessage(
            alt_text='推播設定列表',
            contents={
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "推播開關設定",
                    "weight": "bold",
                    "size": "xl"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您現在的推播時間是:"+DayAlarm,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您現在的推播週期為:"+a,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您現在的推播字詞為:"+Message,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                          {
                            "type": "text",
                            "text": "您現在的推播開關為:"+NewsDaySwitch,
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md",
                            "flex": 0
                          }
                        ]
                      }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "開啟",
                      "text": "推播通知開啟"
                    }
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "關閉",
                      "text": "推播通知關閉"
                    }
                  }
                ]
              }
        }
    )
    return flex_message

'''
def BankListService(atm):
    BankList=["台灣銀行","土地銀行","合作金庫",
              "第一銀行","華南銀行","彰化銀行",
              "上海銀行","富邦銀行","國泰世華",
              "中國輸出","高雄銀行","兆豐銀行",
              "花旗銀行","王道銀行","台灣企銀",
              "渣打銀行","台中銀行","京城銀行",
              "匯豐銀行","瑞興銀行","華泰銀行",
              "新光銀行","陽信銀行","板信銀行",
              "三信銀行","聯邦銀行","遠東商銀",
              "元大銀行","永豐銀行","玉山銀行",
              "凱基銀行","星辰銀行","台新銀行",
              "日盛銀行","安泰銀行","中國信託"]
    content=[]
    for i in range(0,len(BankList),6):
        if atm!="ATM":
            b=[{
                "type": "text",
                "text": "銀行列表",
                "weight": "bold",
                "size": "xl"
            }]
        else:
            b=[{
                "type": "text",
                "text": "ATM列表",
                "weight": "bold",
                "size": "xl"
            }]
        for j in range(i,i+6,2):
            a=[]
            for k in range(j,j+2):
                if atm!="ATM":
                    a.append({
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": BankList[k],
                          "uri": 'https://www.google.com.tw/maps/search/'+BankList[k]
                        }
                      })
                else:
                    a.append({
                        "type": "button",
                        "action": {
                          "type": "uri",
                          "label": BankList[k],
                          "uri": 'https://www.google.com.tw/maps/search/'+BankList[k]+'ATM'
                        }
                      })
            b.append({
                "type": "box",
                "layout": "horizontal",
                "contents":a}
            )
        content.append({
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents":b
            }
          })
    flex_message = FlexSendMessage(
    alt_text='銀行列表',
    contents={
      "type": "carousel",
      "contents": content
     })
    return flex_message
'''
#----------------------推播設定-----------設定推播時間-----------------------------
def TimeService():
    TimeList=["0","1","2","3",
              "4","5","6","7",
              "8","9","10","11",
              "12","13","14","15",
              "16","17","18","19",
              "20","21","22","23"]
    
    c=[{
        "type": "text",
        "text": "時間設定",
        "weight": "bold",
        "size": "xl"
        }]
    for i in range(0,len(TimeList),4):
        a=[]
        for j in range(i,i+4):
            if len(TimeList[j])==2:
                a.append({
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": TimeList[j],
                          "text": TimeList[j]+":00"
                        }
                      })
            else:
                a.append({
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": TimeList[j],
                          "text": "0"+TimeList[j]+":00"
                        }
                      })
        c.append({"type": "box",
                "layout": "horizontal",
                "contents":a})
    flex_message = FlexSendMessage(
    alt_text='銀行列表',
    contents={
      "type": "bubble",
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents":c
          }
     })
    return flex_message

#--------------------------信用卡情報---------------------------
def CreditCard():
    url='https://www.ptt.cc/bbs/creditcard/search?q=%5B%E6%83%85%E5%A0%B1%5D'
    response = requests.get(url,timeout=30)
    response.encoding = 'UTF-8-sig'
    input_html = response.text
    soup = BeautifulSoup(input_html,"html.parser")
    
    lisname=[]
    lishref=[]
    
    for item in soup.select(".r-ent"):
        if item.select(".title")[0].text.strip()[0]=='R' and item.select(".title")[0].text.strip()[1]=='e' and item.select(".title")[0].text.strip()[2]==':':
            continue
        lisname.append(item.select(".title")[0].text.strip())
        lishref.append('https://www.ptt.cc/'+item.find('a').get('href'))
        
    flex_message = FlexSendMessage(
    alt_text='信用卡情報',
    contents=
    {
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#FF0000",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[0],
              "altUri": {
                "desktop": lishref[0]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[0][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        },
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#F75000",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[1],
              "altUri": {
                "desktop": lishref[1]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[1][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        },
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#FFE153",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[2],
              "altUri": {
                "desktop": lishref[2]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[2][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        },
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#A8FF24",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[3],
              "altUri": {
                "desktop": lishref[3]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[3][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        },
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#0000FF",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[4],
              "altUri": {
                "desktop": lishref[4]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[4][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        },
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#4B0080",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[5],
              "altUri": {
                "desktop": lishref[5]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[5][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        },
        {
          "type": "bubble",
          "size": "nano",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "前往",
                "color": "#ffffff",
                "align": "start",
                "size": "md",
                "gravity": "center"
              }
            ],
            "backgroundColor": "#8B00FF",
            "paddingAll": "lg",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": lishref[6],
              "altUri": {
                "desktop": lishref[6]
              }
            }
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": lisname[6][5:],
                    "color": "#8C8C8C",
                    "size": "sm",
                    "wrap": True
                  }
                ],
                "flex": 1
              }
            ],
            "spacing": "md",
            "paddingAll": "12px"
          },
          "styles": {
            "footer": {
              "separator": False
            }
          }
        }
      ]
    }
    )
    return flex_message

#-------------------------洨幫手-----------------------------------
def HelperQ():
    qrm = TextSendMessage(
        text='請問您想了解...',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label="外幣服務", text="#說明外幣服務#")
                ),
                QuickReplyButton(
                    action=MessageAction(label="銀行位置服務", text="#說明銀行位置服務#")
                ),
                QuickReplyButton(
                    action=MessageAction(label="推播設定", text="#說明推播設定#")
                ),
                QuickReplyButton(
                    action=MessageAction(label="news新聞", text="#說明news功能#")
                ),
                QuickReplyButton(
                    action=MessageAction(label="財經節目", text="#說明財經節目功能#")
                ),
                QuickReplyButton(
                    action=MessageAction(label="金融知識庫", text="#說明金融知識庫#")
                ),
            ]))
    return qrm

# 銀行服務
def BankService():
    BS = TextSendMessage(
        text='以下為銀行服務',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="外幣服務", text="外幣服務")),
                QuickReplyButton(action=MessageAction(label="ATM位置服務", text="找銀行或ATM")),
                QuickReplyButton(action=MessageAction(label="信用卡情報", text="信用卡情報")),
            ]))
    return BS

def OtherInfo():
    OInfo = TextSendMessage(
        text='以下為其他資訊',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="新聞服務", text="新聞服務")),
                QuickReplyButton(action=MessageAction(label="MoneyDJ理財網新聞", text="MoneyDJ理財網新聞")),
                QuickReplyButton(action=MessageAction(label="財經節目", text="財經節目")),
            ]))
    return OInfo
#外幣服務
def FScrvice():
    OInfo = TextSendMessage(
        text='以下為外幣服務',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="目前匯率查詢", text="目前匯率查詢")),
                QuickReplyButton(action=MessageAction(label="貨幣分析", text="貨幣分析")),
                QuickReplyButton(action=MessageAction(label="貨幣追蹤", text="貨幣追蹤")),
                # URITemplateAction(label='匯率新聞', uri='https://news.cnyes.com/news/cat/forex?exp=a')
            ]))
    return OInfo
    
#---------------------------youtube-----------------------------------------------
def youtube_channel():
    lsurl = [
        'https://m.youtube.com/results?search_query=%E9%8C%A2%E7%B7%9A%E7%99%BE%E5%88%86%E7%99%BE&sp=CAISBAgFEAE%253D',
        'https://m.youtube.com/channel/UCYDaGPmMfSXViITpPYDKIcw/featured',
        'https://www.youtube.com/results?search_query=%E8%B2%A1%E7%B6%938%E9%BB%9E%E6%AA%94&sp=CAISBAgFEAE%253D',
        'https://www.youtube.com/channel/UCQvsuaih5lE0n_Ne54nNezg',
        'https://www.youtube.com/user/CMoneySchool']  

    flex_message = FlexSendMessage(
        alt_text="youtube_channel",
        contents=
        {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://yt3.ggpht.com/a/AATXAJzuTeSk05um_2Uzg1mTnfLfalH-rAJE6iGMWrik=s88-c-k-c0x00ffffff-no-rj",
                        "aspectMode": "fit",
                        "aspectRatio": "350:210",
                        "size": "full",
                        "backgroundColor": "#132669"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "錢線百分百",
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                            },
                            {
                                "type": "text",
                                "text": "\n前往觀看!",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                                "color": "#9f907f",
                                "action": {
                                    "type": "uri",
                                    "label": "start",
                                    "uri": lsurl[0],
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "\n#在 Youtube 觀看#",
                                                "wrap": True,
                                                "color": "#8c8c8c",
                                                "size": "xxs",
                                                "align": "center",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    }
                },
                # ---------------------------------------------------------------------------------財經大白話
                {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://yt3.ggpht.com/a/AATXAJwwxNtwBJ7hLLPHi2bzQC2GmnF5fpOY4-kiBu7d=s88-c-k-c0x00ffffff-no-rj",
                        "aspectMode": "fit",
                        "aspectRatio": "350:210",
                        "size": "full",
                        "backgroundColor": "#fbc588"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "財經大白話",
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                            },
                            {
                                "type": "text",
                                "text": "\n前往觀看!",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                                "color": "#9f907f",
                                "action": {
                                    "type": "uri",
                                    "label": "start",
                                    "uri": lsurl[1],
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "\n#在 Youtube 觀看#",
                                                "wrap": True,
                                                "color": "#8c8c8c",
                                                "size": "xxs",
                                                "align": "center",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    }
                },
                # ---------------------------------------------------------------------------------財經8點檔
                {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://lh3.googleusercontent.com/sYHSOE5GKZY3IVfHGvFjy4snOVxTJNFDnXEvhAb8vU_9F0K5ydqMHrKzEqnX-xz0Hblq5A=s170",
                        "aspectMode": "fit",
                        "aspectRatio": "350:210",
                        "size": "full",
                        "backgroundColor": "#c9b9db"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "財經8點檔",
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                            },
                            {
                                "type": "text",
                                "text": "\n前往觀看!",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                                "color": "#9f907f",
                                "action": {
                                    "type": "uri",
                                    "label": "start",
                                    "uri": lsurl[2],
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "\n#在 Youtube 觀看#",
                                                "wrap": True,
                                                "color": "#8c8c8c",
                                                "size": "xxs",
                                                "align": "center",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    }
                },
                # -----------------------------------------理財達人秀
                {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://imgur.com/SJPH542.jpg",
                        "aspectMode": "fit",
                        "aspectRatio": "350:210",
                        "size": "full",
                        "backgroundColor": "#000000"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "理財達人秀",
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                            },
                            {
                                "type": "text",
                                "text": "\n前往觀看!",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                                "color": "#9f907f",
                                "action": {
                                    "type": "uri",
                                    "label": "start",
                                    "uri": lsurl[3],
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "\n#在 Youtube 觀看#",
                                                "wrap": True,
                                                "color": "#8c8c8c",
                                                "size": "xxs",
                                                "align": "center",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    }
                },
                # --------------------------------------- 理財寶
                {
                    "type": "bubble",
                    "size": "micro",
                    "hero": {
                        "type": "image",
                        "url": "https://imgur.com/dPW0jcC.jpg",
                        "aspectMode": "fit",
                        "aspectRatio": "350:210",
                        "size": "full",
                        "backgroundColor": "#AA0000"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "理財寶",
                                "weight": "bold",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                            },
                            {
                                "type": "text",
                                "text": "\n前往觀看!",
                                "size": "xl",
                                "wrap": True,
                                "align": "center",
                                "color": "#9f907f",
                                "action": {
                                    "type": "uri",
                                    "label": "start",
                                    "uri": lsurl[4],
                                }
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "\n#在 Youtube 觀看#",
                                                "wrap": True,
                                                "color": "#8c8c8c",
                                                "size": "xxs",
                                                "align": "center",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "spacing": "sm",
                        "paddingAll": "13px"
                    }
                },

                
            ]
        }
    )
    return flex_message


def YoutubeKeys():
    YTK = TextSendMessage(
        text='您可以輸入K加上關鍵字\n例: K 美金\n即可搜尋美金\n或者選擇以下Tag',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="外幣", text="K 外幣")),
                QuickReplyButton(action=MessageAction(label="股票", text="K 股票")),
                QuickReplyButton(action=MessageAction(label="ETF", text="K ETF")),
                QuickReplyButton(action=MessageAction(label="人工智慧", text="K 人工智慧")),
                QuickReplyButton(action=MessageAction(label="機器人", text="K 機器人")),     
                QuickReplyButton(action=MessageAction(label="5G", text="K 5G")),          
                QuickReplyButton(action=MessageAction(label="電動車", text="K 電動車")),          
            ]))
    return YTK

# 財經關鍵字
def NewsKeys(txt):
    # from urllib.parse import quote
    # strr = quote('繁體')
    # print(strr)

    txts = quote(txt)
    lishref = []
    lishref.append(
        'https://m.youtube.com/results?search_query=%22%E9%8C%A2%E7%B7%9A%E7%99%BE%E5%88%86%E7%99%BE%22%2B%22{}%22&sp=EgIIBQ%253D%253D'.format(
            txts))
    lishref.append(
        'https://m.youtube.com/results?search_query=%22%E8%B2%A1%E7%B6%93%E5%A4%A7%E7%99%BD%E8%A9%B1%22%2B%22{}%22&sp=EgIIBQ%253D%253D'.format(
            txts))
    lishref.append(
        'https://m.youtube.com/results?search_query=%22%E8%B2%A1%E7%B6%938%E9%BB%9E%E6%AA%94%22%2B%22{}%22&sp=EgIIBQ%253D%253D'.format(
            txts))
    lishref.append(
        'https://m.youtube.com/results?search_query=%22%E7%90%86%E8%B2%A1%E9%81%94%E4%BA%BA%E7%A7%80%22%2B%22{}%22&sp=EgIIBQ%253D%253D'.format(
            txts))
    lishref.append(
        'https://m.youtube.com/results?search_query=%22CMoney%E7%90%86%E8%B2%A1%E5%AF%B6%22%2B%22{}%22&sp=EgIIBQ%253D%253D'.format(
            txts))
    print(lishref)
    flex_message = FlexSendMessage(
        alt_text='頻道觀賞',
        contents=
        {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "size": "nano",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "前往",
                                "color": "#ffffff",
                                "align": "start",
                                "size": "md",
                                "gravity": "center"
                            }
                        ],
                        "backgroundColor": "#FF0000",
                        "paddingAll": "lg",
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": lishref[0],
                            "altUri": {
                                "desktop": lishref[0]
                            }
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "節目:\n錢線百分百\n關鍵字:\n{}\n#Youtube觀看".format(txt),
                                        "color": "#8C8C8C",
                                        "size": "sm",
                                        "wrap": True
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "spacing": "md",
                        "paddingAll": "12px"
                    },
                    "styles": {
                        "footer": {
                            "separator": False
                        }
                    }
                },
                {
                    "type": "bubble",
                    "size": "nano",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "前往",
                                "color": "#ffffff",
                                "align": "start",
                                "size": "md",
                                "gravity": "center"
                            }
                        ],
                        "backgroundColor": "#F75000",
                        "paddingAll": "lg",
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": lishref[1],
                            "altUri": {
                                "desktop": lishref[1]
                            }
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "節目:\n財經大白話\n關鍵字:\n{}\n#Youtube觀看".format(txt),
                                        "color": "#8C8C8C",
                                        "size": "sm",
                                        "wrap": True
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "spacing": "md",
                        "paddingAll": "12px"
                    },
                    "styles": {
                        "footer": {
                            "separator": False
                        }
                    }
                },
                {
                    "type": "bubble",
                    "size": "nano",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "前往",
                                "color": "#ffffff",
                                "align": "start",
                                "size": "md",
                                "gravity": "center"
                            }
                        ],
                        "backgroundColor": "#FFE153",
                        "paddingAll": "lg",
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": lishref[2],
                            "altUri": {
                                "desktop": lishref[2]
                            }
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "節目:\n財經8點檔\n關鍵字:\n{}\n#Youtube觀看".format(txt),
                                        "color": "#8C8C8C",
                                        "size": "sm",
                                        "wrap": True
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "spacing": "md",
                        "paddingAll": "12px"
                    },
                    "styles": {
                        "footer": {
                            "separator": False
                        }
                    }
                },
                {
                    "type": "bubble",
                    "size": "nano",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "前往",
                                "color": "#ffffff",
                                "align": "start",
                                "size": "md",
                                "gravity": "center"
                            }
                        ],
                        "backgroundColor": "#A8FF24",
                        "paddingAll": "lg",
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": lishref[3],
                            "altUri": {
                                "desktop": lishref[3]
                            }
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "節目:\n理財達人秀\n關鍵字:\n{}\n#Youtube觀看".format(txt),
                                        "color": "#8C8C8C",
                                        "size": "sm",
                                        "wrap": True
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "spacing": "md",
                        "paddingAll": "12px"
                    },
                    "styles": {
                        "footer": {
                            "separator": False
                        }
                    }
                },
                {
                    "type": "bubble",
                    "size": "nano",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "前往",
                                "color": "#ffffff",
                                "align": "start",
                                "size": "md",
                                "gravity": "center"
                            }
                        ],
                        "backgroundColor": "#0000FF",
                        "paddingAll": "lg",
                        "action": {
                            "type": "uri",
                            "label": "action",
                            "uri": lishref[4],
                            "altUri": {
                                "desktop": lishref[4],
                            }
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "節目:\nCMoney\n理財寶\n關鍵字:\n{}\n#Youtube觀看".format(txt),
                                        "color": "#8C8C8C",
                                        "size": "sm",
                                        "wrap": True
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "spacing": "md",
                        "paddingAll": "12px"
                    },
                    "styles": {
                        "footer": {
                            "separator": False
                        }
                    }
                }
            ]
        }
    )
    return flex_message

#--------------------------貨幣追蹤設定----------------------------------
def FlexTrackCashService(Word):
    content="無"
    if Word=="無":
        content=[{
                    "type": "text",
                    "text": "您目前無追蹤的貨幣"
                  }]
    else:
        content=[
                  {
                    "type": "text",
                    "text": "您目前追蹤的貨幣為:"+Word[0]
                  },
                  {
                    "type": "text",
                    "text": "開始日期為:"+Word[1]
                  },
                  {
                    "type": "text",
                    "text": "結束日期為:"+Word[2]
                  },
                  {
                    "type": "text",
                    "text": "追蹤方式為:"+Word[3]+"   "+Word[4]
                  },
                  {
                    "type": "text",
                    "text": "現金或即期:"+Word[5]
                  },
                  {
                    "type": "text",
                    "text": Word[0]+"目前"+Word[5]+Word[3]+"為:"+Word[6]
                  }
                ]
    flex_message = FlexSendMessage(
            alt_text='貨幣追蹤服務',
            contents={
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "vertical",
                "contents": content
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "貨幣列表",
                          "text": "貨幣列表"
                        }
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "現金或即期",
                          "text": "現金或即期"
                        }
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "追蹤方式",
                          "text": "追蹤方式"
                        }
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "買入或賣出",
                          "text": "買入或賣出"
                        }
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "目標匯率設定",
                          "text": "目標匯率設定"
                        }
                      },
                      {
                        "type": "button",
                        "action": {
                          "type": "message",
                          "label": "追蹤天數設定",
                          "text": "追蹤天數設定"
                        }
                      }
                    ]
                  },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                          {
                            "type": "button",
                            "action": {
                              "type": "message",
                              "label": "通知開關設定",
                              "text": "通知開關設定"
                            }
                          }
                        ]
                      }
                ]
              }
            }
    )
    return flex_message

def MemberCenter(UserName):
    flex_message = FlexSendMessage(
            alt_text='會員中心',
            contents={
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "http://linecorp.com/"
                }
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "會員中心",
                    "weight": "bold",
                    "size": "xl"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                      {
                        "type": "text",
                        "text": "您好，"+UserName,
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                      }
                    ]
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                      "type": "message",
                      "label": "設定",
                      "text": "推播設定"
                    }
                  },
                  {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                      "type": "message",
                      "label": "我的收藏",
                      "text": "我的收藏"
                    }
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "常見問題",
                      "text": "小幫手"
                    }
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "回饋",
                      "text": "回饋"
                    }
                  }
                ],
                "flex": 0
              }
            }
        )
    return flex_message