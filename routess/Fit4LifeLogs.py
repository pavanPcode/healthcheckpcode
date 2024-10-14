from flask import Blueprint, render_template,url_for,redirect,session,request
from routess.signin import login_required
from utilities.utility import get_data_from_session
from Dal import  mssqlhelper

Fit4Life = "Fit4Life"
# Create a blueprint instance
Fit4Lifeapp = Blueprint('Fit4Lifeapp', __name__)

@Fit4Lifeapp.route('/Fit4LifeReminders', methods=['GET', 'POST'])
@login_required
def Fit4LifeReminders():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """select top 50 cus.Name,rem.OperatingDate ,cus.EmailAddr,cus.Mobile,rem.apptid from Customers cus
inner join reminders rem on rem.Customerid = cus.id
order by rem.CreatedOn desc"""
        # elif request.method == 'POST':
        #     chosen_date = request.form['chosen_date']
        #     original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        #     chosen_date = original_date.strftime("%Y-%m-%d")
        #
        #     quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
        #                 inner join Physician p on p.id = n.PhysicianId
        #                 WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
        #                 order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(Fit4Life)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="Fit4LifeReminders.html", data=data['ResultData'], name=name, role=role)
        #return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@Fit4Lifeapp.route('/Fit4LifeAppt', methods=['GET', 'POST'])
@login_required
def Fit4LifeAppt():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """SELECT top 50  customername,ApppointmentDt,StartTime,Endtime,Status,Mobile,CreatedOn FROM appointments order by id desc"""
        # elif request.method == 'POST':
        #     chosen_date = request.form['chosen_date']
        #     original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        #     chosen_date = original_date.strftime("%Y-%m-%d")
        #
        #     quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
        #                 inner join Physician p on p.id = n.PhysicianId
        #                 WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
        #                 order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(Fit4Life)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="Fit4LifeAppt.html", data=data['ResultData'], name=name, role=role)
        #return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500
