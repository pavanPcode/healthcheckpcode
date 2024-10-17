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
                         DATE(punchdt) = '{cur_ist_datestr}' order by punchdt desc; """
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

@app.route('/add_zoho_token', methods=['POST'])
def add_zoho_token():
    # Retrieve form data from the POST request
    superid = request.form.get('superid')
    client_id = request.form.get('clientId')
    client_secret = request.form.get('clientSecret')
    refresh_token = request.form.get('refreshToken')
    access_token = request.form.get('accessToken')
    zoho_token_url = request.form.get('zohoTokenUrl')
    attendance_api_url = request.form.get('attendanceApiUrl')

    # Print the data for debugging purposes
    print(f'SuperId: {superid}')
    print(f'Client ID: {client_id}')
    print(f'Client Secret: {client_secret}')
    print(f'Refresh Token: {refresh_token}')
    print(f'Access Token: {access_token}')
    print(f'Zoho Token URL: {zoho_token_url}')
    print(f'Attendance API URL: {attendance_api_url}')
    quary = f"""insert into Hrmszohosettings(superid,clientid,clientsecret,refreshtoken,accesstoken,zohotokenurl,attendanceapiurl)
                values ({superid},'{client_id}','{client_secret}','{refresh_token}','{access_token}','{zoho_token_url}','{attendance_api_url}')"""
    # You can process the data further here, e.g., saving to a database
    sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
    data = sqlobj.update(quary)
    print(data)
    # Return a response to the client
    return redirect(url_for('zohosettings'))

@app.route('/zohosettings',methods=['GET'])
@login_required
def zohosettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select * from Hrmszohosettings where isactive = 1; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="zohoSettings.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500
@app.route('/add_orangehrm_user', methods=['POST'])
def add_orangehrm_user():
    # Retrieve form data from the POST request
    superid = request.form.get('superid')
    client_id = request.form.get('clientId')
    accessToken = request.form.get('accessToken')
    refresh_token = request.form.get('refreshToken')
    OrangeHrmUrl = request.form.get('OrangeHrmUrl')
    OrgName = request.form.get('OrgName')

    quary = f"""INSERT INTO OrangeHRMSettings (superid, OrgName,clientid, refreshtoken, OrangeHrmUrl,accessToken)
            VALUES ({superid}, '{OrgName}','{client_id}', '{refresh_token}', '{OrangeHrmUrl}','{accessToken}');"""
    # You can process the data further here, e.g., saving to a database
    sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
    data = sqlobj.update(quary)
    print(data)
    # Return a response to the client
    return redirect(url_for('orangehrmsettings'))

@app.route('/orangehrmsettings',methods=['GET'])
@login_required
def orangehrmsettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select * from OrangeHRMSettings where isactive = 1; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="orangeSettings.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500


@app.route('/delete_Orange_User', methods=['POST'])
def delete_Orange_User():
    # Retrieve the token ID (timer job ID)
    superid = request.form.get('superid')
    print(superid,'djkhfgkdjh',9348765894348953)
    if superid:
        quary = f"""update OrangeHRMSettings set isactive = 0 where id = {superid}; """
        print(quary)
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.update(quary)
        print(data)
        # Return a success response
        return {'message': 'Token deleted successfully!'}
    else:
        return {'message': 'No token ID provided!'}

@app.route('/delete_zoho_token', methods=['POST'])
def delete_zoho_token():
    # Retrieve the token ID (timer job ID)
    superid = request.form.get('superid')
    print(superid,'djkhfgkdjh',9348765894348953)
    if superid:
        quary = f"""update Hrmszohosettings set isactive = 0 where id = {superid}; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.update(quary)
        print(data)
        # Return a success response
        return {'message': 'Token deleted successfully!'}
    else:
        return {'message': 'No token ID provided!'}
