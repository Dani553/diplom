#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session, url_for
import importlib.util
from dotenv import load_dotenv
import requests
import os
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

application = Flask(__name__)

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")
admin_email= os.getenv("ADMIN_EMAIL")
recaptcha_secret = os.getenv("RECAPTCHA_SECRET_KEY")

application.config["SECRET_KEY"] = secret_key
# application.config["SERVER_NAME"] = 'www.net-equip-aggregator.ru'

db_host = 'localhost'
db_name = 'postgres'
db_user = 'postgres'

conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

cur.execute("""SELECT DISTINCT "Уровень" from "Характеристики коммутаторов" Where "Уровень"!=' '""")
row1 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Пропускная способность(Скорость)" from "Характеристики коммутаторов" 
Where "Пропускная способность(Скорость)"!=' '""")
row2 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Вид" from "Характеристики коммутаторов" Where "Вид"!=''""")
row3 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Размещение" from "Характеристики коммутаторов" Where "Размещение"!=' '""")
row4 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Процессор" from "Характеристики серверных платформ" Where "Процессор"!=''""")
row5 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Стандарты Wi-Fi" from "Характеристики точек доступа Wi-Fi" Where "Стандарты Wi-Fi"!=''""")
row6 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Размещение" from "Характеристики точек доступа Wi-Fi" Where "Размещение"!=''""")
row7 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Варианты крепления" from "Характеристики точек доступа Wi-Fi" Where "Варианты крепления"!=' '""")
row8 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Установка" from "Характеристики шкафов" Where "Установка"!=''""")
row9 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Защита" from "Характеристики шкафов" Where "Защита"!=' '""")
row10 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Тип шкафа" from "Характеристики шкафов" Where "Тип шкафа"!=''""")
row11 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Поддержка IPv6" from "Характеристики маршрутизаторов" Where "Поддержка IPv6"!=' '""")
row12 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Стандарты Wi-Fi" from "Характеристики Wi-Fi роутеров" Where "Стандарты Wi-Fi"!=''""")
row13 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Скорость передачи" from "Характеристики Wi-Fi роутеров" Where "Скорость передачи"!=' '""")
row14 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Поддержка IPv6" from "Характеристики Wi-Fi роутеров" Where "Поддержка IPv6"!=' '""")
row15 = cur.fetchall()

cur.close()
conn.close()

@application.route('/')
def home():
    list_found=[0, 0, 0, 0, 0, 0, 0]
    if 'username' in session:
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, 
                           row4=row4, row5=row5, row6=row6, row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, 
                           row12=row12, row13=row13, row14=row14, row15=row15)
    else:
        return redirect(url_for('login'))
@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

            username = request.form.get('username')
            password = request.form.get('password')
        #recaptcha_response = request.form.get('g-recaptcha-response')
        
        #recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        #data = {'secret': recaptcha_secret, 'response': recaptcha_response}
        #response = requests.post(recaptcha_url, data=data)
        #result = response.json()
        #print(result)
        #if result['success']:
            conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
            cur = conn.cursor()
            user_query="SELECT * FROM users WHERE username='"+username+"'"

            cur.execute(user_query)
            user = cur.fetchone()

            cur.close()
            conn.close()

            if user and check_password_hash(user[2], password):
                session['username'] = username
                if session['username']==admin_email:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Введен неверный логин или пароль')
        # else:
        #     error = 'Captcha не прошла проверку'
        #     return render_template('login.html', error=error)
    else:
        return render_template('login.html')
    
@application.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        users_query="SELECT * FROM users WHERE username='"+username+"'"
        cur.execute(users_query)
        user = cur.fetchone()

        if user:
            return render_template('register.html', error='Пользователь уже создан')
        elif (not username):
            return render_template('register.html', error='Не введен логин')
        elif (not password):
            return render_template('register.html', error='Не введен пароль')
        else:
            hashed_password = generate_password_hash(password)

            users_login_query="INSERT INTO users (username, password) VALUES ('"+username+"', '"+hashed_password+"')"
            cur.execute(users_login_query)
            conn.commit()
            cur.close()
            conn.close()

            session['username'] = username
            return redirect(url_for('home'))
    else:
        return render_template('register.html')

