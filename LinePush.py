from ProcessData import*

now=datetime.now().strftime("%H:%M")
schedule.every().day.at("08:00").do(PushCash)
schedule.every().day.at("21:28").do(PushMessage)
while True:
    schedule.run_pending()