@app.route('/add_FrappeHR', methods=['POST'])
def add_FrappeHR():
    # Retrieve form data from the POST request
    superid = request.form.get('superid')
    token = request.form.get('token')
    apisecret = request.form.get('apisecret')
    checkinapi = request.form.get('checkinapi')
    checkoutapi = request.form.get('checkoutapi')

    # # Print the form data for debugging purposes
    # print(f'SuperId: {superid}')
    # print(f'API Key (Token): {token}')
    # print(f'API Secret: {apisecret}')
    # print(f'Check In API: {checkinapi}')
    # print(f'Check Out API: {checkoutapi}')

    quary = f"""insert into FrappeHrSettings(superid,apikey,apisecret,checkinapi,checkoutapi)
    values ({superid},'{token}','{apisecret}','{checkinapi}','{checkinapi}')"""
    sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
    data = sqlobj.update(quary)
    print(data)
    # Return a success message or JSON response
    return redirect(url_for('FrappeHrSettings'))

@app.route('/delete_frappe_token', methods=['POST'])
def delete_frappe_token():
    # Retrieve the token ID (timer job ID)
    superid = request.form.get('superid')
    print(superid,'djkhfgkdjh',9348765894348953)
    if superid:
        quary = f"""update FrappeHrSettings set isactive = 0 where superid = {superid}; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.update(quary)
        print(data)
        # Return a success response
        return {'message': 'Token deleted successfully!'}
    else:
        return {'message': 'No token ID provided!'}

@app.route('/FrappeHrSettings',methods=['GET'])
@login_required
def FrappeHrSettings():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        quary = f"""select * from FrappeHrSettings where isactive = 1; """
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


@app.route('/delete_token', methods=['POST'])
def delete_token():
    # Retrieve the token ID (timer job ID)
    superid = request.form.get('superid')
    print(superid,'djkhfgkdjh',9348765894348953)
    if superid:
        quary = f"""update Hrmscloudrollcallconfigurations set isactive = 0 where superid = {superid}; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.update(quary)
        print(data)
        # Return a success response
        return {'message': 'Token deleted successfully!'}
    else:
        return {'message': 'No token ID provided!'}


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
        # print(data)
        return render_template('main.html', htmlpage="cloudrollcallsettings.html", data=data['ResultData'],name=name,role=role)
    except Exception as e:
        print(e)
        return render_template('error-500.html', text=str(e)), 500


@app.route('/delete_icehrms_token', methods=['POST'])
def delete_icehrms_token():
    # Retrieve the token ID (timer job ID)
    superid = request.form.get('superid')
    print(superid,'djkhfgkdjh',9348765894348953)
    if superid:
        quary = f"""update HrmsIceHrmsSettings set isactive = 0 where superid = {superid}; """
        sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
        data = sqlobj.update(quary)
        print(data)
        # Return a success response
        return {'message': 'user deleted successfully!'}
    else:
        return {'message': 'No  ID provided!'}

@app.route('/add_icehrms_user', methods=['POST'])
def add_icehrms_user():
    # Retrieve form data from the POST request
    superid = request.form.get('superid')
    token = request.form.get('token')
    punchinapi = request.form.get('punchinapi')
    punchoutapi = request.form.get('punchoutapi')

    # Print the form data for debugging
    print(f'SuperId: {superid}')
    print(f'authToken: {token}')
    print(f'punchInApi: {punchinapi}')
    print(f'punchOutApi: {punchoutapi}')
    quary = f"""insert into HrmsIceHrmsSettings (superid,authtoken,punchinapi,punchoutapi)
values({superid},'{token}','{punchinapi}','{punchoutapi}')"""
    sqlobj = mysqlhelper.MySQLHelper(dbcloudrollcallSwipes)
    data = sqlobj.update(quary)
    print(data)
    # Optionally, do something with the data (e.g., save to a database)
    # Return a success message
    return redirect(url_for('IceHrmssettings'))


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
    return render_template('under-maintenance.html'), 404

# Custom 500 error handler
@app.errorhandler(500)
@login_required
def internal_server_error(error):
    return render_template('error-500.html'), 500

if __name__ == '__main__':
    app.run()
