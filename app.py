from flask import Flask, render_template, request, redirect, session, url_for
import os

import psycopg2

app = Flask(__name__)
app.secret_key = 'hello'

db_host = 'localhost'
db_name = 'postgres'
db_user = 'postgres'
db_password = '14789635'

switches_table = 'charact_com'
routers_table = 'routers'
wifi_routers_table = 'wifi_routers'
server_platforms_table = 'server_platforms'
access_points_table = 'access_points'
cabinets_table = 'cabinets'
network_storage_table = 'network_storage'

conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

cur.execute("SELECT DISTINCT charact4 from charact_com Where charact4!=' '")
row1 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact5 from charact_com Where charact5!=' '")
row2 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact6 from charact_com Where charact6!=' '")
row3 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact7 from charact_com Where charact7!=' '")
row4 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact3 from charact_server Where charact3!=' '")
row5 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact3 from charact_toch Where charact3!=' '")
row6 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact4 from charact_toch Where charact4!=' '")
row7 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact5 from charact_toch Where charact5!=' '")
row8 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact1 from charact_shkaf Where charact1!=' '")
row9 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact3 from charact_shkaf Where charact3!=' '")
row10 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact5 from charact_shkaf Where charact5!=' '")
row11 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact4 from charact_marsh Where charact4!=' '")
row12 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact3 from charact_router Where charact3!=' '")
row13 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact4 from charact_router Where charact4!=' '")
row14 = cur.fetchall()
cur.execute(f"SELECT DISTINCT charact5 from charact_router Where charact5!=' '")
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
            session['is_admin'] = user[0]
            if user[0]:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid login credentials')
    else:
        return render_template('login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
    cur = conn.cursor()
    if 'username' in session and session['is_admin']:
        if request.method == 'POST':
            print(request.form.get('submit'))
            if request.form['submit']=='Вывод таблицы':
                table_name = request.form['table_name']

                cur.execute(f"SELECT * FROM {table_name}, charact_{table_name} WHERE {table_name}.id_charact=charact_{table_name}.id_charact")
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
                field9 = request.form['field9']
                field10 = request.form['field10']
                table_name1 = request.form.getlist('table_name1')

                if table_name1==['com']:
                    cur.execute(f"INSERT INTO charact_com(charact2, charact3, charact4, charact5, charact6, charact7, charact8) VALUES ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}', '{field9}', '{field10}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_com ORDER BY id_charact DESC LIMIT 1")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO com(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
                    conn.commit()
                elif table_name1==['marsh']:
                    cur.execute(f"INSERT INTO charact_marsh (charact1, charact2, charact3, charact4) VALUES ('{field4}', '{field5}', '{field6}', '{field7}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_marsh ORDER BY id_charact DESC LIMIT 1")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO marsh(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
                    conn.commit()
                elif table_name1==['router']:
                    cur.execute(f"INSERT INTO charact_router(charact1, charact2, charact3, charact4, charact5) VALUES ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_router ORDER BY id_charact DESC LIMIT 1;")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO router(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
                    conn.commit()
                elif table_name1==['server']:
                    cur.execute(f"INSERT INTO charact_server (charact1, charact2, charact3, charact4, charact5, charact6) VALUES ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}', '{field9}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_server ORDER BY id_charact DESC LIMIT 1;")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO server(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
                    conn.commit()
                elif table_name1==['shkaf']:
                    cur.execute(f"INSERT INTO charact_shkaf(charact1, charact2, charact3, charact4, charact5) VALUES ('{field4}', '{field5}', '{field6}', '{field7}', '{field8}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_shkaf ORDER BY id_charact DESC LIMIT 1;")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO shkaf(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
                    conn.commit()
                elif table_name1==['toch']:
                    cur.execute(f"INSERT INTO charact_toch(charact2, charact3, charact4, charact5) VALUES ('{field4}', '{field5}', '{field6}', '{field7}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_toch ORDER BY id_charact DESC LIMIT 1;")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO toch(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
                    conn.commit()
                elif table_name1==['chran']:
                    cur.execute(f"INSERT INTO charact_chran(charact1, charact2, charact3, charact4) VALUES ('{field4}', '{field5}', '{field6}', '{field7}')")
                    conn.commit()
                    cur.execute("SELECT id_charact FROM charact_chran ORDER BY id_charact DESC LIMIT 1;")
                    index=cur.fetchone()
                    cur.execute(f"INSERT INTO chran(name, price, link, id_charact) VALUES ('{field1}', '{field2}', '{field3}', '{index[0]}')")
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
                field9 = request.form['field9']
                field10 = request.form['field10']
                table_name1 = request.form.getlist('table_name1')

                query=[]

                if table_name1==['com']:
                    if field01!='':
                        update_query=f"UPDATE charact_com SET "
                        if field4!='':
                            query.append(f"charact2='{field4}'")
                        if field5!='':
                            query.append(f"charact3='{field5}'")
                        if field6!='':
                            query.append(f"charact4='{field6}'")
                        if field7!='':
                            query.append(f"charact5='{field7}'")
                        if field8!='':
                            query.append(f"charact6='{field8}'")
                        if field9!='':
                            query.append(f"charact7='{field9}'")
                        if field10!='':
                            query.append(f"charact8='{field10}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE com SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_com='{field0}'"
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['marsh']:
                    if field01!='':
                        update_query=f"UPDATE charact_marsh SET "
                        if field4!='':
                            query.append(f"charact1='{field4}'")
                        if field5!='':
                            query.append(f"charact2='{field5}'")
                        if field6!='':
                            query.append(f"charact3='{field6}'")
                        if field7!='':
                            query.append(f"charact4='{field7}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE marsh SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_marsh='{field0}'"
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['router']:
                    print('Hello')
                    if field01!='':
                        update_query=f"UPDATE charact_router SET "
                        if field4!='':
                            query.append(f"charact1='{field4}'")
                        if field5!='':
                            query.append(f"charact2='{field5}'")
                        if field6!='':
                            query.append(f"charact3='{field6}'")
                        if field7!='':
                            query.append(f"charact4='{field7}'")
                        if field8!='':
                            query.append(f"charact5='{field8}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE router SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_router='{field0}'"
                        cur.execute(update_query)
                        conn.commit()
                    conn.commit()
                elif table_name1==['server']:
                    if field01!='':
                        update_query=f"UPDATE charact_server SET "
                        if field4!='':
                            query.append(f"charact1='{field4}'")
                        if field5!='':
                            query.append(f"charact2='{field5}'")
                        if field6!='':
                            query.append(f"charact3='{field6}'")
                        if field7!='':
                            query.append(f"charact4='{field7}'")
                        if field8!='':
                            query.append(f"charact5='{field8}'")
                        if field9!='':
                            query.append(f"charact6='{field9}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE server SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_server='{field0}'"
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['shkaf']:
                    if field01!='':
                        update_query=f"UPDATE charact_shkaf SET "
                        if field4!='':
                            query.append(f"charact1='{field4}'")
                        if field5!='':
                            query.append(f"charact2='{field5}'")
                        if field6!='':
                            query.append(f"charact3='{field6}'")
                        if field7!='':
                            query.append(f"charact4='{field7}'")
                        if field8!='':
                            query.append(f"charact5='{field8}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE shkaf SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_shkaf='{field0}'"
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['toch']:
                    if field01!='':
                        update_query=f"UPDATE charact_toch SET "
                        if field4!='':
                            query.append(f"charact2='{field4}'")
                        if field5!='':
                            query.append(f"charact3='{field5}'")
                        if field6!='':
                            query.append(f"charact4='{field6}'")
                        if field7!='':
                            query.append(f"charact5='{field7}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE toch SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_toch='{field0}'"
                        cur.execute(update_query)
                        conn.commit()
                elif table_name1==['chran']:
                    if field01!='':
                        update_query=f"UPDATE charact_chran SET "
                        if field4!='':
                            query.append(f"charact1='{field4}'")
                        if field5!='':
                            query.append(f"charact2='{field5}'")
                        if field6!='':
                            query.append(f"charact3='{field6}'")
                        if field7!='':
                            query.append(f"charact4='{field7}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_charact='{field01}'"
                        cur.execute(update_query) 
                        conn.commit()
                    if field0!='':
                        query=[]
                        update_query=f"UPDATE chran SET "
                        if field1!='':
                            query.append(f"name='{field1}'")
                        if field2!='':
                            query.append(f"price='{field2}'")
                        if field3!='':
                            query.append(f"link='{field3}'")
                        if query!='':
                            update_query+= ', '.join(query)
                        update_query+=f" WHERE id_chran='{field0}'"
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
                        delete_query1=f"DELETE FROM charact_com USING com WHERE com.id_charact=charact_com.id_charact AND com.id_com='{field0}'"
                        delete_query=f"DELETE FROM com WHERE id_com='{field0}'"
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()
                
                elif table_name1==['marsh']:
                    if field0!='':
                        delete_query1=f"DELETE FROM charact_marsh USING marsh WHERE marsh.id_charact=charact_marsh.id_charact AND marsh.id_marsh='{field0}'"
                        delete_query=f"DELETE FROM marsh WHERE id_marsh='{field0}'"
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['router']:
                    if field0!='':
                        delete_query1=f"DELETE FROM charact_router USING router WHERE router.id_charact=charact_router.id_charact AND router.id_router='{field0}'"
                        delete_query=f"DELETE FROM router WHERE id_router='{field0}'"
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['server']:
                    if field0!='':
                        delete_query1=f"DELETE FROM charact_server USING server WHERE server.id_charact=charact_server.id_charact AND server.id_server='{field0}'"
                        delete_query=f"DELETE FROM server WHERE id_server='{field0}'"
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()
                
                elif table_name1==['shkaf']:
                    if field0!='':
                        delete_query1=f"DELETE FROM charact_shkaf USING shkaf WHERE shkaf.id_charact=charact_shkaf.id_charact AND shkaf.id_shkaf='{field0}'"
                        delete_query=f"DELETE FROM shkaf WHERE id_shkaf='{field0}'"
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['toch']:
                    if field0!='':
                        delete_query1=f"DELETE FROM charact_toch USING toch WHERE toch.id_charact=charact_toch.id_charact AND toch.id_toch='{field0}'"
                        delete_query=f"DELETE FROM toch WHERE id_toch='{field0}'"
                        cur.execute(delete_query1)
                        cur.execute(delete_query)
                        conn.commit()

                elif table_name1==['chran']:
                    if field0!='':
                        delete_query1=f"DELETE FROM charact_chran USING chran WHERE chran.id_charact=charact_chran.id_charact AND chran.id_chran='{field0}'"
                        delete_query=f"DELETE FROM chran WHERE id_chran='{field0}'"
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
            return render_template('register.html', error='Username already exists')
        else:
            cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
            conn.commit()
            cur.close()
            conn.close()

            session['username'] = username
            return redirect(url_for('home'))
    else:
        return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():

    switch_field1 = request.form['switch_field1']
    switch_field2 = request.form['switch_field2']
    switch_listbox1 = request.form.getlist('switch_listbox1')
    switch_listbox2 = request.form.getlist('switch_listbox2')
    switch_listbox3 = request.form.getlist('switch_listbox3')
    switch_listbox4 = request.form.getlist('switch_listbox4')

    router_field1 = request.form['router_field1']
    router_field2 = request.form['router_field2']
    router_field3 = request.form['router_field3']
    router_listbox = request.form.getlist('router_listbox')

    wifi_router_field1 = request.form['wifi_router_field1']
    wifi_router_field2 = request.form['wifi_router_field2']
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

    switch_query = f"SELECT name, price, link FROM com, charact_com WHERE charact_com.id_charact=com.id_charact AND "

    where_clause = []
    params=[]
    if switch_field1!='':
        where_clause.append(f"charact2 = '{switch_field1}'")
    if switch_field2!='':
        where_clause.append(f"charact3 = '{switch_field2}'")
    if switch_listbox1!=['']:
        params.extend(str(x) for x in switch_listbox1)
        where_clause.append(f"charact4 IN ({','.join(['%s']*len(switch_listbox1))})")
    if switch_listbox2!=['']:
        params.extend(str(x) for x in switch_listbox2)
        where_clause.append(f"charact5 IN ({','.join(['%s']*len(switch_listbox2))})")
    if switch_listbox3!=['']:
        params.extend(str(x) for x in switch_listbox3)
        where_clause.append(f"charact6 IN ({','.join(['%s']*len(switch_listbox3))})")
    if switch_listbox4!=['']:
        params.extend(str(x) for x in switch_listbox4)
        where_clause.append(f"charact7 IN ({','.join(['%s']*len(switch_listbox4))})")
    if where_clause:
        switch_query += ' AND '.join(where_clause)
    cur.execute(switch_query, switch_listbox1 + switch_listbox2 + switch_listbox3 + switch_listbox4)
    switch_results = cur.fetchall()

    router_query = f"SELECT name, price, link FROM marsh, charact_marsh WHERE charact_marsh.id_charact=marsh.id_charact AND "

    where_clause = []
    params=[]
    if router_field1!='':
        where_clause.append(f"charact1 = '{router_field1}'")
    if router_field2!='':
        where_clause.append(f"charact2 = '{router_field2}'")
    if router_field3!='':
        where_clause.append(f"charact3 = '{router_field3}'")
    if router_listbox!=['']:
        params.extend(str(x) for x in router_listbox)
        where_clause.append(f"charact4 IN ({','.join(['%s']*len(router_listbox))})")
    if where_clause:
        router_query += ' AND '.join(where_clause)
    print(router_query, params)
    cur.execute(router_query, params)
    router_results = cur.fetchall()

    wifi_router_query = f"SELECT name, price, link FROM router, charact_router WHERE charact_router.id_charact=router.id_charact AND "

    where_clause = []
    params=[]
    if wifi_router_field1!='':
        where_clause.append(f"charact1 = '{wifi_router_field1}'")
    if wifi_router_field2!='':
        where_clause.append(f"charact2 = '{wifi_router_field2}'")
    if wifi_router_listbox1!=['']:
        params.extend(str(x) for x in wifi_router_listbox1)
        where_clause.append(f"charact3 IN ({','.join(['%s']*len(wifi_router_listbox1))})")
    if wifi_router_listbox2!=['']:
        params.extend(str(x) for x in wifi_router_listbox2)
        where_clause.append(f"charact4 IN ({','.join(['%s']*len(wifi_router_listbox2))})")
    if wifi_router_listbox3!=['']:
        params.extend(str(x) for x in wifi_router_listbox3)
        where_clause.append(f"charact5 IN ({','.join(['%s']*len(wifi_router_listbox3))})")
    if where_clause:
        wifi_router_query += ' AND '.join(where_clause)
    print(wifi_router_query, params)
    cur.execute(wifi_router_query, params)
    wifi_router_results = cur.fetchall()

    server_query = f"SELECT name, price, link FROM server, charact_server WHERE charact_server.id_charact=server.id_charact AND "

    where_clause = []
    params=[]
    if server_field1!='':
        where_clause.append(f"charact1 = '{server_field1}'")
    if server_field2!='':
        where_clause.append(f"charact3 = '{server_field2}'")
    if server_field3!='':
        where_clause.append(f"charact4 = '{server_field3}'")
    if server_field4!='':
        where_clause.append(f"charact5 = '{server_field4}'")
    if server_listbox1!=['']:
        params.extend(str(x) for x in server_listbox1)
        where_clause.append(f"charact2 IN ({','.join(['%s']*len(server_listbox1))})")
    if where_clause:
        server_query += ' AND '.join(where_clause)
    print(server_query, params)
    cur.execute(server_query, params)
    server_results = cur.fetchall()

    access_point_query = f"SELECT name, price, link FROM toch, charact_toch WHERE charact_toch.id_charact=toch.id_charact AND "
    params=[]
    where_clause = []
    if access_point_field1!='':
        where_clause.append(f"charact2 = '{access_point_field1}'")
    if access_point_listbox1!=['']:
        params.extend(str(x) for x in access_point_listbox1)
        where_clause.append(f"charact3 IN ({','.join(['%s']*len(access_point_listbox1))})")
    if access_point_listbox2!=['']:
        params.extend(str(x) for x in access_point_listbox2)
        where_clause.append(f"charact4 IN ({','.join(['%s']*len(access_point_listbox2))})")
    if access_point_listbox3!=['']:
        params.extend(str(x) for x in access_point_listbox3)
        where_clause.append(f"charact5 IN ({','.join(['%s']*len(access_point_listbox3))})")
    if where_clause:
        access_point_query += ' AND '.join(where_clause)
    print(access_point_query, params)
    cur.execute(access_point_query, params)
    access_point_results = cur.fetchall()

    cabinet_query = f"SELECT name, price, link FROM shkaf, charact_shkaf WHERE charact_shkaf.id_charact=shkaf.id_charact AND "
    params=[]
    where_clause = []
    if cabinet_field1!='':
        where_clause.append(f"charact2 = '{cabinet_field1}'")
    if cabinet_field2!='':
        where_clause.append(f"charact4 = '{cabinet_field2}'")
    if cabinet_listbox1!=['']:
        params.extend(str(x) for x in cabinet_listbox1)
        where_clause.append(f"charact1 IN ({','.join(['%s']*len(cabinet_listbox1))})")
    if cabinet_listbox2!=['']:
        params.extend(str(x) for x in cabinet_listbox2)
        where_clause.append(f"charact3 IN ({','.join(['%s']*len(cabinet_listbox2))})")
    if cabinet_listbox3!=['']:
        params.extend(str(x) for x in cabinet_listbox3)
        where_clause.append(f"charact5 IN ({','.join(['%s']*len(cabinet_listbox3))})")
    if where_clause:
        cabinet_query += ' AND '.join(where_clause)
    cur.execute(cabinet_query, params)
    cabinet_results = cur.fetchall()

    network_storage_query = f"SELECT name, price, link FROM chran, charact_chran WHERE charact_chran.id_charact=chran.id_charact AND "

    where_clause = []
    if network_storage_field1!='':
        where_clause.append(f"charact1 = '{network_storage_field1}'")
    if network_storage_field2!='':
        where_clause.append(f"charact2 = '{network_storage_field2}'")
    if network_storage_field3!='':
        where_clause.append(f"charact3 = '{network_storage_field3}'")
    if where_clause:
        network_storage_query += ' AND '.join(where_clause)
    print(network_storage_query)
    cur.execute(network_storage_query)
    network_storage_results = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('home.html', switch_results=switch_results, router_results=router_results, 
                           wifi_router_results=wifi_router_results, server_results=server_results, 
                           access_point_results=access_point_results, cabinet_results=cabinet_results, 
                           network_storage_results=network_storage_results, row1=row1, row2=row2, row3=row3, 
                           row4=row4, row5=row5, row6=row6, row7=row7, row8=row8, row9=row9, row10=row10, row11=row11, 
                           row12=row12, row13=row13, row14=row14, row15=row15)

app.run(debug=True)