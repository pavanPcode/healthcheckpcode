from flask import Blueprint, render_template,url_for,redirect,session,request
from routess.signin import login_required
from utilities.utility import get_data_from_session
from datetime import datetime
from Dal import mysqlhelper

HealthCheck_Prod = 'HealthCheck_Prod'
# Create a blueprint instance
Notifyapp = Blueprint('Notifyapp', __name__)

@Notifyapp.route('/',methods=['POST','GET'])
@login_required
def indexatt():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        if request.method == 'GET':
            quary = """select superid,Service,toaddr,Mailmessage,Status,createdon,message as resultResponce,bcc,message from MailLog 
                        order by createdon desc limit 100;"""

        elif request.method == 'POST':
            # Retrieve form data
            log_type = request.form['log_type']
            status = request.form['status']
            chosen_date = request.form['chosen_date']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")

            quary = f"""select superid,Service,toaddr,Status,createdon,Mailmessage,message as resultResponce,bcc,message from MailLog
                        where type = {log_type} and Status = '{status}' and createdon between '{chosen_date} 00:00:01' and 
                        '{chosen_date} 23:59:59'"""
        sqlobj = mysqlhelper.MySQLHelper(HealthCheck_Prod)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="NotifyLogs.html", data=data['ResultData'],name=name,role=role)
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500
