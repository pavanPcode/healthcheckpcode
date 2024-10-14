from flask import Blueprint, render_template,url_for,redirect,session,request
from routess.signin import login_required
from utilities.utility import get_data_from_session
from datetime import datetime
from Dal import mssqlhelper

dbbookmyot = 'bookmyot'

# Create a blueprint instance
bookmyotapp = Blueprint('bookmyotapp', __name__)


@bookmyotapp.route('/BookMyOtmailLogs', methods=['GET', 'POST'])
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
        return render_template('main.html', htmlpage="BookMyOtMails.html", data=data['ResultData'],
                               filterdata=filter['ResultData'], name=name, role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@bookmyotapp.route('/BookMyOtMobileNotifications', methods=['GET', 'POST'])
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

        return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],
                               name=name, role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500
