from flask import Flask,render_template,request
import mysqlhelper
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def indexatt():
    try:
        quary = "select superid,Service,toaddr,Mailmessage,Status,createdon,message as resultResponce,bcc from MailLog;"
        sqlobj = mysqlhelper.MySQLHelper()
        data = sqlobj.queryall(quary)
        print(data)
        return  render_template('sales-list - Copy.html', data=data)
    except Exception as e:
        # Simulate a server error (e.g., database connection error)
        return render_template('error-500.html', text=str(e)), 500


# Define route to handle form submission
@app.route('/process_filter', methods=['POST'])
def process_filter():
    try :
        # Retrieve form data
        log_type = request.form['log_type']
        status = request.form['status']
        chosen_date = request.form['chosen_date']
        print(request.form)
        print(f"Log Type: {log_type}, Status: {status}, Chosen Date: {chosen_date}")
        original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        # Format the datetime object into "yyyy-dd-mm" format
        chosen_date = original_date.strftime("%Y-%m-%d")

        quary = f"""select superid,Service,toaddr,Status,createdon,Mailmessage,message as resultResponce,bcc from MailLog
                    where type = {log_type} and Status = '{status}' and createdon between '{chosen_date} 00:00:01' and 
                    '{chosen_date} 23:59:59'"""
        sqlobj = mysqlhelper.MySQLHelper()
        data = sqlobj.queryall(quary)
        return render_template('sales-list - Copy.html', data=data)

    except Exception as e:
        # Simulate a server error (e.g., database connection error)
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
