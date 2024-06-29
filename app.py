from flask import Flask,render_template,request,render_template_string,url_for,redirect
import mysqlhelper
import mssqlhelper
from datetime import datetime

app = Flask(__name__)

dbnamerollcall = 'rcalerts_Prod'
dbbookmyot = 'bookmyot'

@app.route('/',methods=['POST','GET'])
def indexatt():
    try:
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
        return render_template('main.html', htmlpage="NotifyLogs.html", data=data['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500

@app.route('/RolcallLogs' ,methods=['POST','GET'])
def RolcallLogs():
    try:
        if request.method == 'GET':
            quary = """select top 100  id,superid,ToEmail toaddr,Subjectemail,createdon,ccemail,BodyEmail  from  
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

        return render_template('main.html',htmlpage = "RollCallLogs.html",data = data['ResultData'],filterdata = filter['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500

@app.route('/novotel',methods=['POST','GET'])
def novotel():
    try:
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
        return render_template('main.html', htmlpage="Novotel.html", data=data['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/mailtemplate', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            templatestring = request.form.get('templatestring', '')
            return redirect(url_for('index', templatestring=templatestring))
        elif request.method == 'GET':
            templatestring = request.args.get('templatestring', '')
            return render_template_string(templatestring)
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':

            return render_template('signin.html')
        return render_template('signin.html')

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500

@app.route('/BookMyOtmailLogs', methods=['GET', 'POST'])
def BookMyOtmailLogs():
    try:
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
        return render_template('main.html',htmlpage = "BookMyOtMails.html",data = data['ResultData'],filterdata = filter['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/BookMyOtMobileNotifications', methods=['GET', 'POST'])
def BookMyOtMobileNotifications():
    try:
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
        print(quary)
        sqlobj = mssqlhelper.MSSQLHelper(dbbookmyot)
        data = sqlobj.queryall(quary)
        print(data)

        return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('under-maintenance.html'), 404

# Custom 500 error handler
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error-500.html'), 500

if __name__ == '__main__':
    app.run()
