from datetime import datetime
import os
from os import getenv


from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, jsonify
from flask_mysqldb import MySQL
import yaml
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from src.models.role import Role
import smtplib
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bcrypt import Bcrypt

app = Flask('__name__')

app.secret_key = "goodluckwithprogrammer"

#bootstrap = Bootstrap(app)
moment = Moment(app)

# Connecting to Database Mysql
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] =db['mysql_host']
app.config['MYSQL_USER'] =db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

# login route
@app.route('/login', methods =['POST', 'GET'])
def login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username ='" + username + "' and password ='" + password +"'")
        user = cursor.fetchone()
        if user is None:
            flash('Invalid username or password.')
            return render_template('login1.html')

        else:
            session['user']=user
            return redirect(url_for('create_tools'))
    else:
        return render_template('login1.html')


# logout route
@app.route('/logout')
def logout():
    session.pop("user", None)
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/login/create_tools')
def create_tools():
    return render_template('menu_user.html', user=session['user'])#, current_time=datetime.utcnow())


# create user for system
@app.route('/login/create_user', methods=['GET', 'POST'])
def create_user():
    cur = mysql.connection.cursor()
    roles = cur.execute("SELECT *FROM role")
    if roles > 0:
        userDetails = cur.fetchall()
    if request.method == 'POST':
        first_name = request.form['name']
        last_name = request.form['last_name']
        celphone = request.form['phone_number']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, username, password,email, celphone, role_id) VALUES "
                    "(%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name,username,password,email, celphone, role))

        mysql.connection.commit()
        cur.close()

        # message = "Congratulation your username: julio.manhica1 e senha:12345, now registered!"
        # server = smtplib.SMTP("smtp.gmail.com", 465)
        # server.starttls()
        # server.login("techcelito01@gmail.com", 'Nekeisk01')
        # server.sendmail("erciliomboa@gmail.com", email, message)
        # server.quit()
        #flash("Data Inserted Successfully")
        return "Done"
    else:
        return render_template('create_user.html', userDetails=userDetails,  user = session['user'])

@app.route('/login/create_tools/list_user')
def list_user():
    cur = mysql.connection.cursor()
    user = cur.execute(" SELECT first_name, last_name, username, email, celphone, type_role from users JOIN role "
                       "ON users.role_id=role.role_id")
    if user > 0:
        userDetails = cur.fetchall()
    return render_template('view_user.html', userDetails=userDetails)

@app.route('/login/vehicle_registration', methods=['GET','POST'])
def vehicle_registration():
    # getting the elements of first drop down
    # cur = mysql.connection.cursor()
    # address = cur.execute("SELECT * from province")
    # if address > 0:
    #     provinces = cur.fetchall()
    # # getting the elements of second drop down
    # drop = cur.execute("SELECT * FROM district")
    # if drop > 0:
    #     districts = cur.fetchall()
    #html_string_selected = ''
    # ret =''
    #for entry in districts:
        #html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)
        #ret += '<option value="{}">{}</option>'.format(entry[0], entry[1])
    #return jsonify( ret=ret)
    # return render_template('test.html', provinces=provinces, districts=districts)
    return render_template('test.html')

@app.route('/provinces')
def provinces():
    cur = mysql.connection.cursor()
    prv = cur.execute("SELECT * FROM province")
    provinces = []
    if prv > 0:
        provinces = cur.fetchall()
    return jsonify(provinces)


@app.route('/districts')
def districts():
    cur = mysql.connection.cursor()
    dist = cur.execute("SELECT * FROM district")
    districts = []
    if dist > 0:
        districts = cur.fetchall()
    return jsonify(districts)


@app.route('/vehicle_brand')
def vehicle_brand():
    cur = mysql.connection.cursor()
    prv = cur.execute("SELECT * FROM vehicle_brand")
    vBrands = []
    if prv > 0:
        vBrands = cur.fetchall()
    return jsonify(vBrands)


@app.route('/model')
def model():
    cur = mysql.connection.cursor()
    dist = cur.execute("SELECT * FROM model")
    models = []
    if dist > 0:
        models = cur.fetchall()
    return jsonify(models)

#this part is for automovel tools register VIEWWWWWWWWWWWWWWWWW





