from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia
import threading


api = "AIzaSyBvcDnn2upjJwSWw89RDx99lFaIv2DCif0"
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)


app = Flask(__name__)
flag = 1
@app.route("/",methods=["POST", "GET"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["POST","GET"])
def main():
    global flag
    if flag == 1:
        user_name = request.form.get("q")
        t = datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?,?)",(user_name, t))
        conn.commit()
        c.close()
        conn.close()
        flag = 0

    return(render_template("main.html"))

@app.route("/foodexp",methods=["POST","GET"])
def foodexp():
    return(render_template("foodexp.html"))

@app.route("/foodexp1",methods=["POST","GET"])
def foodexp1():
    return(render_template("foodexp1.html"))
 
@app.route("/foodexp2",methods=["POST","GET"])
def foodexp2():
    return(render_template("foodexp2.html"))

@app.route("/FAQ",methods=["POST","GET"])
def FAQ():
    return(render_template("FAQ.html"))

@app.route("/FAQ1",methods=["POST","GET"])
def FAQ1():
    r=model.generate_content("Factors for Profit")
    r=r.candidates[0].content.parts[0].text
    return(render_template("FAQ1.html",r=r))

@app.route("/ethical_test",methods=["POST","GET"])
def ethical_test():
    return(render_template("ethical_test.html"))

@app.route("/test_result",methods=["POST","GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))

@app.route("/foodexp_pred",methods=["POST","GET"])
def test_rfoodexp_predesult():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html",r=(q*0.4851)+147.4))

@app.route("/userLog",methods=["POST","GET"])
def userLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
        r = r + str(row) + "\n"
    print(r)
    c.close()
    conn.close()
    return(render_template("userLog.html",r=r))

import threading

@app.route("/telegram_predict", methods=["POST", "GET"])
def telegram_predict():
    def start_bot():
        import time
        import requests

        telegram_api = "7845485789:AAFfSdEIiRcdPP40xxpknxwr_fH6u0oFrh0"  # ⚠️ 建议替换为安全方式，例如读取环境变量
        url = f"https://api.telegram.org/bot{telegram_api}/"
        updates = url + 'getUpdates'

        print("Waiting for user to send the first message...")

        chat_id = None
        while not chat_id:
            try:
                r = requests.get(updates).json()
                if "result" in r and len(r["result"]) > 0:
                    last_msg = r["result"][-1]["message"]
                    chat_id = last_msg["chat"]["id"]
                    print("Chat ID acquired:", chat_id)
            except Exception as e:
                print("Error getting updates:", e)
            time.sleep(2)

        prompt = "Please enter the inflation rate in %(type exit to break): "
        err_msg = "Please enter a number"

        # 发第一条提示消息
        msg = url + f"sendMessage?chat_id={chat_id}&text={prompt}"
        requests.get(msg)

        flag = ""
        while True:
            time.sleep(5)
            try:
                r = requests.get(updates).json()
                if "result" not in r or len(r["result"]) == 0:
                    continue
                last_msg = r["result"][-1]["message"]
                user_input = last_msg["text"]

                if flag != user_input:
                    flag = user_input
                    if user_input.isnumeric():
                        reply = "The predicted interest rate is " + str(float(user_input) + 1.5)
                        msg = url + f"sendMessage?chat_id={chat_id}&text={reply}"
                        requests.get(msg)
                    else:
                        if user_input.lower() == "exit":
                            break
                        else:
                            msg = url + f"sendMessage?chat_id={chat_id}&text={err_msg}"
                            requests.get(msg)
            except Exception as e:
                print("Error during processing:", e)
            time.sleep(8)

    # 启动后台线程
    threading.Thread(target=start_bot).start()

    return render_template("telegram_predict.html")


@app.route("/deleteLog",methods=["POST","GET"])
def deleteLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("deleteLog.html"))


@app.route("/FAQinput",methods=["POST","GET"])
def FAQinput():
     q  = request.form.get("q")
     r=wikipedia.summary(q)
     return(render_template("FAQinput.html",r=r))

if __name__ == "__main__":
    app.run()
