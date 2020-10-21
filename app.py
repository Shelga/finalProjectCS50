from flask import Flask, render_template, redirect, session, request

from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3

import matplotlib.pyplot as plot

import numpy as np

import pandas as pd

import io

import base64

import json

import collections





app = Flask(__name__)

connection = sqlite3.connect("project.db", check_same_thread=False)
db = connection.cursor()

app.secret_key = "b'\x8cU\xd7\xcd\x8d\xeb\xb4m\xbfJ\xb5\xdcM\xba\xc3\x8e'"

@app.route('/barchart')
def build_plot():


    # x = []
    # arrs = db.execute("SELECT value FROM light_value")
    # arrs = db.fetchall()
    # for arr in arrs:
    #     t = (row[0], row[1], row[2], row[3])
    #     x.append(t)
    # j = json.dumps(x)
    # print("j", j)

    #     x.append(arr[0])
    # true_arr_light = list(x)
    # print("true_arr_light", true_arr_light)


 


# for row in rows:
#     t = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
#     rowarray_list.append(t)
# j = json.dumps(rowarray_list)

    
    y = []
    dates = db.execute("SELECT date FROM light_value")
    dates = db.fetchall()
    for date in dates:
        y.append(date[0])
    true_date_light = list(y)
    print("true_date_light", true_date_light)

    

    return render_template("barchart.html", true_arr_light=true_arr_light, true_date_light=true_date_light)


