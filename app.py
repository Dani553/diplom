from flask import Flask, render_template, request, redirect, session, url_for
import importlib.util
from dotenv import load_dotenv
import os

import psycopg2

app = Flask(__name__)

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")
admin_email= os.getenv("ADMIN_EMAIL")

app.config["SECRET_KEY"] = secret_key

db_host = 'localhost'
db_name = 'postgres'
db_user = 'postgres'

conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

cur.execute("""SELECT DISTINCT "Уровень" from "Характеристики коммутаторов" Where "Уровень"!=''""")
row1 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Пропускная способность(Скорость)" from "Характеристики коммутаторов" Where "Пропускная способность(Скорость)"!=''""")
row2 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Вид" from "Характеристики коммутаторов" Where "Вид"!=''""")
row3 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Размещение" from "Характеристики коммутаторов" Where "Размещение"!=''""")
row4 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Процессор" from "Характеристики серверных платформ" Where "Процессор"!=''""")
row5 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Стандарты Wi-Fi" from "Характеристики точек доступа Wi-Fi" Where "Стандарты Wi-Fi"!=''""")
row6 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Размещение" from "Характеристики точек доступа Wi-Fi" Where "Размещение"!=''""")
row7 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Варианты крепления" from "Характеристики точек доступа Wi-Fi" Where "Варианты крепления"!=''""")
row8 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Установка" from "Характеристики шкафов" Where "Установка"!=''""")
row9 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Защита" from "Характеристики шкафов" Where "Защита"!=''""")
row10 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Тип шкафа" from "Характеристики шкафов" Where "Тип шкафа"!=''""")
row11 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Поддержка IPv6" from "Характеристики маршрутизаторов" Where "Поддержка IPv6"!=''""")
row12 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Стандарты Wi-Fi" from "Характеристики Wi-Fi роутеров" Where "Стандарты Wi-Fi"!=''""")
row13 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Скорость передачи" from "Характеристики Wi-Fi роутеров" Where "Скорость передачи"!=' '""")
row14 = cur.fetchall()
cur.execute("""SELECT DISTINCT "Поддержка IPv6" from "Характеристики Wi-Fi роутеров" Where "Поддержка IPv6"!=' '""")
row15 = cur.fetchall()

