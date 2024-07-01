from flask import Flask,render_template,request,render_template_string,url_for,redirect,session, flash
import mysqlhelper
import mssqlhelper
from datetime import datetime
from functools import wraps
from SignInCheck import verify

app = Flask(__name__)
app.secret_key = 'your_secret_keyahfdkjhdjjkjrjt7656565sal'

dbnamerollcall = 'rcalerts_Prod'
dbbookmyot = 'bookmyot'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'crmemail1' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('signin.html')
        elif request.method == 'POST':

            email = request.form['email']
            plain_password = request.form['password']
            result = verify(email,plain_password)
            # if email == '123' and str(password) == '123':
            if result['status']:
                session['crmemail1'] = email
                session['name'] = result['name']
                session['role'] = result['role']
                # flash('Login successful!', 'success')
                return redirect(url_for('indexatt'))
            else:
                # flash('Invalid credentials', 'danger')
                return render_template('signin.html')
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/logout')
def logout():
    session.pop('crmemail1', None)
    session.pop('name',None)
    session.pop('role', None)
    return redirect(url_for('login'))

def get_data_from_session():
    name = session.get('name')
    role = session.get('role')
    if role == '1':
        role = "Employee"
    elif role == '2':
        role = "Admin"
    elif role == '3':
        role = "Sales"
    elif role == '4':
        role = "Developer"
    else:
        role = role

    return {'name':name,'role':role}


@app.route('/',methods=['POST','GET'])
@login_required
def indexatt():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']

        if request.method == 'GET':
            quary = """select superid,Service,toaddr,Mailmessage,Status,createdon,message as resultResponce,bcc from MailLog 
                        order by createdon desc limit 100;"""

        elif request.method == 'POST':
            # Retrieve form data
            log_type = request.form['log_type']
            status = request.form['status']
            chosen_date = request.form['chosen_date']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")

            quary = f"""select superid,Service,toaddr,Status,createdon,Mailmessage,message as resultResponce,bcc from MailLog
                        where type = {log_type} and Status = '{status}' and createdon between '{chosen_date} 00:00:01' and 
                        '{chosen_date} 23:59:59'"""
        sqlobj = mysqlhelper.MySQLHelper()
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="NotifyLogs.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500

@app.route('/RolcallLogs' ,methods=['POST','GET'])
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

@app.route('/novotel',methods=['POST','GET'])
@login_required
def novotel():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """SELECT dateoftransaction,type,cameratype 
            FROM Novotelhealthcheck order by id desc limit 100;"""

        elif request.method == 'POST':
            cameratype = request.form['camera_type']
            chosen_date = request.form['chosen_date']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")

            quary = f"""SELECT dateoftransaction,type,cameratype FROM Novotelhealthcheck 
            where dateoftransaction between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59' and cameratype = '{cameratype}'
            order by id desc limit 100;"""

        sqlobj = mysqlhelper.MySQLHelper()
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="Novotel.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/mailtemplate', methods=['GET', 'POST'])
@login_required
def index():
    try:
        if request.method == 'POST':
            templatestring = request.form.get('templatestring', '')
            return render_template_string(templatestring)
            # return redirect(url_for('index', templatestring=templatestring))
        elif request.method == 'GET':
            return redirect(url_for('RolcallLogs'))
            # templatestring = request.args.get('templatestring', '')
            # return render_template_string(templatestring)
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/BookMyOtmailLogs', methods=['GET', 'POST'])
@login_required
def BookMyOtmailLogs():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """SELECT * FROM (SELECT p.FirstName AS username,e.title, e.Createdon, e.message FROM [dbo].[EmailNotifications] e
                        INNER JOIN Physician p ON p.id = e.PhysicianId
                        WHERE e.PhysicianId IS NOT NULL  AND e.hosid IS NULL  AND e.title IS NOT NULL
                        
                        UNION ALL
                    
                        SELECT h.name AS username, e.title, e.Createdon, e.message FROM [dbo].[EmailNotifications] e
                        INNER JOIN Hospital h ON h.id = e.hosid WHERE  e.PhysicianId IS NULL  AND e.hosid IS NOT NULL  AND e.title IS NOT NULL
                        ) AS CombinedResults ORDER BY  Createdon DESC
                        OFFSET 0 ROWS FETCH NEXT 50 ROWS ONLY;"""
        elif request.method == 'POST':
            title = request.form['title']
            chosen_date = request.form['chosen_date']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")

            quary = f"""SELECT * FROM (SELECT p.FirstName AS username,e.title, e.Createdon, e.message FROM [dbo].[EmailNotifications] e
                                    INNER JOIN Physician p ON p.id = e.PhysicianId
                                    WHERE e.PhysicianId IS NOT NULL  AND e.hosid IS NULL  AND e.title IS NOT NULL
                                    and e.Createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59' and 
                        e.title = '{title}'
                    

                                    UNION ALL

                                    SELECT h.name AS username, e.title, e.Createdon, e.message FROM [dbo].[EmailNotifications] e
                                    INNER JOIN Hospital h ON h.id = e.hosid WHERE  e.PhysicianId IS NULL  AND e.hosid IS NOT NULL  AND e.title IS NOT NULL
                                    and e.Createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59' and 
                        e.title = '{title}'
                                    ) AS CombinedResults ORDER BY  Createdon DESC
                                    OFFSET 0 ROWS FETCH NEXT 50 ROWS ONLY;"""

        sqlobj = mssqlhelper.MSSQLHelper(dbbookmyot)
        data = sqlobj.queryall(quary)

        filterquary = """select DISTINCT Title from [dbo].[EmailNotifications] where Title is not null order by title desc"""
        filter = sqlobj.queryall(filterquary)
        return render_template('main.html',htmlpage = "BookMyOtMails.html",data = data['ResultData'],filterdata = filter['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/BookMyOtMobileNotifications', methods=['GET', 'POST'])
@login_required
def BookMyOtMobileNotifications():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
                        inner join Physician p on p.id = n.PhysicianId order by n.createdon desc"""
        elif request.method == 'POST':
            chosen_date = request.form['chosen_date']
            original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
            chosen_date = original_date.strftime("%Y-%m-%d")

            quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
                        inner join Physician p on p.id = n.PhysicianId 
                        WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
                        order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(dbbookmyot)
        data = sqlobj.queryall(quary)

        return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
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
