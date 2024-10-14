from flask import Blueprint, render_template,url_for,redirect,session,request
from routess.signin import login_required
from utilities.utility import get_data_from_session
from Dal import mysqlhelper
from datetime import datetime
HealthCheck_Prod = 'HealthCheck_Prod'
# Create a blueprint instance
Novotelapp = Blueprint('Novotelapp', __name__)

@Novotelapp.route('/novotel',methods=['POST','GET'])
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

        sqlobj = mysqlhelper.MySQLHelper(HealthCheck_Prod)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="Novotel.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500