cur.close()
conn.close()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15)
    else:
        return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            session['username'] = username
            if session['username']==admin_email:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Введен неверный логин или пароль')
    else:
        return render_template('login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    if 'username' in session and session['username']==admin_email:
        if request.method == 'POST':
            print(request.form.get('submit'))
            if request.form['submit']=='Вывод таблицы':
                table_name = request.form['table_name']

                match table_name:
                    case("Коммутаторы"):
                        table_name1="Характеристики коммутаторов"
                    case("Маршрутизаторы"):
                        table_name1="Характеристики маршрутизаторов"
                    case("Wi-Fi роутеры"):
                        table_name1="Характеристики Wi-Fi роутеров"
                    case("Серверные платформы"):
                        table_name1="Характеристики серверных платформ"
                    case("Точки доступа Wi-Fi"):
                        table_name1="Характеристики точек доступа Wi-Fi"
                    case("Шкафы и стойки"):
                        table_name1="Характеристики шкафов"
                    case("Сетевые хранилища"):
                        table_name1="Характеристики сетевых хранилищ"

                cur.execute(f"""SELECT * FROM "{table_name}", "{table_name1}" WHERE "{table_name}"."ID_характеристики"="{table_name1}"."ID_характеристики" """)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

                cur.close()
                conn.close()

                return render_template('admin_dashboard.html', table=table_name, rows=rows, columns=columns)
            
            elif request.form['submit']=='Вставка данных':
                field1 = request.form['field1']
                field2 = request.form['field2']
                field3 = request.form['field3']
                field4 = request.form['field4']
                field5 = request.form['field5']
                field6 = request.form['field6']
                field7 = request.form['field7']
                field8 = request.form['field8']
                table_name1 = request.form.getlist('table_name1')

                if table_name1==['com']:
                    cur.execute(f"""INSERT INTO "Характеристики коммутаторов" ("Порты WAN/LAN", "Уровень", "Пропускная способность(Скорость)", "Вид", "Размещение") values ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики коммутаторов" ORDER BY "ID_характеристики" DESC LIMIT 1;""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Коммутаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                elif table_name1==['marsh']:
                    cur.execute(f"""INSERT INTO "Характеристики маршрутизаторов" ("Порты WAN/LAN", "Поддержка IPv6") values ('{field4}', '{field5}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики маршрутизаторов" ORDER BY "ID_характеристики" DESC LIMIT 1;""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Маршрутизаторы" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                elif table_name1==['router']:
                    cur.execute(f"""INSERT INTO "Характеристики Wi-Fi роутеров" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Скорость передачи", "Поддержка IPv6") values ('{field4}', '{field5}', '{field6}', '{field7}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики Wi-Fi роутеров" ORDER BY "ID_характеристики" DESC LIMIT 1;""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Wi-Fi роутеры" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                elif table_name1==['server']:
                    cur.execute(f"""INSERT INTO "Характеристики серверных платформ" ("Порты WAN/LAN", "Порты USB", "Процессор", "Количество процессоров", "Дисковая корзина") values ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики серверных платформ" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Серверные платформы" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                elif table_name1==['shkaf']:
                    cur.execute(f"""INSERT INTO "Характеристики шкафов" ("Установка", "Число секций", "Защита", "Высота", "Тип шкафа") values ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики шкафов" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Шкафы и стойки" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                elif table_name1==['toch']:
                    cur.execute(f"""INSERT INTO "Характеристики точек доступа Wi-Fi" ("Порты WAN/LAN", "Стандарты Wi-Fi", "Размещение", "Варианты крепления") values ('{field4}', '{field5}', '{field6}', '{field7}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики точек доступа Wi-Fi" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Точки доступа Wi-Fi" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                elif table_name1==['chran']:
                    cur.execute(f"""INSERT INTO "Характеристики сетевых хранилищ" ("Количество отсеков", "Максимально поддерживаемый объем", "Количество портов Ethernet") values ('{field4}', '{field5}', '{field6}')""")
                    conn.commit()
                    cur.execute("""SELECT "ID_характеристики" FROM "Характеристики сетевых хранилищ" ORDER BY "ID_характеристики" DESC LIMIT 1""")
                    index=cur.fetchone()
                    cur.execute(f"""INSERT INTO "Сетевые хранилища" ("Название", "Ссылки", "Цена", "ID_характеристики") values ('{field1}', '{field2}', '{field3}', '{index[0]}')""")
                    conn.commit()
                else:
                    redirect(url_for('login'))

            elif request.form['submit']=='Изменение данных':
                field0 = request.form['field0']
                field01 = request.form['field01']
                field1 = request.form['field1']
                field2 = request.form['field2']
                field3 = request.form['field3']
                field4 = request.form['field4']
                field5 = request.form['field5']
                field6 = request.form['field6']
                field7 = request.form['field7']
                field8 = request.form['field8']
                table_name1 = request.form.getlist('table_name1')

                query=[]

                if table_name1==['com']:
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики коммутаторов" SET """
                        if field4!='':
                            query.append(f""""Порты WAN/LAN"='{field4}'""")
                        if field5!='':
                            query.append(f""""Уровень"='{field5}'""")
                        if field6!='':
                            query.append(f""""Пропускная способность(Скорость)"='{field6}'""")
                        if field7!='':
                            query.append(f""""Вид"='{field7}'""")
                        if field8!='':
                            query.append(f""""Размещение"='{field8}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Коммутаторы" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['marsh']:
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики маршрутизаторов" SET """
                        if field4!='':
                            query.append(f""""Порты WAN/LAN"='{field4}'""")
                        if field5!='':
                            query.append(f""""Поддержка IPv6"='{field5}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Маршрутизаторы" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['router']:
                    print('Hello')
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики Wi-Fi роутеров" SET """
                        if field4!='':
                            query.append(f""""Порты WAN/LAN"='{field4}'""")
                        if field5!='':
                            query.append(f""""Стандарты Wi-Fi"='{field5}'""")
                        if field6!='':
                            query.append(f""""Скорость передачи"='{field6}'""")
                        if field7!='':
                            query.append(f""""Поддержка IPv6"='{field7}'""")
                        if field8!='':
                            query.append(f"charact5='{field8}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Wi-Fi роутеры" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['server']:
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики серверных платформ" SET """
                        if field4!='':
                            query.append(f""""Порты WAN/LAN"='{field4}'""")
                        if field5!='':
                            query.append(f""""Порты USB"='{field5}'""")
                        if field6!='':
                            query.append(f""""Процессор"='{field6}'""")
                        if field7!='':
                            query.append(f""""Количество процессоров"='{field7}'""")
                        if field8!='':
                            query.append(f""""Дисковая корзина"='{field8}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Серверные платформы" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['shkaf']:
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики шкафов" SET """
                        if field4!='':
                            query.append(f""""Установка"='{field4}'""")
                        if field5!='':
                            query.append(f""""Число секций"='{field5}'""")
                        if field6!='':
                            query.append(f""""Защита"='{field6}'""")
                        if field7!='':
                            query.append(f""""Высота"='{field7}'""")
                        if field8!='':
                            query.append(f""""Тип шкафа"='{field8}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Шкафы и стойки" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['toch']:
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики точек доступа Wi-Fi" SET """
                        if field4!='':
                            query.append(f""""Порты WAN/LAN"='{field4}'""")
                        if field5!='':
                            query.append(f""""Стандарты Wi-Fi"='{field5}'""")
                        if field6!='':
                            query.append(f""""Размещение"='{field6}'""")
                        if field7!='':
                            query.append(f""""Варианты крепления"='{field7}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Точки доступа Wi-Fi" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['chran']:
                    if field01!='':
                        update_query=f"""UPDATE "Характеристики сетевых хранилищ" SET """
                        if field4!='':
                            query.append(f""""Количество отсеков"='{field4}'""")
                        if field5!='':
                            query.append(f""""Максимально поддерживаемый объем"='{field5}'""")
                        if field6!='':
                            query.append(f""""Количество портов Ethernet"='{field6}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID_характеристики"='{field01}'"""
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"""UPDATE "Сетевые хранилища" SET """
                        if field1!='':
                            query.append(f""""Название"='{field1}'""")
                        if field2!='':
                            query.append(f""""Цена"='{field2}'""")
                        if field3!='':
                            query.append(f""""Ссылки"='{field3}'""")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f""" WHERE "ID"='{field0}'"""
                        cur.execute(update_query)
                        conn.commit()
                else:
                    redirect(url_for('login'))
                conn.commit()

            elif request.form['submit']=='Удаление данных':
                field0 = request.form['field0']
                table_name1 = request.form.getlist('table_name1')

                if table_name1==['com']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики коммутаторов" USING "Коммутаторы" 
                        WHERE "Коммутаторы"."ID_характеристики"="Характеристики коммутаторов"."ID_характеристики" 
                        AND "Коммутаторы"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Коммутаторы" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()
                
                elif table_name1==['marsh']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики маршрутизаторов" USING "Маршрутизаторы" 
                        WHERE "Маршрутизаторы"."ID_характеристики"="Характеристики маршрутизаторов"."ID_характеристики" 
                        AND "Маршрутизаторы"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Маршрутизаторы" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['router']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики Wi-Fi роутеров" USING "Wi-Fi роутеры" 
                        WHERE "Wi-Fi роутеры"."ID_характеристики"="Характеристики Wi-Fi роутеров"."ID_характеристики" 
                        AND "Wi-Fi роутеры"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Wi-Fi роутеры" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['server']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики серверных платформ" USING "Серверные платформы" 
                        WHERE "Серверные платформы"."ID_характеристики"="Характеристики серверных платформ"."ID_характеристики" 
                        AND "Серверные платформы"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Серверные платформы" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()
                
                elif table_name1==['shkaf']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики шкафов" USING "Шкафы и стойки" 
                        WHERE "Шкафы и стойки"."ID_характеристики"="Характеристики шкафов"."ID_характеристики" 
                        AND "Шкафы и стойки"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Шкафы и стойки" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['toch']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики точек доступа Wi-Fi" USING "Точки доступа Wi-Fi" 
                        WHERE  "Точки доступа Wi-Fi"."ID_характеристики"="Характеристики точек доступа Wi-Fi"."ID_характеристики" 
                        AND "Точки доступа Wi-Fi"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Точки доступа Wi-Fi" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['chran']:
                    if field0!='':
                        delete_query1=f"""DELETE FROM "Характеристики сетевых хранилищ" USING "Сетевые хранилища" 
                        WHERE "Сетевые хранилища"."ID_характеристики"="Характеристики сетевых хранилищ"."ID_характеристики" 
                        AND "Сетевые хранилища"."ID"='{field0}'"""
                        delete_query=f"""DELETE FROM "Сетевые хранилища" WHERE "ID"='{field0}'"""
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                else:
                    redirect(url_for('login'))
                conn.commit()

            return redirect(url_for('admin_dashboard'))
            
        else:
            return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))
            
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM users WHERE username='{username}'")
        user = cur.fetchone()

        if user:
            return render_template('register.html', error='Пользователь уже создан')
        elif (not username):
            return render_template('register.html', error='Не введен логин')
        elif (not password):
            return render_template('register.html', error='Не введен пароль')
        else:
            cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
            conn.commit()
            cur.close()
            conn.close()

            session['username'] = username
            return redirect(url_for('home'))
    else:
        return render_template('register.html')
    
@app.route('/sniffer_dns', methods=['POST'])
def run_sniffer_dns():
    spec=importlib.util.spec_from_file_location('sniffer_dns', "./sniffer_dns.py")
    sniffer_dns=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_dns)
    return redirect(url_for('admin_dashboard'))

@app.route('/sniffer_citilink', methods=['POST'])
def run_sniffer_citilink():
    spec=importlib.util.spec_from_file_location('sniffer_citilink', "./sniffer_citilink.py")
    sniffer_citilink=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_citilink)
    return redirect(url_for('admin_dashboard'))

@app.route('/sniffer_lanmart', methods=['POST'])
def run_sniffer_lanmart():
    spec=importlib.util.spec_from_file_location('sniffer_lanmart', "./sniffer_lanmart.py")
    sniffer_lanmart=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_lanmart)
    return redirect(url_for('admin_dashboard'))

@app.route('/sniffer_qtech', methods=['POST'])
def run_sniffer_qtech():
    spec=importlib.util.spec_from_file_location('sniffer_qtech', "./sniffer_qtech.py")
    sniffer_qtech=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sniffer_qtech)
    return redirect(url_for('admin_dashboard'))

@app.route('/korzina', methods=['POST'])
def korzina():
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    querty_search=f"SELECT * FROM korzina, users WHERE users.id_client=korzina.id_client AND users.username='{session.get('username')}'"
    cur.execute(querty_search)
    if cur.fetchone():
        stack_com=[]
        inform_com=[]
        count_query="SELECT count(*) FROM information_schema.columns WHERE table_name='stack_com'"
        cur.execute(count_query)
        count_result=cur.fetchone()[0]
        for i in range(int(count_result)-1):
            id_com_num_query=f"SELECT id_com{i+1} FROM stack_com, korzina, users WHERE stack_com.id_stack_com=korzina.id_stack_com AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_com_num_query)
            id_com_num=cur.fetchone()[0]
            if id_com_num:
                stack_com.append(id_com_num)
        for id in stack_com:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Коммутаторы" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_com.append(inform_attr)

        stack_marsh=[]
        inform_marsh=[]
        for i in range(int(count_result)-1):
            id_marsh_num_query=f"SELECT id_marsh{i+1} FROM stack_marsh, korzina, users WHERE stack_marsh.id_stack_marsh=korzina.id_stack_marsh AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_marsh_num_query)
            id_marsh_num=cur.fetchone()[0]
            if id_marsh_num:
                stack_marsh.append(id_marsh_num)
        for id in stack_marsh:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Маршрутизаторы" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_marsh.append(inform_attr)

        stack_router=[]
        inform_router=[]
        for i in range(int(count_result)-1):
            id_router_num_query=f"SELECT id_router{i+1} FROM stack_router, korzina, users WHERE stack_router.id_stack_router=korzina.id_stack_router AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_router_num_query)
            id_router_num=cur.fetchone()[0]
            if id_router_num:
                stack_router.append(id_router_num)
        for id in stack_router:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Wi-Fi роутеры" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_router.append(inform_attr)

        stack_server=[]
        inform_server=[]
        for i in range(int(count_result)-1):
            id_server_num_query=f"SELECT id_server{i+1} FROM stack_server, korzina, users WHERE stack_server.id_stack_server=korzina.id_stack_server AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_server_num_query)
            id_server_num=cur.fetchone()[0]
            if id_server_num:
                stack_server.append(id_server_num)
        for id in stack_server:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Серверные платформы" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_server.append(inform_attr)

        stack_shkaf=[]
        inform_shkaf=[]
        for i in range(int(count_result)-1):
            id_shkaf_num_query=f"SELECT id_shkaf{i+1} FROM stack_shkaf, korzina, users WHERE stack_shkaf.id_stack_shkaf=korzina.id_stack_shkaf AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_shkaf_num_query)
            id_shkaf_num=cur.fetchone()[0]
            if id_shkaf_num:
                stack_shkaf.append(id_shkaf_num)
        for id in stack_shkaf:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Шкафы и стойки" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_shkaf.append(inform_attr)

        stack_toch=[]
        inform_toch=[]
        for i in range(int(count_result)-1):
            id_toch_num_query=f"SELECT id_toch{i+1} FROM stack_toch, korzina, users WHERE stack_toch.id_stack_toch=korzina.id_stack_toch AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_toch_num_query)
            id_toch_num=cur.fetchone()[0]
            if id_toch_num:
                stack_toch.append(id_toch_num)
        for id in stack_toch:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Точки доступа Wi-Fi" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_toch.append(inform_attr)

        stack_chran=[]
        inform_chran=[]
        for i in range(int(count_result)-1):
            id_chran_num_query=f"SELECT id_chran{i+1} FROM stack_chran, korzina, users WHERE stack_chran.id_stack_chran=korzina.id_stack_chran AND korzina.id_client=users.id_client AND users.username='{session.get('username')}' ORDER BY korzina.id_korzina DESC LIMIT 1"
            cur.execute(id_chran_num_query)
            id_chran_num=cur.fetchone()[0]
            if id_chran_num:
                stack_chran.append(id_chran_num)
        for id in stack_chran:
            product_query=f"""SELECT "Название", "Ссылки", "Цена" FROM "Сетевые хранилища" WHERE "ID"='{id}'"""
            cur.execute(product_query)
            inform_attr=cur.fetchone()
            inform_chran.append(inform_attr)

        return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, 
                           row14=row14, row15=row15, inform_com=inform_com, inform_marsh=inform_marsh, inform_router=inform_router,
                           inform_server=inform_server, inform_chran=inform_chran, inform_shkaf=inform_shkaf, inform_toch=inform_toch)
    else:
        return render_template('home.html', row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6, 
                           row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, row12=row12, row13=row13, row14=row14, row15=row15)

@app.route('/submit', methods=['POST'])
def submit():

    switch_field1 = request.form['switch_field1']
    switch_listbox1 = request.form.getlist('switch_listbox1')
    switch_listbox2 = request.form.getlist('switch_listbox2')
    switch_listbox3 = request.form.getlist('switch_listbox3')
    switch_listbox4 = request.form.getlist('switch_listbox4')

    router_field1 = request.form['router_field1']
    router_listbox = request.form.getlist('router_listbox')

    wifi_router_field1 = request.form['wifi_router_field1']
    wifi_router_listbox1 = request.form.getlist('wifi_router_listbox1')
    wifi_router_listbox2 = request.form.getlist('wifi_router_listbox2')
    wifi_router_listbox3 = request.form.getlist('wifi_router_listbox3')

    server_field1 = request.form['server_field1']
    server_field2 = request.form['server_field2']
    server_field3 = request.form['server_field3']
    server_field4 = request.form['server_field4']
    server_listbox1 = request.form.getlist('server_listbox1')

    access_point_field1 = request.form['access_point_field1']
    access_point_listbox1 = request.form.getlist('access_point_listbox1')
    access_point_listbox2 = request.form.getlist('access_point_listbox2')
    access_point_listbox3 = request.form.getlist('access_point_listbox3')

    cabinet_field1 = request.form['cabinet_field1']
    cabinet_field2 = request.form['cabinet_field2']
    cabinet_listbox1 = request.form.getlist('cabinet_listbox1')
    cabinet_listbox2 = request.form.getlist('cabinet_listbox2')
    cabinet_listbox3 = request.form.getlist('cabinet_listbox3')

    network_storage_field1 = request.form['network_storage_field1']
    network_storage_field2 = request.form['network_storage_field2']
    network_storage_field3 = request.form['network_storage_field3']

    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()

    switch_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Коммутаторы", "Характеристики коммутаторов" WHERE "Характеристики коммутаторов"."ID_характеристики"="Коммутаторы"."ID_характеристики" AND """

    where_clause = []
    params=[]
    if switch_field1!='':
        where_clause.append(f""""Порты WAN/LAN" >= '{switch_field1}'""")
    if switch_listbox1!=['']:
        params.extend(str(x) for x in switch_listbox1)
        where_clause.append(f""""Уровень" IN ({','.join(['%s']*len(switch_listbox1))})""")
    if switch_listbox2!=['']:
        params.extend(str(x) for x in switch_listbox2)
        where_clause.append(f""""Пропускная способность(Скорость)" IN ({','.join(['%s']*len(switch_listbox2))})""")
    if switch_listbox3!=['']:
        params.extend(str(x) for x in switch_listbox3)
        where_clause.append(f""""Вид" IN ({','.join(['%s']*len(switch_listbox3))})""")
    if switch_listbox4!=['']:
        params.extend(str(x) for x in switch_listbox4)
        where_clause.append(f""""Размещение" IN ({','.join(['%s']*len(switch_listbox4))})""")
    if where_clause:
        switch_query += ' AND '.join(where_clause)
    cur.execute(switch_query, switch_listbox1 + switch_listbox2 + switch_listbox3 + switch_listbox4)
    switch_results = cur.fetchall()
    id_com_list=[results[0] for results in switch_results[:5]]
    num_elements=len(id_com_list)
    stack="INSERT INTO stack_com({}) VALUES ({})".format(
        ", ".join(f"id_com{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_com_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_com FROM stack_com ORDER BY id_stack_com DESC LIMIT 1"
    cur.execute(id_stack)
    stack_com=cur.fetchone()

    router_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Маршрутизаторы", "Характеристики маршрутизаторов" WHERE "Характеристики маршрутизаторов"."ID_характеристики"="Маршрутизаторы"."ID_характеристики" AND """

    where_clause = []
    params=[]
    if router_field1!='':
        where_clause.append(f""""Порты WAN/LAN" >= '{router_field1}'""")
    if router_listbox!=['']:
        params.extend(str(x) for x in router_listbox)
        where_clause.append(f""""Поддержка IPv6" IN ({','.join(['%s']*len(router_listbox))})""")
    if where_clause:
        router_query += ' AND '.join(where_clause)
    cur.execute(router_query, params)
    router_results = cur.fetchall()
    id_marsh_list=[results[0] for results in router_results[:5]]
    num_elements=len(id_marsh_list)
    stack="INSERT INTO stack_marsh({}) VALUES ({})".format(
        ", ".join(f"id_marsh{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_marsh_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_marsh FROM stack_marsh ORDER BY id_stack_marsh DESC LIMIT 1"
    cur.execute(id_stack)
    stack_marsh=cur.fetchone()

    wifi_router_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Wi-Fi роутеры", "Характеристики Wi-Fi роутеров" WHERE "Характеристики Wi-Fi роутеров"."ID_характеристики"="Wi-Fi роутеры"."ID_характеристики" AND """

    where_clause = []
    params=[]
    if wifi_router_field1!='':
        where_clause.append(f""""Порты WAN/LAN" >= '{wifi_router_field1}'""")
    if wifi_router_listbox1!=['']:
        params.extend(str(x) for x in wifi_router_listbox1)
        where_clause.append(f""""Стандарты Wi-Fi" IN ({','.join(['%s']*len(wifi_router_listbox1))})""")
    if wifi_router_listbox2!=['']:
        params.extend(str(x) for x in wifi_router_listbox2)
        where_clause.append(f""""Скорость передачи" IN ({','.join(['%s']*len(wifi_router_listbox2))})""")
    if wifi_router_listbox3!=['']:
        params.extend(str(x) for x in wifi_router_listbox3)
        where_clause.append(f""""Поддержка IPv6" IN ({','.join(['%s']*len(wifi_router_listbox3))})""")
    if where_clause:
        wifi_router_query += ' AND '.join(where_clause)
    cur.execute(wifi_router_query, params)
    wifi_router_results = cur.fetchall()
    id_wifi_router_list=[results[0] for results in wifi_router_results[:5]]
    num_elements=len(id_wifi_router_list)
    stack="INSERT INTO stack_router({}) VALUES ({})".format(
        ", ".join(f"id_router{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_wifi_router_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_router FROM stack_router ORDER BY id_stack_router DESC LIMIT 1"
    cur.execute(id_stack)
    stack_router=cur.fetchone()

    server_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Серверные платформы", "Характеристики серверных платформ" WHERE "Характеристики серверных платформ"."ID_характеристики"="Серверные платформы"."ID_характеристики" AND """

    where_clause = []
    params=[]
    if server_field1!='':
        where_clause.append(f""""Порты WAN/LAN" >= '{server_field1}'""")
    if server_field2!='':
        where_clause.append(f""""Порты USB" >= '{server_field2}'""")
    if server_field3!='':
        where_clause.append(f""""Количество процессоров" >= '{server_field3}'""")
    if server_field4!='':
        where_clause.append(f""""Дисковая корзина" >= '{server_field4}'""")
    if server_listbox1!=['']:
        params.extend(str(x) for x in server_listbox1)
        where_clause.append(f""""Процессор" IN ({','.join(['%s']*len(server_listbox1))})""")
    if where_clause:
        server_query += ' AND '.join(where_clause)
    cur.execute(server_query, params)
    server_results = cur.fetchall()
    id_server_list=[results[0] for results in server_results[:5]]
    num_elements=len(id_server_list)
    stack="INSERT INTO stack_server({}) VALUES ({})".format(
        ", ".join(f"id_server{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_server_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_server FROM stack_server ORDER BY id_stack_server DESC LIMIT 1"
    cur.execute(id_stack)
    stack_server=cur.fetchone()

    access_point_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Точки доступа Wi-Fi", "Характеристики точек доступа Wi-Fi" WHERE "Характеристики точек доступа Wi-Fi"."ID_характеристики"="Точки доступа Wi-Fi"."ID_характеристики" AND """
    params=[]
    where_clause = []
    if access_point_field1!='':
        where_clause.append(f""""Порты WAN/LANПорты WAN/LAN" >= '{access_point_field1}'""")
    if access_point_listbox1!=['']:
        params.extend(str(x) for x in access_point_listbox1)
        where_clause.append(f""""Стандарты Wi-Fi" IN ({','.join(['%s']*len(access_point_listbox1))})""")
    if access_point_listbox2!=['']:
        params.extend(str(x) for x in access_point_listbox2)
        where_clause.append(f""""Размещение" IN ({','.join(['%s']*len(access_point_listbox2))})""")
    if access_point_listbox3!=['']:
        params.extend(str(x) for x in access_point_listbox3)
        where_clause.append(f""""Варианты крепления" IN ({','.join(['%s']*len(access_point_listbox3))})""")
    if where_clause:
        access_point_query += ' AND '.join(where_clause)
    cur.execute(access_point_query, params)
    access_point_results = cur.fetchall()
    id_access_point_list=[results[0] for results in access_point_results[:5]]
    num_elements=len(id_access_point_list)
    stack="INSERT INTO stack_toch({}) VALUES ({})".format(
        ", ".join(f"id_toch{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_access_point_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_toch FROM stack_toch ORDER BY id_stack_toch DESC LIMIT 1"
    cur.execute(id_stack)
    stack_toch=cur.fetchone()

    cabinet_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Шкафы и стойки", "Характеристики шкафов" WHERE "Характеристики шкафов"."ID_характеристики"="Шкафы и стойки"."ID_характеристики" AND """
    params=[]
    where_clause = []
    if cabinet_field1!='':
        where_clause.append(f""""Число секций" => '{cabinet_field1}'""")
    if cabinet_field2!='':
        where_clause.append(f""""Высота" =< '{cabinet_field2}'""")
    if cabinet_listbox1!=['']:
        params.extend(str(x) for x in cabinet_listbox1)
        where_clause.append(f""""Установка" IN ({','.join(['%s']*len(cabinet_listbox1))})""")
    if cabinet_listbox2!=['']:
        params.extend(str(x) for x in cabinet_listbox2)
        where_clause.append(f""""Защита" IN ({','.join(['%s']*len(cabinet_listbox2))})""")
    if cabinet_listbox3!=['']:
        params.extend(str(x) for x in cabinet_listbox3)
        where_clause.append(f""""Тип шкафа" IN ({','.join(['%s']*len(cabinet_listbox3))})""")
    if where_clause:
        cabinet_query += ' AND '.join(where_clause)
    cur.execute(cabinet_query, params)
    cabinet_results = cur.fetchall()
    id_cabinet_list=[results[0] for results in cabinet_results[:5]]
    num_elements=len(id_cabinet_list)
    stack="INSERT INTO stack_shkaf({}) VALUES ({})".format(
        ", ".join(f"id_shkaf{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_cabinet_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_shkaf FROM stack_shkaf ORDER BY id_stack_shkaf DESC LIMIT 1"
    cur.execute(id_stack)
    stack_shkaf=cur.fetchone()

    network_storage_query = f"""SELECT "ID", "Название", "Ссылки", "Цена" FROM "Сетевые хранилища", "Характеристики сетевых хранилищ" WHERE "Характеристики сетевых хранилищ"."ID_характеристики"="Сетевые хранилища"."ID_характеристики" AND """

    where_clause = []
    if network_storage_field1!='':
        where_clause.append(f""""Количество отсеков" >= '{network_storage_field1}'""")
    if network_storage_field2!='':
        where_clause.append(f""""Максимально поддерживаемый объем" >= '{network_storage_field2}'""")
    if network_storage_field3!='':
        where_clause.append(f""""Количество портов Ethernet" >= '{network_storage_field3}'""")
    if where_clause:
        network_storage_query += ' AND '.join(where_clause)
    cur.execute(network_storage_query)
    network_storage_results = cur.fetchall()
    id_network_storage_list=[results[0] for results in network_storage_results[:7]]
    num_elements=len(id_network_storage_list)
    stack="INSERT INTO stack_chran({}) VALUES ({})".format(
        ", ".join(f"id_chran{i+1}" for i in range(num_elements)),
        ", ".join(f"'{id_network_storage_list[i]}'" for i in range(num_elements))
    )
    cur.execute(stack)
    conn.commit()
    id_stack="SELECT id_stack_chran FROM stack_chran ORDER BY id_stack_chran DESC LIMIT 1"
    cur.execute(id_stack)
    stack_chran=cur.fetchone()

    name_query=f"SELECT id_client FROM users WHERE username='{session.get('username')}'"
    cur.execute(name_query)
    username=cur.fetchone()

    korzina="INSERT INTO korzina(id_stack_router, id_stack_toch, id_stack_com, id_stack_marsh, id_stack_server, id_stack_shkaf, id_stack_chran, id_client) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        stack_router[0], stack_toch[0], stack_com[0], stack_marsh[0], stack_server[0], stack_shkaf[0], stack_chran[0], username[0])
    
    cur.execute(korzina)
    conn.commit()

    cur.close()
    conn.close()

    return render_template('home.html', switch_results=switch_results, router_results=router_results, 
                           wifi_router_results=wifi_router_results, server_results=server_results, 
                           access_point_results=access_point_results, cabinet_results=cabinet_results, 
                           network_storage_results=network_storage_results, row1=row1, row2=row2, row3=row3, 
                           row4=row4, row5=row5, row6=row6, row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, 
                           row12=row12, row13=row13, row14=row14, row15=row15)

app.run(debug=True)