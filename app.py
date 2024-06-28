from flask import Flask,render_template,request,render_template_string
import mysqlhelper
import mssqlhelper
from datetime import datetime

app = Flask(__name__)

dbnamerollcall = 'rcalerts_Prod'
dbbookmyot = 'bookmyot'

@app.route('/')
def indexatt():
    try:
        quary = """select superid,Service,toaddr,Mailmessage,Status,createdon,message as resultResponce,bcc from MailLog 
                    order by createdon desc limit 100;"""
        sqlobj = mysqlhelper.MySQLHelper()
        data = sqlobj.queryall(quary)
        #if data['Status'] ==True:
        return render_template('main.html',htmlpage = "NotifyLogs.html",data = data['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/process_filter', methods=['POST'])
def process_filter():
    try :
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
        return render_template('main.html',htmlpage = "NotifyLogs.html", data=data['ResultData'])

    except Exception as e:
        # Simulate a server error (e.g., database connection error)
        return render_template('error-500.html', text=str(e)), 500



@app.route('/RolcallLogs')
def RolcallLogs():
    try:
        quary = """select top 100  id,superid,ToEmail toaddr,Subjectemail,createdon,ccemail,BodyEmail  from  
        [PROD].[EmailAlerts] order by createdon desc;"""
        sqlobj = mssqlhelper.MSSQLHelper(dbnamerollcall)
        data = sqlobj.queryall(quary)
        print(data)

        filterquary = """SELECT DISTINCT Subjectemail FROM      [PROD].[EmailAlerts]"""
        filter = sqlobj.queryall(filterquary)

        #if data['Status'] ==True:
        return render_template('main.html',htmlpage = "RollCallLogs.html",data = data['ResultData'],filterdata = filter['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500



@app.route('/RollCall_filter', methods=['POST'])
def RollCall_filter():
    try :
        # Retrieve form data
        Subjectemail = request.form['Subjectemail']
        chosen_date = request.form['chosen_date']
        original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        chosen_date = original_date.strftime("%Y-%m-%d")

        quary = f"""select  id,superid,ToEmail toaddr,Subjectemail,createdon,ccemail,BodyEmail 
                    from [PROD].[EmailAlerts] 
                    where Subjectemail = '{Subjectemail}' and createdon 
                    between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'"""
        sqlobj = mssqlhelper.MSSQLHelper(dbnamerollcall)
        data = sqlobj.queryall(quary)
        filterquary = """SELECT DISTINCT Subjectemail FROM      [PROD].[EmailAlerts]"""
        filter = sqlobj.queryall(filterquary)

        #if data['Status'] == True:
        return render_template('main.html', htmlpage="RollCallLogs.html", data=data['ResultData'],
                                   filterdata=filter['ResultData'])


    except Exception as e:
        # Simulate a server error (e.g., database connection error)
        return render_template('error-500.html', text=str(e)), 500


@app.route('/novotel')
def novotel():
    try:
        quary = """SELECT Entrycount,exitcount,inandouttotal,inandoutfind,dateoftransaction,type,cameratype 
        FROM Novotelhealthcheck order by id desc limit 50;"""
        sqlobj = mysqlhelper.MySQLHelper()
        data = sqlobj.queryall(quary)
        if data['Status'] ==True:
            return render_template('main.html',htmlpage = "Novotel.html",data = data['ResultData'])

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@app.route('/mailtemplate', methods=['GET', 'POST'])
def index():
    templatestring = request.form.get('templatestring', '')
    return render_template_string(templatestring)




@app.route('/BookMyOtLogs')
def BookMyOtLogs():
    try:
        quary = """SELECT * FROM (
    SELECT 
        p.FirstName AS username,
        e.title, 
        e.Createdon, 
        e.message 
    FROM 
        [dbo].[EmailNotifications] e
    INNER JOIN 
        Physician p ON p.id = e.PhysicianId
    WHERE 
        e.PhysicianId IS NOT NULL  
        AND e.hosid IS NULL  
        AND e.title IS NOT NULL

    UNION ALL

    SELECT 
        h.name AS username, 
        e.title, 
        e.Createdon, 
        e.message 
    FROM 
        [dbo].[EmailNotifications] e
    INNER JOIN 
        Hospital h ON h.id = e.hosid
    WHERE  
        e.PhysicianId IS NULL  
        AND e.hosid IS NOT NULL  
        AND e.title IS NOT NULL
) AS CombinedResults
ORDER BY 
    Createdon DESC
OFFSET 0 ROWS FETCH NEXT 50 ROWS ONLY;"""
        sqlobj = mssqlhelper.MSSQLHelper(dbbookmyot)
        data = sqlobj.queryall(quary)
        print(data)

        # filterquary = """SELECT DISTINCT Subjectemail FROM      [PROD].[EmailAlerts]"""
        # filter = sqlobj.queryall(filterquary)
        # filter = [('Hospitals',),('Physicians')]
        filter = []

        #if data['Status'] ==True:
        return render_template('main.html',htmlpage = "BookMyOtLogs.html",data = data['ResultData'],filterdata = filter)

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
