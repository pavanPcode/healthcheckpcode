from flask import Flask,render_template,request,render_template_string,url_for,redirect,session
from Dal import mysqlhelper, mssqlhelper
from datetime import datetime
from utilities.utility import get_current_ist_time,get_data_from_session
from routess.signin import auth,login_required
from routess import NotifyLogs,BookMyOtLogs,RollcallMails,CampusLogs,Fit4LifeLogs,Novotel,Timerjob

app = Flask(__name__)
app.secret_key = 'your_secret_keyahfdk343jhdjjkjrjt765dgfgfggf6565sal'

HealthCheck_Prod = 'HealthCheck_Prod'
dbcloudrollcallSwipes= 'Hrms'

app.register_blueprint(auth)
app.register_blueprint(NotifyLogs.Notifyapp)
app.register_blueprint(BookMyOtLogs.bookmyotapp)
app.register_blueprint(RollcallMails.Rollcallmailsapp)
app.register_blueprint(CampusLogs.Campusapp)
app.register_blueprint(Fit4LifeLogs.Fit4Lifeapp)
app.register_blueprint(Novotel.Novotelapp)
app.register_blueprint(Timerjob.TimerJobsapp)
@app.route('/cloudrollcallSwipes',methods=['POST','GET'])
@login_required
def cloudrollcallSwipes():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            cur_ist_date, cur_ist_time = get_current_ist_time()
            cur_ist_datestr = cur_ist_date.strftime('%Y-%m-%d')
            quary = f"""SELECT id, transid, deviceid, empcode, punchdt, ischeckin, ispushed, createdon,superId
                    FROM HrmsSwipeTransactions WHERE 
                         DATE(punchdt) = '{cur_ist_datestr}' ; """
        elif request.method == 'POST':
            # Retrieve form data
            #log_type = request.form['log_type']
            status = request.form['Attandancetype']
            chosen_date = request.form['chosen_date']
            ispushed = request.form['ispushed']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")
            quary = f"""SELECT id, transid, deviceid, empcode, punchdt, ischeckin, ispushed, createdon,superId
                    FROM hrmsSwipeTransactions WHERE 
                         DATE(punchdt) = '{chosen_date}' and  ischeckin = {status} and ispushed = {ispushed}"""
            print(quary)
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="cloudrollcallSwipesforzoho.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500

@app.route('/zohosettings',methods=['GET'])
@login_required
def zohosettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select * from Hrmszohosettings; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="zohoSettings.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500

@app.route('/FrappeHrSettings',methods=['GET'])
@login_required
def FrappeHrSettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select * from FrappeHrSettings; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="FrappeHrSettings.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500

@app.route('/add_rollcal_token', methods=['POST'])
def create_category():
    # Capture form data
    superid = request.form.get('superid')
    token = request.form.get('token')
    notes = request.form.get('notes')

    quary = f"""INSERT INTO Hrmscloudrollcallconfigurations (superid, token, notes) 
                    VALUES ({superid}, '{token}', '{notes}'); """
    sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
    data = sqlobj.update(quary)
    # Redirect to the category list or do other processing
    return redirect(url_for('cloudrollcallsettings'))


@app.route('/cloudrollcallsettings',methods=['GET'])
@login_required
def cloudrollcallsettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select *  from Hrmscloudrollcallconfigurations where isactive = 1; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="cloudrollcallsettings.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500


@app.route('/IceHrmssettings',methods=['GET'])
@login_required
def IceHrmssettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select *  from HrmsIceHrmsSettings where isactive = 1; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="IceHrmsettings.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500

# Custom 404 error handler
@app.errorhandler(404)
@login_required
def page_not_found(error):
    print(error)
    return render_template('under-maintenance.html'), 404

# Custom 500 error handler
@app.errorhandler(500)
@login_required
def internal_server_error(error):
    return render_template('error-500.html'), 500

if __name__ == '__main__':
    app.run()
