from flask import Blueprint, render_template,url_for,redirect,session,request
from routess.signin import login_required
from utilities.utility import get_data_from_session
from Dal import  mssqlhelper

dbcampus = 'CampusManagement'
# Create a blueprint instance
Campusapp = Blueprint('Campusapp', __name__)

@Campusapp.route('/CampusAdvertisement', methods=['GET', 'POST'])
@login_required
def CampusAdvertisement():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """select top 50 superid,Title , Description,startdate,EndDate,filepath from [Campus].[OnlineComm] where type = 4 and isactive = 1
                        order by CreatedOn desc"""
        # elif request.method == 'POST':
        #     chosen_date = request.form['chosen_date']
        #     original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        #     chosen_date = original_date.strftime("%Y-%m-%d")
        #
        #     quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
        #                 inner join Physician p on p.id = n.PhysicianId
        #                 WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
        #                 order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(dbcampus)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="CampusAdvertisement.html", data=data['ResultData'], name=name, role=role)
        #return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@Campusapp.route('/campusimgs', methods=['GET', 'POST'])
@login_required
def campusimgs():
    try:
        if request.method == 'POST':
            campusimgs_path = request.form.get('campusimgs', '')
            if campusimgs_path ==None or campusimgs_path == "":
                return "images not uploded"
            external_url = f'https://pcuploadfiles.azurewebsites.net/download?path={campusimgs_path}'
            return redirect(external_url)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@Campusapp.route('/CampusAnnouncement', methods=['GET', 'POST'])
@login_required
def CampusAnnouncement():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """select top 50 superid,Title , Description,startdate,EndDate,filepath from [Campus].[OnlineComm] where type = 5 and isactive = 1
                        order by CreatedOn desc"""
        # elif request.method == 'POST':
        #     chosen_date = request.form['chosen_date']
        #     original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        #     chosen_date = original_date.strftime("%Y-%m-%d")
        #
        #     quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
        #                 inner join Physician p on p.id = n.PhysicianId
        #                 WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
        #                 order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(dbcampus)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="CampusAnnouncement.html", data=data['ResultData'], name=name, role=role)
        #return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@Campusapp.route('/CampusNotifications', methods=['GET', 'POST'])
@login_required
def CampusNotifications():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        if request.method == 'GET':
            quary = """select top 50 superid,Title , Description,startdate,EndDate from [Campus].[OnlineComm] where type = 6 and isactive = 1
                        order by CreatedOn desc"""
        # elif request.method == 'POST':
        #     chosen_date = request.form['chosen_date']
        #     original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        #     chosen_date = original_date.strftime("%Y-%m-%d")
        #
        #     quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
        #                 inner join Physician p on p.id = n.PhysicianId
        #                 WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
        #                 order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(dbcampus)
        data = sqlobj.queryall(quary)
        return render_template('main.html', htmlpage="CampusNotifications.html", data=data['ResultData'], name=name, role=role)
        #return render_template('main.html', htmlpage="BookMyOtMobileNotification.html", data=data['ResultData'],name=name,role=role)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500