@app.route('/login/register', methods=['POST', 'GET'])
def auto_register():
    user= session['user']
    cur = mysql.connection.cursor()
    dist = cur.execute("SELECT * FROM fuel")
    if dist > 0:
        fuels = cur.fetchall()
    dist = cur.execute("SELECT * FROM body_type")
    if dist > 0:
        bodytypes = cur.fetchall()
    dist = cur.execute("SELECT * FROM marital_status")
    if dist > 0:
        maritals = cur.fetchall()

    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        id_num = request.form['id_number']
        date_birth = request.form['birthday']
        m_status = request.form['mar_status']
        profession = request.form['profession']
        province = request.form['select_province']
        district = request.form['select_district']
        neighbor_description = request.form['neighbor']
        street_num = request.form['add_details']
        license_num = request.form['plate_num']
        reg_date = request.form['reg_date']
        brands = request.form['select_brand']
        model = request.form['select_model']
        fuel = request.form['select_fuel']
        body_type = request.form['select_bdtype']
        service = request.form['service']
        seat = request.form['seat']
        chassis = request.form['chassis']
        eng_size = request.form['engine_size']
        cylinder = request.form['cylinder']
        weight = request.form['weight']
        color = request.form['color']
        wheel_size = request.form['wheel_size']
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO neighborhood(neighbor_description, Av_street_Numeber, district_id) VALUES "
                    "(%s, %s, %s)", (neighbor_description, street_num, district))

        cur.execute("INSERT INTO individual_owner(identification_num, first_name, last_name, profession, birth_date, marital_st_id) VALUES "
                    "(%s, %s, %s, %s, %s, %s)", (id_num, first_name, last_name, profession, date_birth, m_status))

        cur.execute("INSERT INTO owner(identification_num, province_id) VALUES "
                    "(%s, %s)", (id_num, province))
        last_id = cur.lastrowid

        cur.execute("INSERT INTO vehicle(license_plate_num, process_num, chassis_number, engine_size, cylinder, wheel_mesures, weight, "
                    "seats, Ext_color, service, registration_date, owner_id, brand_id, fuel_id, bodyType_id ) "
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (license_num, id_num, chassis, eng_size, cylinder, wheel_size, weight, seat, color, service, reg_date, last_id,
                     str(brands), str(fuel), str(body_type)))
        mysql.connection.commit()
        cur.close()

        return "Done"
    else:

        return render_template('automovel_register.html', fuels=fuels, bodytypes=bodytypes, maritals=maritals, user=user)


@app.route('/search', methods=['GET', 'POST'])
def search_for_mortgage():
    cur = mysql.connection.cursor()
    if request.method =='POST':
        license_plt = request.form.get('license')
        brand = request.form.get('select_brand')
        model = request.form.get('data')
        # cur.execute("SELECT * FROM vehicle WHERE license_plate_num= '"+license_plt+"'")
        details = cur.execute("SELECT v.license_plate_num, vb.description, m.description, iw.first_name, iw.last_name, in_favor  FROM vehicle v "
                            "JOIN owner o ON v.owner_id = o.owner_id",
                            "JOIN individual_owner iw ON o.identification_num = iw.identification_num"
                            "JOIN mortage mrt ON v.mortage_id = mrt.mortage_id"
                            "JOIN vehicle_brand vb ON v.brand_id = vb.brand_id"
                            "JOIN model m"
                            "WHERE license_plate_num ='"+license_plt+"' and m.model_id = '"+model+"'")
        # if detail > 0:
        details = cur.fetchone()
        # details =cur.fetchone()
        mysql.connection.commit()
        mysql.connection.close()
        return render_template('search_for_mortgage.html', details=details)

    return render_template('search_for_mortgage.html')
# @app.route('/process_data')
# def process_data():
#     selected_class = request.args.get('provinces', type=str)
#     selected_entry = request.args.get('selected_entry', type=str)
#
#     # process the two selected values here and return the response; here we just create a dummy string
#
#     return jsonify(random_text="you selected {} and {}".format(selected_class, selected_entry))

# @app.route('/select_province', methods=['GET', 'POST'])
# def select_province():
#     ret = ''
#     cur = mysql.connection.cursor()
#     address = cur.execute("SELECT prv.province_id, prv.description, dist.district_id, dist.description "
#                           "from province prv JOIN district dist ON prv.province_id=dist.province_id")
#     if address > 0:
#         addressDetails = cur.fetchall()
#     for entry in addressDetails:
#         #data = {"id": entry[0], "name": entry[1]}
#         #addressDetail = jsonify(data)
#         #ret += '<option value="{}">{}</option>'.format(data)
#         ret += '<option value="%i">%s</option>' % (entry[0], entry[1])
#         return ret
#     #return render_template('test.html', addressDetails=addressDetails)



@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    user = cur.execute("SELECT *FROM users")
    if user > 0:
        userDetails = cur.fetchall()

        return render_template('index.html', userDetails=userDetails)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

if __name__ == ('__main__'):
    app.run(debug=True)