@application.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    if 'username' in session and session['username']==admin_email:
        if request.method == 'POST':
            if request.form['submit']=='Вывод таблицы':
                table_name = request.form['table_name']

                if (table_name=="Коммутаторы"):
                        table_name1="Характеристики коммутаторов"
                elif (table_name=="Маршрутизаторы"):
                        table_name1="Характеристики маршрутизаторов"
                elif (table_name=="Wi-Fi роутеры"):
                        table_name1="Характеристики Wi-Fi роутеров"
                elif (table_name=="Серверные платформы"):
                        table_name1="Характеристики серверных платформ"
                elif (table_name=="Точки доступа Wi-Fi"):
                        table_name1="Характеристики точек доступа Wi-Fi"
                elif (table_name=="Шкафы и стойки"):
                        table_name1="Характеристики шкафов"
                elif (table_name=="Сетевые хранилища"):
                        table_name1="Характеристики сетевых хранилищ"

                table_query="""SELECT * FROM "{}", "{}" WHERE "{}"."ID_характеристики"="{}"."ID_характеристики";""".format(table_name, table_name1, table_name, table_name1)
                cur.execute(table_query)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

                cur.close()
                conn.close()

                return render_template('admin_dashboard.html', table=table_name, rows=rows, columns=columns)
            
            if len(request.form['field0'])<6:
                field0 = request.form['field0']
            else:
                return render_template('admin_dashboard.html', error="Значение поля ID слишком велико!")
            if len(request.form['field01'])<6:
                field01 = request.form['field01']
            else:
                return render_template('admin_dashboard.html', error="Значение поля ID_характеристики слишком велико!")
            if len(request.form['field1'])<200:
                field1 = request.form['field1']
            else:
                return render_template('admin_dashboard.html', error="Значение поля 'Название' слишком велико!")
            if len(request.form['field2'])<50:
                field2 = request.form['field2']
            else:
                return render_template('admin_dashboard.html', error="Значение поля 'Цена' слишком велико!")
            if len(request.form['field3'])<200:
                field3 = request.form['field3']
            else:
                return render_template('admin_dashboard.html', error="Значение поля 'Ссылки' слишком велико!")
            field4 = request.form['field4']
            field5 = request.form['field5']
            field6 = request.form['field6']
            field7 = request.form['field7']
            field8 = request.form['field8']
            table_name1 = request.form.getlist('table_name1')
            
            if request.form['submit']=='Вставка данных':
                try:
                    if table_name1==['com']:
                        if field4!='' and field1!='' and field3!='':
                                cur.execute("""INSERT INTO "Характеристики коммутаторов" ("Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", 
                                "Вид", "Размещение") values ('{}', '{}', '{}', '{}', '{}')""".format(field4, field5, field6, field7, field8))
                                conn.commit()
                                cur.execute("""SELECT "ID_характеристики" FROM "Характеристики коммутаторов" ORDER BY "ID_характеристики" DESC LIMIT 1;""")
                                index=cur.fetchone()
                                cur.execute("""INSERT INTO "Коммутаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") values 
                                ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                                conn.commit()
                        else:
                                return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Первая характеристика'")
    
                    elif table_name1==['marsh']:
                        if field4!='' and field1!='' and field3!='':
                            cur.execute("""INSERT INTO "Характеристики маршрутизаторов" ("Порты WAN/LAN", "Поддержка IPv6") 
                            values ('{}', '{}')""".format(field4, field5))
                            conn.commit()
                            cur.execute("""SELECT "ID_характеристики" FROM "Характеристики маршрутизаторов" ORDER BY "ID_характеристики" DESC LIMIT 1;""")
                            index=cur.fetchone()
                            cur.execute("""INSERT INTO "Маршрутизаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") 
                            values ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Первая характеристика'")
                    elif table_name1==['router']:
                        if field5!='' and field1!='' and field3!='':
                            cur.execute("""INSERT INTO "Характеристики Wi-Fi роутеров" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Скорость передачи", 
                            "Поддержка IPv6") values ('{}', '{}', '{}', '{}')""").format(field4, field5, field6, field7)
                            conn.commit()
                            cur.execute("""SELECT "ID_характеристики" FROM "Характеристики Wi-Fi роутеров" ORDER BY "ID_характеристики" DESC LIMIT 1;""")
                            index=cur.fetchone()
                            cur.execute("""INSERT INTO "Wi-Fi роутеры" ("Название", "Ссылки", "Цена", "ID_характеристики") 
                            values ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Вторая характеристика'")
                    elif table_name1==['server']:
                        if field8!='' and field1!='' and field3!='':
                            cur.execute("""INSERT INTO "Характеристики серверных платформ" ("Порты WAN/LAN", "Порты USB", "Процессор", 
                            "Количество процессоров", "Дисковая корзина") values ('{}', /
                            '{}', '{}', '{}', '{}')""".format(field4, field5, field6, field7, field8))
                            conn.commit()
                            cur.execute("""SELECT "ID_характеристики" FROM "Характеристики серверных платформ" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                            index=cur.fetchone()
                            cur.execute("""INSERT INTO "Серверные платформы" ("Название", "Ссылки", "Цена", "ID_характеристики") 
                            values ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Пятую характеристика'")
                    elif table_name1==['shkaf']:
                        if field5!='' and field1!='' and field3!='':
                            cur.execute("""INSERT INTO "Характеристики шкафов" ("Установка", "Число секций", "Защита", "Высота", "Тип шкафа") 
                            values ('{}', '{}', '{}', '{}', '{}')""".format(field4, field5, field6, field7, field8))
                            conn.commit()
                            cur.execute("""SELECT "ID_характеристики" FROM "Характеристики шкафов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                            index=cur.fetchone()
                            cur.execute("""INSERT INTO "Шкафы и стойки" ("Название", "Ссылки", "Цена", "ID_характеристики") 
                            values ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Вторую характеристика'")
                    elif table_name1==['toch']:
                        if field5!='' and field1!='' and field3!='':
                            cur.execute("""INSERT INTO "Характеристики точек доступа Wi-Fi" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", 
                            "Варианты крепления") values ('{}', '{}', '{}', '{}')""".format(field4, field5, field6, field7))
                            conn.commit()
                            cur.execute("""SELECT "ID_характеристики" FROM "Характеристики точек доступа Wi-Fi" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                            index=cur.fetchone()
                            cur.execute("""INSERT INTO "Точки доступа Wi-Fi" ("Название", "Ссылки", "Цена", "ID_характеристики") 
                            values ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Вторую характеристика'")
                    elif table_name1==['chran']:
                        if field5!='' and field1!='' and field3!='':
                            cur.execute("""INSERT INTO "Характеристики сетевых хранилищ" ("Количество отсеков", "Максимально поддерживаемый объем", 
                            "Количество портов Ethernet") values ('{}', '{}', '{}')""".format(field4, field5, field6))
                            conn.commit()
                            cur.execute("""SELECT "ID_характеристики" FROM "Характеристики сетевых хранилищ" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                            index=cur.fetchone()
                            cur.execute("""INSERT INTO "Сетевые хранилища" ("Название", "Ссылки", "Цена", "ID_характеристики") 
                            values ('{}', '{}', '{}', '{}')""".format(field1, field3, field2, index[0]))
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'Название', 'Ссылка' и 'Вторую характеристика'")    
                    else:
                        redirect(url_for('login'))
                except (Exception):
                        return render_template('admin_dashboard.html', error="Введены неверные данные в поля!")
    
            elif request.form['submit']=='Изменение данных':
                query=[]
                try:
                    if table_name1==['com']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики коммутаторов" SET """
                            if field4!='':
                                query.append(""""Порты WAN/LAN"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Уровень"='{}'""".format(field5))
                            if field6!='':
                                query.append(""""Пропускная способность(Скорость)"='{}'""".format(field6))
                            if field7!='':
                                query.append(""""Вид"='{}'""".format(field7))
                            if field8!='':
                                query.append(""""Размещение"='{}'""".format(field8))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                            query=[]
                        elif field0!='':
                            update_query="""UPDATE "Коммутаторы" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field0)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")     
                    elif table_name1==['marsh']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики маршрутизаторов" SET """
                            if field4!='':
                                query.append(""""Порты WAN/LAN"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Поддержка IPv6"='{}'""".format(field5))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                        elif field0!='':
                            query=[]
                            update_query="""UPDATE "Маршрутизаторы" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field0)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")
                    elif table_name1==['router']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики Wi-Fi роутеров" SET """
                            if field4!='':
                                query.append(""""Порты WAN/LAN"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Стандарты Wi-Fi"='{}'""".format(field5))
                            if field6!='':
                                query.append(""""Скорость передачи"='{}'""".format(field6))
                            if field7!='':
                                query.append(""""Поддержка IPv6"='{}'""".format(field7))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                        elif field0!='':
                            query=[]
                            update_query="""UPDATE "Wi-Fi роутеры" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field0)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")
                    elif table_name1==['server']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики серверных платформ" SET """
                            if field4!='':
                                query.append(""""Порты WAN/LAN"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Порты USB"='{}'""".format(field5))
                            if field6!='':
                                query.append(""""Процессор"='{}'""".format(field6))
                            if field7!='':
                                query.append(""""Количество процессоров"='{}'""".format(field7))
                            if field8!='':
                                query.append(""""Дисковая корзина"='{}'""".format(field8))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                        elif field0!='':
                            query=[]
                            update_query="""UPDATE "Серверные платформы" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field0)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")
                    elif table_name1==['shkaf']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики шкафов" SET """
                            if field4!='':
                                query.append(""""Установка"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Число секций"='{}'""".format(field5))
                            if field6!='':
                                query.append(""""Защита"='{}'""".format(field6))
                            if field7!='':
                                query.append(""""Высота"='{}'""".format(field7))
                            if field8!='':
                                query.append(""""Тип шкафа"='{}'""".format(field8))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                        elif field0!='':
                            query=[]
                            update_query="""UPDATE "Шкафы и стойки" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field4)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")
                    elif table_name1==['toch']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики точек доступа Wi-Fi" SET """
                            if field4!='':
                                query.append(""""Порты WAN/LAN"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Стандарты Wi-Fi"='{}'""".format(field5))
                            if field6!='':
                                query.append(""""Размещение"='{}'""".format(field6))
                            if field7!='':
                                query.append(""""Варианты крепления"='{}'""".format(field7))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                        elif field0!='':
                            query=[]
                            update_query="""UPDATE "Точки доступа Wi-Fi" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field0)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")
                    elif table_name1==['chran']:
                        if field01!='':
                            update_query="""UPDATE "Характеристики сетевых хранилищ" SET """
                            if field4!='':
                                query.append(""""Количество отсеков"='{}'""".format(field4))
                            if field5!='':
                                query.append(""""Максимально поддерживаемый объем"='{}'""".format(field5))
                            if field6!='':
                                query.append(""""Количество портов Ethernet"='{}'""".format(field6))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID_характеристики"='{}'""".format(field01)
                            cur.execute(update_query) 
                            conn.commit()
                        elif field0!='':
                            query=[]
                            update_query="""UPDATE "Сетевые хранилища" SET """
                            if field1!='':
                                query.append(""""Название"='{}'""".format(field1))
                            if field2!='':
                                query.append(""""Цена"='{}'""".format(field2))
                            if field3!='':
                                query.append(""""Ссылки"='{}'""".format(field3))
                            if query!='':
                                update_query+= ', '.join(query)
                            update_query+=""" WHERE "ID"='{}'""".format(field0)
                            cur.execute(update_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поля: 'ID' и 'ID_характеристики'")
                    conn.commit()
                except (Exception):
                        return render_template('admin_dashboard.html', error="Введены неверные данные в поля!")

            elif request.form['submit']=='Удаление данных':
                field0 = request.form['field0']
                table_name1 = request.form.getlist('table_name1')
                try:
                    if table_name1==['com']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики коммутаторов" USING "Коммутаторы" 
                            WHERE "Коммутаторы"."ID_характеристики"="Характеристики коммутаторов"."ID_характеристики" 
                            AND "Коммутаторы"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Коммутаторы" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
     
                    elif table_name1==['marsh']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики маршрутизаторов" USING "Маршрутизаторы" 
                            WHERE "Маршрутизаторы"."ID_характеристики"="Характеристики маршрутизаторов"."ID_характеристики" 
                            AND "Маршрутизаторы"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Маршрутизаторы" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
    
                    elif table_name1==['router']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики Wi-Fi роутеров" USING "Wi-Fi роутеры" 
                            WHERE "Wi-Fi роутеры"."ID_характеристики"="Характеристики Wi-Fi роутеров"."ID_характеристики" 
                            AND "Wi-Fi роутеры"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Wi-Fi роутеры" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
    
                    elif table_name1==['server']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики серверных платформ" USING "Серверные платформы" 
                            WHERE "Серверные платформы"."ID_характеристики"="Характеристики серверных платформ"."ID_характеристики" 
                            AND "Серверные платформы"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Серверные платформы" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
                    
                    elif table_name1==['shkaf']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики шкафов" USING "Шкафы и стойки" 
                            WHERE "Шкафы и стойки"."ID_характеристики"="Характеристики шкафов"."ID_характеристики" 
                            AND "Шкафы и стойки"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Шкафы и стойки" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
    
                    elif table_name1==['toch']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики точек доступа Wi-Fi" USING "Точки доступа Wi-Fi" 
                            WHERE  "Точки доступа Wi-Fi"."ID_характеристики"="Характеристики точек доступа Wi-Fi"."ID_характеристики" 
                            AND "Точки доступа Wi-Fi"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Точки доступа Wi-Fi" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
    
                    elif table_name1==['chran']:
                        if field0!='':
                            delete_query1="""DELETE FROM "Характеристики сетевых хранилищ" USING "Сетевые хранилища" 
                            WHERE "Сетевые хранилища"."ID_характеристики"="Характеристики сетевых хранилищ"."ID_характеристики" 
                            AND "Сетевые хранилища"."ID"='{}'""".format(field0)
                            delete_query="""DELETE FROM "Сетевые хранилища" WHERE "ID"='{}'""".format(field0)
                            cur.execute(delete_query1)
                            cur.execute(delete_query)
                            conn.commit()
                        else:
                            return render_template('admin_dashboard.html', error="Введите значения в поле: 'ID'")
    
                    else:
                        redirect(url_for('login'))
                    conn.commit()
                except (Exception):
                    return render_template('admin_dashboard.html', error="Введены неверные данные в поля!")

            return redirect(url_for('admin_dashboard'))
            
        else:
            return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))
    
@application.route('/admin_dashboard/sniffer_dns', methods=['POST'])
def run_sniffer_dns():
    spec=importlib.util.spec_from_file_location('sniffer_dns', "./sniffer_dns.py")
    sniffer_dns=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_dns)
    return redirect(url_for('admin_dashboard'))

@application.route('/admin_dashboard/sniffer_citilink', methods=['POST'])
def run_sniffer_citilink():
    spec=importlib.util.spec_from_file_location('sniffer_citilink', "./sniffer_citilink.py")
    sniffer_citilink=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_citilink)
    return redirect(url_for('admin_dashboard'))