@app.route('/register', methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        # print('username', username)
        password = request.form.get("password")
        # print("password", password)
        hash = generate_password_hash(request.form.get("password"))
        # print('hash', hash)

        if not username:
            return render_template("apology_reg.html", message = "You must provide a username")

        elif not password:
            return render_template("apology_reg.html", message = "You must provide a password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("apology_reg.html", message = "The confirmation is incorrect")


        db.execute("SELECT COUNT(*) FROM login WHERE username = :username", {"username": request.form.get("username")})
        records = db.fetchone()
        # records_len = len(records)
        records_row = records[0]
        # print("records_row", records_row)
        # print("records", records)
        # print("records_len", records_len)

        if records_row == 1:
            return render_template("apology_reg.html", message = "Username already taken")

        db.execute("INSERT INTO login (username, hash) VALUES (?, ?)", (username, hash))
        connection.commit()

        return redirect("/index")

    if request.method == "GET":
        return render_template("register.html")



@app.route('/login', methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("apology_log.html", message = "You must provide a username")

        elif not request.form.get("password"):
            return render_template("apology_log.html", message = "You must provide a password")

        db.execute("SELECT COUNT(*) FROM login WHERE username = :username", {"username": request.form.get("username")})
        records = db.fetchone()
        # records_len = len(records)
        records_row = records[0]
        # print("records_row", records_row)
        # print("records", records)
        # print("records_len", records_len)

        if records_row == 0:
            return render_template("apology_log.html", message = "Invalid username")
  

        rows = db.execute("SELECT * FROM login WHERE username = :username", {"username": request.form.get("username")})
        print("rows", rows)
        for row in rows:
            global row_id
            # global row_name
            global row_pass
            row_id = row[0]
            # row_name = row[1]
            row_pass = row[2]
            # print("row_id", row_id)
            # print("row_name", row_name)
            # print("row_pass", row_pass)
            # print("password", request.form.get("password"))
            # hash = generate_password_hash(request.form.get("password"))
            # print("hash", hash)

        if not check_password_hash(row_pass, request.form.get("password")):
            return render_template("apology_log.html", message = "Invalid password")
        
        # db.execute("SELECT COUNT(*) FROM login WHERE username = :username", {"username": request.form.get("username")})
        # records = db.fetchall()
        # records_len = len(records)
        # print("records_len", records_len)

        return redirect("/index")

    if request.method == "GET":
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    # session.pop("username", None)
    return render_template("login.html")


@app.route('/')
def index():

    global water_today_value
    global count_water_today_total
    global light_today_value
    global count_light_today_total
    global heater_today_value
    global count_heater_today_total


    # rows = db.execute("SELECT * FROM water")
    # print("rows", rows)
    # for row in rows:
        # print("rows_index", rows)
        # global water_today_id
        # water_today_id = row[0]
        # print("water_today_id_index", water_today_id)

        # water_today_value = row[1]
        # print("water_today_value", water_today_value)

        # water_yesterday_id = water_today_id - 1
        # print("water_yesterday_id", water_yesterday_id)

        # toos = db.execute("SELECT value FROM water WHERE id = id", {"id": water_yesterday_id})
    toos = db.execute("SELECT value FROM water")
    toos = db.fetchall()
    for too in toos:
        global water_yesterday_value
    water_yesterday_value = toos[-2][0]
    # print("index_water_yesterday_value", water_yesterday_value)
    water_today_value = toos[-1][0]
    # print("index_water_today_value", water_today_value)
        # print("toos", toos) 
        
    count_water_today_total = round((water_today_value - water_yesterday_value), 4)
    # print("water_yesterday_value", water_yesterday_value)
    # print("count_water_today_total", count_water_today_total)

    lows = db.execute("SELECT * FROM light")
    # print("lows", lows)
    for low in lows:
        global light_today_id
           
        light_today_id = low[0]
        # print("light_today_id", light_today_id)
        light_today_value = low[1]
        # print("light_today_value", light_today_value)
        light_yesterday_id = light_today_id - 1
        # print("light_yesterday_id", light_yesterday_id)

        loos = db.execute("SELECT value FROM light WHERE id = id", {"id": light_yesterday_id})
        loos = db.fetchall()
        for loo in loos:
            global light_yesterday_value
        light_yesterday_value = loos[-2][0]
        # print("loos", loos)
        
        
        count_light_today_total = round((light_today_value - light_yesterday_value), 4)
        # print("light_yesterday_value", light_yesterday_value)
        # print("count_light_today_total", count_light_today_total)


        rows = db.execute("SELECT * FROM heater")
        # print("rows", rows)
        for row in rows:
            global heater_today_id
            heater_today_id = row[0]
            # print("heater_today_id", heater_today_id)

        heater_today_value = row[1]
        # print("heater_today_value", heater_today_value)

        heater_yesterday_id = heater_today_id - 1
        # print("heater_yesterday_id", heater_yesterday_id)

        toos = db.execute("SELECT value FROM heater WHERE id = id", {"id": heater_yesterday_id})
        toos = db.fetchall()
        for too in toos:
            global heater_yesterday_value
        heater_yesterday_value = toos[-2][0]
        heater_today_value = toos[-1][0]
        # print("toos", toos) 
        
        count_heater_today_total = round((heater_today_value - heater_yesterday_value), 4)
        # print("heater_yesterday_value", heater_yesterday_value)
        # print("count_heater_today_total", count_heater_today_total)
  
        return render_template("/index.html", count_water_today_total = count_water_today_total, water_yesterday_value = water_yesterday_value, count_light_today_total=count_light_today_total, light_yesterday_value=light_yesterday_value, water_today_value=water_today_value, light_today_value=light_today_value, count_heater_today_total = count_heater_today_total, heater_yesterday_value = heater_yesterday_value)



@app.route('/water', methods=["GET", "POST"])
def water():

    if request.method == "POST":

        water = request.form.get("water")
        # print('water', water)

        if not request.form.get("water"):
            return render_template("apology_log.html", message = "You must provide a water")
        

        db.execute("INSERT INTO water (value) VALUES (?)", (water,))
        connection.commit()


        rows = db.execute("SELECT * FROM water WHERE value = :water", {"water": request.form.get("water")})
        # print("rows", rows)
        for row in rows:
            # print("!!!rows", row)
            global water_today_id
           
            water_today_id = row[0]
            # print("water_today_id", water_today_id)
            water_today_value = row[1]
            # print("water_today_value", water_today_value)
            water_yesterday_id = water_today_id - 1
            # print("water_yesterday_id", water_yesterday_id)

        toos = db.execute("SELECT value FROM water WHERE id = id", {"id": water_yesterday_id})
        toos = db.fetchall()
        for too in toos:
            global water_yesterday_value
        water_yesterday_value = toos[-1][0]
        # print("water_water_yesterday_value", water_yesterday_value)
        # print("toos", toos)
        
        
        count_water_today_total = round((water_today_value - water_yesterday_value), 4)
        # print("water_yesterday_value", water_yesterday_value)
        # print("count_water_today_total", count_water_today_total)

        db.execute("SELECT value FROM water")
        df = db.fetchall()
        # print("df", df)
        # print("data", data)
        
        
        return redirect("/")


    if request.method == "GET":
        return render_template("water.html", water_yesterday_value=water_yesterday_value)


@app.route('/light', methods=["GET", "POST"])
def light():

    if request.method == "POST":

        light = request.form.get("light")
        print('light', light)

        if not request.form.get("light"):
            return render_template("apology_log.html", message = "You must provide a light")
        

        db.execute("INSERT INTO light (value) VALUES (?)", (light,))
        connection.commit()


        rows = db.execute("SELECT * FROM light WHERE value = :light", {"light": request.form.get("light")})
        print("rows", rows)
        for row in rows:
            global light_today_id
           
            light_today_id = row[0]
            print("light_today_id", light_today_id)
            light_today_value = row[1]
            print("light_today_value", light_today_value)
            light_yesterday_id = light_today_id - 1
            print("light_yesterday_id", light_yesterday_id)

        toos = db.execute("SELECT value FROM light WHERE id = id", {"id": light_yesterday_id})
        toos = db.fetchall()
        for too in toos:
            global light_yesterday_value
        light_yesterday_value = toos[-2][0]
        print("toos", toos)
        
        
        count_light_today_total = round((light_today_value - light_yesterday_value), 4)
        print("light_yesterday_value", light_yesterday_value)
        print("count_light_today_total", count_light_today_total)

        db.execute("INSERT INTO light_valu (value) VALUES (?)", (count_light_today_total,))
        connection.commit()


        # x = []
        # arrs = db.execute("SELECT value FROM light_value")
        # arrs = db.fetchall()
        # for arr in arrs:
        #     x.append(arr[0])
        # true_arr_light = list(x)
        # print("true_arr_light", true_arr_light)

        # json_data = json.dumps(arrs)
        # print("json_data", json_data)


        # y = []
        # dates = db.execute("SELECT date FROM light_value")
        # dates = db.fetchall()
        # for date in dates:
        #     y.append(date[0])
        # true_date_light = list(y)
        # print("true_date_light", true_date_light)


    



        
        return redirect("/")


    if request.method == "GET":
        return render_template("light.html", light_yesterday_value=light_yesterday_value)




@app.route('/heater', methods=["GET", "POST"])
def heater():

    global heater_yesterday_value

    if request.method == "POST":

        heater = request.form.get("heater")
        # print('heater', heater)

        if not request.form.get("heater"):
            return render_template("apology_log.html", message = "You must provide a heater")

        
        db.execute("INSERT INTO heater (value) VALUES (?)", (heater,))
        connection.commit()

        rows = db.execute("SELECT * FROM heater WHERE value = :heater", {"heater": request.form.get("heater")})
        # print("rows", rows)
        for row in rows:
            global heater_today_id
           
            heater_today_id = row[0]
            # print("heater_today_id", heater_today_id)
            heater_today_value = row[1]
            # print("heater_today_value", heater_today_value)
            heater_yesterday_id = heater_today_id - 1
            # print("heater_yesterday_id", heater_yesterday_id)

       
        # x = 0

        # if heater_yesterday_value not in globals():
        #     heater_yesterday_value = x
        #     print("!!!heater_yesterday_value0", heater_yesterday_value)
        #     return(heater_yesterday_value)

        if heater_today_id == 0:
            heater_yesterday_value = 0
            heater_today_value = 0
            count_heater_today_total = heater_yesterday_value 
        elif heater_today_id == 1:
            heater_yesterday_value = 0
            count_heater_today_total = heater_yesterday_value 
        elif heater_today_id >= 2:
            toos = db.execute("SELECT value FROM heater WHERE id = id", {"id": heater_yesterday_id})
            toos = db.fetchall()
            for too in toos:
                heater_yesterday_value = toos[-2][0]
                # print("toos", toos)
        
        
        count_heater_today_total = round((heater_today_value - heater_yesterday_value), 4)
        # print("heater_yesterday_value", heater_yesterday_value)
        # print("count_heater_today_total", count_heater_today_total)

        
        return redirect("/")


    if request.method == "GET":
        return render_template("heater.html", heater_yesterday_value=heater_yesterday_value)



if __name__ == '__main__':
	app.run(debug=True)