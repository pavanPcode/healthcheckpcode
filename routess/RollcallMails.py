from flask import Blueprint,render_template,request,render_template_string,url_for,redirect
from Dal import  mssqlhelper
from routess.signin import login_required
from utilities.utility import get_data_from_session
from datetime import datetime

dbnamerollcall = 'rcalerts_Prod'
# Create a blueprint instance
Rollcallmailsapp = Blueprint('Rollcallmailsapp', __name__)

@Rollcallmailsapp.route('/mailtemplate', methods=['GET', 'POST'])
@login_required
def index():
    try:
        if request.method == 'POST':
            templatestring = request.form.get('templatestring', '')
            return render_template_string(templatestring)
            # return redirect(url_for('index', templatestring=templatestring))
        elif request.method == 'GET':
            return redirect(url_for('Rollcallmailsapp.RolcallLogs'))
            # templatestring = request.args.get('templatestring', '')
            # return render_template_string(templatestring)
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@Rollcallmailsapp.route('/RolcallLogs' ,methods=['POST','GET'])
@login_required
def RolcallLogs():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        if request.method == 'GET':
            quary = """select top 150  id,superid,ToEmail toaddr,Subjectemail,createdon,ccemail,BodyEmail  from  
            [PROD].[EmailAlerts] order by createdon desc;"""

        elif request.method == 'POST':
            # Retrieve form data
            Subjectemail = request.form['Subjectemail']
            chosen_date = request.form['chosen_date']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")

            quary = f"""select  id,superid,ToEmail toaddr,Subjectemail,createdon,ccemail,BodyEmail from [PROD].[EmailAlerts] 
                        where Subjectemail = '{Subjectemail}' and createdon 
                        between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'"""

        sqlobj = mssqlhelper.MSSQLHelper(dbnamerollcall)
        data = sqlobj.queryall(quary)
        filterquary = """SELECT DISTINCT Subjectemail FROM      [PROD].[EmailAlerts]"""
        filter = sqlobj.queryall(filterquary)
        return render_template('main.html',htmlpage = "RollCallLogs.html",data = data['ResultData'],filterdata = filter['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500