@application.route('/admin_dashboard/sniffer_lanmart', methods=['POST'])
def run_sniffer_lanmart():
    spec=importlib.util.spec_from_file_location('sniffer_lanmart', "./sniffer_lanmart.py")
    sniffer_lanmart=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_lanmart)
    return redirect(url_for('admin_dashboard'))

@application.route('/admin_dashboard/sniffer_qtech', methods=['POST'])
def run_sniffer_qtech():
    spec=importlib.util.spec_from_file_location('sniffer_qtech', "./sniffer_qtech.py")
    sniffer_qtech=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_qtech)
    return redirect(url_for('admin_dashboard'))

@application.route('/korzina', methods=['POST'])
def korzina():
    list_found=[0, 0, 0, 0, 0, 0, 0]
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    querty_search="SELECT * FROM korzina, users WHERE users.id_client=korzina.id_client AND users.username='"+session.get('username')+"' \
    ORDER BY korzina.id_korzina DESC LIMIT 1"
    cur.execute(querty_search)
    if cur.fetchone():
        count_query="SELECT count(*) FROM information_schema.columns WHERE table_name='stack_com'"
        cur.execute(count_query)
        count_result=cur.fetchone()[0]
        stack_com=[]
        inform_com=[]
        for i in range(int(count_result)-1):
            id_com_num_query="SELECT id_com{} FROM stack_com, korzina, users WHERE stack_com.id_stack_com=korzina.id_stack_com \
                AND korzina.id_client=users.id_client AND users.username='{}' \
                ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_com_num_query)
            id_com_num=cur.fetchone()
            if id_com_num:
                    id_com_num=id_com_num[0]
                    if id_com_num:
                        stack_com.append(id_com_num)
        for id in stack_com:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", 
            "Вид", "Размещение" FROM "Коммутаторы", "Характеристики коммутаторов" 
            WHERE "Характеристики коммутаторов"."ID_характеристики"="Коммутаторы"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_com.append(inform_attr)

        stack_marsh=[]
        inform_marsh=[]
        for i in range(int(count_result)-1):
            id_marsh_num_query="SELECT id_marsh{} FROM stack_marsh, korzina, users \
                WHERE stack_marsh.id_stack_marsh=korzina.id_stack_marsh AND korzina.id_client=users.id_client AND \
                users.username='{}' ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_marsh_num_query)
            id_marsh_num=cur.fetchone()
            print(id_marsh_num)
            if id_marsh_num:
                id_marsh_num=id_marsh_num[0]
                if id_marsh_num:
                    stack_marsh.append(id_marsh_num)
        for id in stack_marsh:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Поддержка IPv6" 
            FROM "Маршрутизаторы", "Характеристики маршрутизаторов" 
            WHERE "Характеристики маршрутизаторов"."ID_характеристики"="Маршрутизаторы"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_marsh.append(inform_attr)

        stack_router=[]
        inform_router=[]
        for i in range(int(count_result)-1):
            id_router_num_query="SELECT id_router{} FROM stack_router, korzina, users \
            WHERE stack_router.id_stack_router=korzina.id_stack_router AND korzina.id_client=users.id_client AND \
            users.username='{}' ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_router_num_query)
            id_router_num=cur.fetchone()
            if id_router_num:
                id_router_num=id_router_num[0]
                if id_router_num:
                    stack_router.append(id_router_num)
        for id in stack_router:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Стандарты Wi-Fi", "Скорость передачи", "Поддержка IPv6" 
            FROM "Wi-Fi роутеры", "Характеристики Wi-Fi роутеров" 
            WHERE "Характеристики Wi-Fi роутеров"."ID_характеристики"="Wi-Fi роутеры"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_router.append(inform_attr)

        stack_server=[]
        inform_server=[]
        for i in range(int(count_result)-1):
            id_server_num_query="SELECT id_server{} FROM stack_server, korzina, users \
            WHERE stack_server.id_stack_server=korzina.id_stack_server AND korzina.id_client=users.id_client AND \
            users.username='{}' ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_server_num_query)
            id_server_num=cur.fetchone()
            if id_server_num:
                id_server_num=id_server_num[0]
                if id_server_num:
                    stack_server.append(id_server_num)
        for id in stack_server:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Порты USB", "Количество процессоров", "Дисковая корзина", 
            "Процессор" FROM "Серверные платформы", "Характеристики серверных платформ" 
            WHERE "Характеристики серверных платформ"."ID_характеристики"="Серверные платформы"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_server.append(inform_attr)

        stack_shkaf=[]
        inform_shkaf=[]
        for i in range(int(count_result)-1):
            id_shkaf_num_query="SELECT id_shkaf{} FROM stack_shkaf, korzina, users \
            WHERE stack_shkaf.id_stack_shkaf=korzina.id_stack_shkaf AND korzina.id_client=users.id_client AND \
            users.username='{}' ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_shkaf_num_query)
            id_shkaf_num=cur.fetchone()
            if id_shkaf_num:
                id_shkaf_num=id_shkaf_num[0]
                if id_shkaf_num:
                    stack_shkaf.append(id_shkaf_num)
        for id in stack_shkaf:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Число секций", "Высота", "Установка", "Защита", "Тип шкафа" 
            FROM "Шкафы и стойки", "Характеристики шкафов" 
            WHERE "Характеристики шкафов"."ID_характеристики"="Шкафы и стойки"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_shkaf.append(inform_attr)

        stack_toch=[]
        inform_toch=[]
        for i in range(int(count_result)-1):
            id_toch_num_query="SELECT id_toch{} FROM stack_toch, korzina, users \
            WHERE stack_toch.id_stack_toch=korzina.id_stack_toch AND korzina.id_client=users.id_client AND \
            users.username='{}' ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_toch_num_query)
            id_toch_num=cur.fetchone()
            if id_toch_num:
                id_toch_num=id_toch_num[0]
                if id_toch_num:
                    stack_toch.append(id_toch_num)
        for id in stack_toch:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", "Варианты крепления" 
            FROM "Точки доступа Wi-Fi", "Характеристики точек доступа Wi-Fi" 
            WHERE "Характеристики точек доступа Wi-Fi"."ID_характеристики"="Точки доступа Wi-Fi"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_toch.append(inform_attr)

        stack_chran=[]
        inform_chran=[]
        for i in range(int(count_result)-1):
            id_chran_num_query="SELECT id_chran{} FROM stack_chran, korzina, users \
                WHERE stack_chran.id_stack_chran=korzina.id_stack_chran AND korzina.id_client=users.id_client AND \
                users.username='{}' ORDER BY korzina.id_korzina DESC LIMIT 1".format(i+1, session.get('username'))
            cur.execute(id_chran_num_query)
            id_chran_num=cur.fetchone()
            if id_chran_num:
                id_chran_num=id_chran_num[0]
                if id_chran_num:
                    stack_chran.append(id_chran_num)
        for id in stack_chran:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Количество отсеков", "Максимально поддерживаемый объем", 
            "Количество портов Ethernet" FROM "Сетевые хранилища", "Характеристики сетевых хранилищ" 
            WHERE "Характеристики сетевых хранилищ"."ID_характеристики"="Сетевые хранилища"."ID_характеристики" AND "ID"='{}'""".format(id)
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            if inform_attr:
                inform_chran.append(inform_attr)

        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, 
                           row14=row14, row15=row15, inform_com=inform_com, inform_marsh=inform_marsh, inform_router=inform_router,
                           inform_server=inform_server, inform_chran=inform_chran, inform_shkaf=inform_shkaf, inform_toch=inform_toch)
    else:
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15)

@application.route('/compare', methods=['POST', 'GET'])
def compare():

    list_found=[0, 0, 0, 0, 0, 0, 0]

    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    compare_com=[]
    selected_rows_com = request.form.getlist('selected_rows_com')
    if selected_rows_com:
        for row in selected_rows_com:
                product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", 
                "Вид", "Размещение" FROM "Коммутаторы", "Характеристики коммутаторов" 
                WHERE "Характеристики коммутаторов"."ID_характеристики"="Коммутаторы"."ID_характеристики" AND "ID"='{}'""".format(row)
                cur.execute(product_query)
                inform_hardware=cur.fetchone()
                compare_com.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_com=compare_com)

    compare_marsh=[]
    selected_rows_marsh = request.form.getlist('selected_rows_marsh')
    if selected_rows_marsh:
        for row in selected_rows_marsh:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Поддержка IPv6" 
            FROM "Маршрутизаторы", "Характеристики маршрутизаторов" 
            WHERE "Характеристики маршрутизаторов"."ID_характеристики"="Маршрутизаторы"."ID_характеристики" AND "ID"='{}'""".format(row)
            cur.execute(product_query)
            inform_hardware=cur.fetchone()
            compare_marsh.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_marsh=compare_marsh)
    
    compare_wifi_router=[]
    selected_rows_wifi_router = request.form.getlist('selected_rows_wifi_router')
    if selected_rows_wifi_router:
        for row in selected_rows_wifi_router:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Стандарты Wi-Fi", "Скорость передачи", "Поддержка IPv6" 
            FROM "Wi-Fi роутеры", "Характеристики Wi-Fi роутеров" 
            WHERE "Характеристики Wi-Fi роутеров"."ID_характеристики"="Wi-Fi роутеры"."ID_характеристики" AND "ID"='{}'""".format(row)
            cur.execute(product_query)
            inform_hardware=cur.fetchone()
            compare_wifi_router.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_wifi_router=compare_wifi_router)

    compare_server=[]
    selected_rows_server = request.form.getlist('selected_rows_server')
    if selected_rows_server:
        for row in selected_rows_server:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Порты USB", "Количество процессоров", "Дисковая корзина", 
            "Процессор" FROM "Серверные платформы", "Характеристики серверных платформ" 
            WHERE "Характеристики серверных платформ"."ID_характеристики"="Серверные платформы"."ID_характеристики" AND "ID"='{}'""".format(row)
            cur.execute(product_query)
            inform_hardware=cur.fetchone()
            compare_server.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_server=compare_server)
    
    compare_access_point=[]
    selected_rows_access_point = request.form.getlist('selected_rows_access_point')
    if selected_rows_access_point:
        for row in selected_rows_access_point:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", "Варианты крепления" 
            FROM "Точки доступа Wi-Fi", "Характеристики точек доступа Wi-Fi" 
            WHERE "Характеристики точек доступа Wi-Fi"."ID_характеристики"="Точки доступа Wi-Fi"."ID_характеристики" AND "ID"='{}'""".format(row)
            cur.execute(product_query)
            inform_hardware=cur.fetchone()
            compare_access_point.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_access_point=compare_access_point)
    
    compare_cabinet=[]
    selected_rows_cabinet = request.form.getlist('selected_rows_cabinet')
    if selected_rows_cabinet:
        for row in selected_rows_cabinet:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Число секций", "Высота", "Установка", "Защита", "Тип шкафа" 
            FROM "Шкафы и стойки", "Характеристики шкафов" 
            WHERE "Характеристики шкафов"."ID_характеристики"="Шкафы и стойки"."ID_характеристики" AND "ID"='{}'""".format(row)
            cur.execute(product_query)
            inform_hardware=cur.fetchone()
            compare_cabinet.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_cabinet=compare_cabinet)
    
    compare_network_storage=[]
    selected_rows_network_storage = request.form.getlist('selected_rows_network_storage')
    if selected_rows_network_storage:
        for row in selected_rows_network_storage:
            product_query="""SELECT "Название", "Ссылки", "Цена", "Количество отсеков", "Максимально поддерживаемый объем", 
            "Количество портов Ethernet" FROM "Сетевые хранилища", "Характеристики сетевых хранилищ" 
            WHERE "Характеристики сетевых хранилищ"."ID_характеристики"="Сетевые хранилища"."ID_характеристики" AND "ID"='{}'""".format(row)
            cur.execute(product_query)
            inform_hardware=cur.fetchone()
            compare_network_storage.append(inform_hardware)
        return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
            compare_network_storage=compare_network_storage)
            
    return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15)

@application.route('/submit', methods=['POST'])
def submit():

    list_found=[0, 0, 0, 0, 0, 0, 0]

    checkbox_switch_value = request.form.getlist('switch_flag')
    checkbox_marsh_value = request.form.getlist('marsh_flag')
    checkbox_wifi_router_value = request.form.getlist('wifi_router_flag')
    checkbox_server_value = request.form.getlist('server_flag')
    checkbox_access_point_value = request.form.getlist('access_point_flag')
    checkbox_cabinet_value = request.form.getlist('cabinet_flag')
    checkbox_network_storage_value = request.form.getlist('network_storage_flag')

    switch_results, router_results, wifi_router_results, server_results, access_point_results, cabinet_results, network_storage_results=' '*7
    not_com, not_marsh, not_wifi_router, not_server, not_access_point, not_cabinet, not_network_storage = 0, 0, 0, 0, 0, 0, 0

    row=[]
    row_att=[]

    query_korz=''
    query_att=''

    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    if checkbox_switch_value:

        switch_field1 = request.form['switch_field1']
        if switch_field1:
            if int(switch_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Порты WAN/LAN' раздела 'Коммутаторы'")
        switch_listbox1 = request.form.getlist('switch_listbox1')
        switch_listbox2 = request.form.getlist('switch_listbox2')
        switch_listbox3 = request.form.getlist('switch_listbox3')
        switch_listbox4 = request.form.getlist('switch_listbox4')

        switch_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Уровень", 
        "Пропускная способность(Скорость)", "Вид", "Размещение" FROM "Коммутаторы", "Характеристики коммутаторов" 
        WHERE "Характеристики коммутаторов"."ID_характеристики"="Коммутаторы"."ID_характеристики" AND """

        where_clause = []
        params=[]
        if switch_field1!='':
            where_clause.append(""""Порты WAN/LAN" >= '"""+switch_field1+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Порты WAN/LAN' в разделе 'Коммутаторы'")
        if switch_listbox1!=['']:
            where_clause.append(""""Уровень" = '"""+switch_listbox1[0]+"""'""")
        if switch_listbox2!=['']:
            where_clause.append(""""Пропускная способность(Скорость)" = '"""+switch_listbox2[0]+"""'""")
        if switch_listbox3!=['']:
            where_clause.append(""""Вид" = '"""+switch_listbox3[0]+"""'""")
        if switch_listbox4!=['']:
            where_clause.append(""""Размещение" = '"""+switch_listbox4[0]+"""'""")
        if where_clause:
            switch_query += ' AND '.join(where_clause)
        cur.execute(switch_query)
        switch_results = cur.fetchall()
        id_com_list=[results[0] for results in switch_results[:7]]
        num_elements=len(id_com_list)
        if num_elements!=0:
            stack="INSERT INTO stack_com({}) VALUES ({})".format(
                ", ".join("id_com{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_com_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_com FROM stack_com ORDER BY id_stack_com DESC LIMIT 1"
            cur.execute(id_stack)
            stack_com=cur.fetchone()
        else:
            id_com_list=0
            not_com=1
    else:
        id_com_list=0

    if checkbox_marsh_value:

        router_field1 = request.form['router_field1']
        if router_field1:
            if int(router_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Порты WAN/LAN' раздела 'Маршрутизаторы'")
        router_listbox = request.form.getlist('router_listbox')

        router_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Поддержка IPv6" FROM "Маршрутизаторы", 
        "Характеристики маршрутизаторов" WHERE "Характеристики маршрутизаторов"."ID_характеристики"="Маршрутизаторы"."ID_характеристики" AND """

        where_clause = []
        params=[]
        if router_field1!='':
            where_clause.append(""""Порты WAN/LAN" >= '"""+router_field1+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Порты WAN/LAN' в разделе 'Маршрутизаторы'")
        if router_listbox!=['']:
            where_clause.append(""""Поддержка IPv6" = '"""+router_listbox[0]+"""'""")
        if where_clause:
            router_query += ' AND '.join(where_clause)
        cur.execute(router_query)
        router_results = cur.fetchall()
        id_marsh_list=[results[0] for results in router_results[:7]]
        num_elements=len(id_marsh_list)
        if num_elements!=0:
            stack="INSERT INTO stack_marsh({}) VALUES ({})".format(
                ", ".join("id_marsh{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_marsh_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_marsh FROM stack_marsh ORDER BY id_stack_marsh DESC LIMIT 1"
            cur.execute(id_stack)
            stack_marsh=cur.fetchone()
        else:
           id_marsh_list=0
           not_marsh=1
    else:
        id_marsh_list=0

    if checkbox_wifi_router_value:

        wifi_router_field1 = request.form['wifi_router_field1']
        if wifi_router_field1:
            if int(wifi_router_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Порты WAN/LAN' раздела 'Wi-Fi роутеры'")
        wifi_router_listbox1 = request.form.getlist('wifi_router_listbox1')
        wifi_router_listbox2 = request.form.getlist('wifi_router_listbox2')
        wifi_router_listbox3 = request.form.getlist('wifi_router_listbox3')

        wifi_router_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Стандарты Wi-Fi", "Скорость передачи", 
        "Поддержка IPv6" FROM "Wi-Fi роутеры", "Характеристики Wi-Fi роутеров" 
        WHERE "Характеристики Wi-Fi роутеров"."ID_характеристики"="Wi-Fi роутеры"."ID_характеристики" AND """

        where_clause = []
        params=[]
        if wifi_router_field1!='':
            where_clause.append(""""Порты WAN/LAN" >= '"""+wifi_router_field1[0]+"""'""")
        if wifi_router_listbox1!=['']:
            where_clause.append(""""Стандарты Wi-Fi" = '"""+wifi_router_listbox1[0]+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Стандарты Wi-Fi' в разделе ' Wi-Fi роутеры'")
        if wifi_router_listbox2!=['']:
            where_clause.append(""""Скорость передачи" = '"""+wifi_router_listbox2[0]+"""'""")
        if wifi_router_listbox3!=['']:
            where_clause.append(""""Поддержка IPv6" = '"""+wifi_router_listbox3[0]+"""'""")
        if where_clause:
            wifi_router_query += ' AND '.join(where_clause)
        cur.execute(wifi_router_query)
        wifi_router_results = cur.fetchall()
        id_wifi_router_list=[results[0] for results in wifi_router_results[:7]]
        num_elements=len(id_wifi_router_list)
        if num_elements!=0:
            stack="INSERT INTO stack_router({}) VALUES ({})".format(
                ", ".join("id_router{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_wifi_router_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_router FROM stack_router ORDER BY id_stack_router DESC LIMIT 1"
            cur.execute(id_stack)
            stack_router=cur.fetchone()
        else:
            id_wifi_router_list=0
            not_wifi_router=1
    else:
        id_wifi_router_list=0

    if checkbox_server_value:

        server_field1 = request.form['server_field1']
        if server_field1:
            if int(server_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Порты WAN/LAN' раздела 'Серверные платформы'")
        server_field2 = request.form['server_field2']
        if server_field2:
            if int(server_field2)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Порты USB' раздела 'Серверные платформы'")
        server_field3 = request.form['server_field3']
        if server_field3:
            if int(server_field3)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Количество процессоров' раздела 'Серверные платформы'")
        server_field4 = request.form['server_field4']
        if server_field4:
            if int(server_field4)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Дисковая корзина' раздела 'Серверные платформы'")
        server_listbox1 = request.form.getlist('server_listbox1')

        server_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Порты USB", "Количество процессоров", 
        "Дисковая корзина", "Процессор" FROM "Серверные платформы", "Характеристики серверных платформ" 
        WHERE "Характеристики серверных платформ"."ID_характеристики"="Серверные платформы"."ID_характеристики" AND """

        where_clause = []
        params=[]
        if server_field1!='':
            where_clause.append(""""Порты WAN/LAN" >= '"""+server_field1+"""'""")
        if server_field2!='':
            where_clause.append(""""Порты USB" >= '"""+server_field2+"""'""")
        if server_field3!='':
            where_clause.append(""""Количество процессоров" >= '"""+server_field3+"""'""")
        if server_field4!='':
            where_clause.append(""""Дисковая корзина" >= '"""+server_field4+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Дисковая корзина' в разделе 'Серверные платформы'")
        if server_listbox1!=['']:
            where_clause.append(""""Процессор" = '"""+server_listbox1[0]+"""'""")
        if where_clause:
            server_query += ' AND '.join(where_clause)
        cur.execute(server_query)
        server_results = cur.fetchall()
        id_server_list=[results[0] for results in server_results[:7]]
        num_elements=len(id_server_list)
        if num_elements!=0:
            stack="INSERT INTO stack_server({}) VALUES ({})".format(
                ", ".join("id_server{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_server_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_server FROM stack_server ORDER BY id_stack_server DESC LIMIT 1"
            cur.execute(id_stack)
            stack_server=cur.fetchone()
        else:
            id_server_list=0
            not_server=1
    else:
        id_server_list=0

    if checkbox_access_point_value:

        access_point_field1 = request.form['access_point_field1']
        if access_point_field1:
            if int(access_point_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Порты WAN/LAN' раздела 'Точки доступа Wi-Fi'")
        access_point_listbox1 = request.form.getlist('access_point_listbox1')
        access_point_listbox2 = request.form.getlist('access_point_listbox2')
        access_point_listbox3 = request.form.getlist('access_point_listbox3')

        access_point_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", 
        "Варианты крепления" FROM "Точки доступа Wi-Fi", "Характеристики точек доступа Wi-Fi" 
        WHERE "Характеристики точек доступа Wi-Fi"."ID_характеристики"="Точки доступа Wi-Fi"."ID_характеристики" AND """
        params=[]
        where_clause = []
        if access_point_field1!='':
            where_clause.append(""""Порты WAN/LAN" >= '"""+access_point_field1+"""'""")
        if access_point_listbox1!=['']:
            params.extend(str(x) for x in access_point_listbox1)
            where_clause.append(""""Стандарты Wi-Fi" = '"""+access_point_listbox1[0]+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Стандарты Wi-Fi' в разделе 'Точки доступа Wi-Fi'")
        if access_point_listbox2!=['']:
            params.extend(str(x) for x in access_point_listbox2)
            where_clause.append(""""Размещение" = '"""+access_point_listbox2[0]+"""'""")
        if access_point_listbox3!=['']:
            params.extend(str(x) for x in access_point_listbox3)
            where_clause.append(""""Варианты крепления" = '"""+access_point_listbox3[0]+"""'""")
        if where_clause:
            access_point_query += ' AND '.join(where_clause)
        cur.execute(access_point_query, params)
        access_point_results = cur.fetchall()
        id_access_point_list=[results[0] for results in access_point_results[:7]]
        num_elements=len(id_access_point_list)
        if num_elements!=0:
            stack="INSERT INTO stack_toch({}) VALUES ({})".format(
                ", ".join("id_toch{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_access_point_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_toch FROM stack_toch ORDER BY id_stack_toch DESC LIMIT 1"
            cur.execute(id_stack)
            stack_toch=cur.fetchone()
        else:
            id_access_point_list=0
            not_access_point=1
    else:
        id_access_point_list=0

    if checkbox_cabinet_value:

        cabinet_field1 = request.form['cabinet_field1']
        if cabinet_field1:
            if int(cabinet_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Число секций' раздела 'Шкафы и стойки'")
        cabinet_field2 = request.form['cabinet_field2']
        if cabinet_field2:
            if int(cabinet_field2)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Высота' раздела 'Шкафы и стойки'")
        cabinet_listbox1 = request.form.getlist('cabinet_listbox1')
        cabinet_listbox2 = request.form.getlist('cabinet_listbox2')
        cabinet_listbox3 = request.form.getlist('cabinet_listbox3')

        cabinet_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Число секций", "Высота", "Установка", "Защита", 
        "Тип шкафа" FROM "Шкафы и стойки", "Характеристики шкафов" 
        WHERE "Характеристики шкафов"."ID_характеристики"="Шкафы и стойки"."ID_характеристики" AND """
        params=[]
        where_clause = []
        if cabinet_field1!='':
            where_clause.append(""""Число секций" >= '"""+cabinet_field1+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Число секций' в разделе 'Шкафы и стойки'")
        if cabinet_field2!='':
            where_clause.append(""""Высота" <= '"""+cabinet_field2+"""'""")
        if cabinet_listbox1!=['']:
            where_clause.append(""""Установка" = '"""+cabinet_listbox1[0]+"""'""")
        if cabinet_listbox2!=['']:
            where_clause.append(""""Защита" = '"""+cabinet_listbox2[0]+"""'""")
        if cabinet_listbox3!=['']:
            where_clause.append(""""Тип шкафа" = '"""+cabinet_listbox3[0]+"""'""")
        if where_clause:
            cabinet_query += ' AND '.join(where_clause)
        cur.execute(cabinet_query)
        cabinet_results = cur.fetchall()
        id_cabinet_list=[results[0] for results in cabinet_results[:7]]
        num_elements=len(id_cabinet_list)
        if num_elements!=0:
            stack="INSERT INTO stack_shkaf({}) VALUES ({})".format(
                ", ".join("id_shkaf{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_cabinet_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_shkaf FROM stack_shkaf ORDER BY id_stack_shkaf DESC LIMIT 1"
            cur.execute(id_stack)
            stack_shkaf=cur.fetchone()
        else:
            id_cabinet_list=0
            not_cabinet=1
    else:
        id_cabinet_list=0

    if checkbox_network_storage_value:

        network_storage_field1 = request.form['network_storage_field1']
        if network_storage_field1:
            if int(network_storage_field1)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Количество отсеков' раздела 'Сетевые хранилища'")
        network_storage_field2 = request.form['network_storage_field2']
        if network_storage_field2:
            if int(network_storage_field2)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Максимально поддерживаемый объем одного накопителя' раздела 'Сетевые хранилища'")
        network_storage_field3 = request.form['network_storage_field3']
        if network_storage_field3:
            if int(network_storage_field3)>1000000:
                return render_template('home.html', list_found=list_found, row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                            row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                            error="Введено слишком большое число в поле 'Количество портов Ethernet' раздела 'Сетевые хранилища'")

        network_storage_query = """SELECT "ID", "Название", "Ссылки", "Цена", "Количество отсеков", "Максимально поддерживаемый объем", 
        "Количество портов Ethernet" FROM "Сетевые хранилища", "Характеристики сетевых хранилищ" 
        WHERE "Характеристики сетевых хранилищ"."ID_характеристики"="Сетевые хранилища"."ID_характеристики" AND """

        where_clause = []
        if network_storage_field1!='':
            where_clause.append(""""Количество отсеков" >= '"""+network_storage_field1+"""'""")
        if network_storage_field2!='':
            where_clause.append(""""Максимально поддерживаемый объем" >= '"""+network_storage_field2+"""'""")
        else:
            return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15, 
                           error="Введите обязательное поле 'Максимально поддерживаемый объем' в разделе 'Сетевые хранилища'")
        if network_storage_field3!='':
            where_clause.append(""""Количество портов Ethernet" >= '"""+network_storage_field3+"""'""")
        if where_clause:
            network_storage_query += ' AND '.join(where_clause)
        cur.execute(network_storage_query)
        network_storage_results = cur.fetchall()
        id_network_storage_list=[results[0] for results in network_storage_results[:7]]
        num_elements=len(id_network_storage_list)
        if num_elements!=0:
            stack="INSERT INTO stack_chran({}) VALUES ({})".format(
                ", ".join("id_chran{}".format(i+1) for i in range(num_elements)),
                ", ".join("'{}'".format(id_network_storage_list[i]) for i in range(num_elements))
            )
            cur.execute(stack)
            conn.commit()
            id_stack="SELECT id_stack_chran FROM stack_chran ORDER BY id_stack_chran DESC LIMIT 1"
            cur.execute(id_stack)
            stack_chran=cur.fetchone()
        else:
          id_network_storage_list=0
          not_network_storage=1
    else:
        id_network_storage_list=0

    list_found=[not_com, not_marsh, not_wifi_router, not_server, not_access_point, not_cabinet, not_network_storage]

    name_query="SELECT id_client FROM users WHERE username='"+session.get('username')+"'"
    cur.execute(name_query)
    username=cur.fetchone()

    if id_wifi_router_list!=0:
        row.append("id_stack_router")
        row_att.append(str(stack_router[0]))
    if id_marsh_list!=0:
        row.append("id_stack_marsh")
        row_att.append(str(stack_marsh[0]))
    if id_access_point_list!=0:
        row.append("id_stack_toch")
        row_att.append(str(stack_toch[0]))
    if id_com_list!=0:
        print(id_com_list)
        row.append("id_stack_com")
        print(stack_com)
        row_att.append(str(stack_com[0]))
    if id_server_list!=0:
        row.append("id_stack_server")
        row_att.append(str(stack_server[0]))
    if id_cabinet_list!=0:
        row.append("id_stack_shkaf")
        row_att.append(str(stack_shkaf[0]))
    if id_network_storage_list!=0:
        row.append("id_stack_chran")
        row_att.append(str(stack_chran[0]))
    if row:
        query_korz+=', '.join(row)
    if row_att:
        query_att+=', '.join(row_att)

    if (id_wifi_router_list!=0 or id_marsh_list!=0 or id_access_point_list!=0 or id_com_list!=0 or id_server_list!=0
        or id_cabinet_list!=0 or id_network_storage_list!=0):
        korzina="INSERT INTO korzina( {}, id_client ) VALUES ({}, {})".format(query_korz, query_att, username[0])
        print(korzina)
        cur.execute(korzina)
        conn.commit()
        cur.close()
        conn.close()

    return render_template('home.html', switch_results=switch_results, router_results=router_results, 
                           wifi_router_results=wifi_router_results, server_results=server_results, 
                           access_point_results=access_point_results, cabinet_results=cabinet_results, 
                           network_storage_results=network_storage_results, list_found=list_found, row1=row1, row2=row2, row3=row3, 
                           row4=row4, row5=row5, row6=row6, row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, 
                           row12=row12, row13=row13, row14=row14, row15=row15)
if __name__=="__main__":
    application.run(debug=True, host='0.0.0.0', port=5050)