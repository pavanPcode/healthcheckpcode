from flask import Blueprint, render_template,url_for,redirect,session,request
from routess.signin import login_required
from utilities.utility import get_data_from_session
from datetime import datetime
from Dal import mssqlhelper

DBTimerJobs = 'TimerJobs'

# Create a blueprint instance
TimerJobsapp = Blueprint('TimerJobsapp', __name__)

# Function to convert date format
def convert_date_format(date_str):
    # Parse the input date in the format '15-10-2024'
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    # Convert to '2024-10-15' format
    return date_obj.strftime("%Y-%m-%d")

# def Convert_12hr_to_24hrs(time_str):
#     # Convert to 24-hour format
#
#     # If the input is in 12-hour format, convert it
#     return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

# Remove AM/PM from the time string
def Convert_12hr_to_24hrs(time_str):
    # Remove AM/PM from the time string and add seconds
    return time_str[:-3].strip() + ":00"


@TimerJobsapp.route('/getScheduleJobs', methods=['GET', 'POST'])
@login_required
def getScheduleJobs():
    try:
        session_data = get_data_from_session()
        name = session_data['name']
        role = session_data['role']
        interval_types = ["minute", "hourly","daily","weekly","monthly","yearly"]

        if request.method == 'GET':
            quary = """SELECT id timerid,[SuperId],[ProcessUrl], CAST([StartDate] AS VARCHAR(10)) AS StartDateStr,LEFT(CAST([StartTime] AS VARCHAR(20)), 8) AS StartTimeStr, 
    LEFT(CAST([EndTime] AS VARCHAR(20)), 8) AS EndTimeStr,[intervalType], 
    [Interval],[IsActive],[TimeOutSec],[Notes],[DeviceId],[Notify],[FailedAttemptstoNotify] 
FROM [dbo].[ScheduleJobs] WHERE [IsActive] = 1 order by id desc;"""
        # elif request.method == 'POST':
        #     chosen_date = request.form['chosen_date']
        #     original_date = datetime.strptime(chosen_date, "%d-%m-%Y")
        #     chosen_date = original_date.strftime("%Y-%m-%d")
        #
        #     quary = f"""select top 200 n.Title,n.message,n.createdon,p.firstname,n.PhysicianId from [dbo].[Notifications]  n
        #                 inner join Physician p on p.id = n.PhysicianId
        #                 WHERE n.createdon between '{chosen_date} 00:00:01' and '{chosen_date} 23:59:59'
        #                 order by n.createdon desc"""
        sqlobj = mssqlhelper.MSSQLHelper(DBTimerJobs)
        data = sqlobj.queryall(quary)
        print(data)
        return render_template('main.html', htmlpage="TimerjobsList.html", data=data['ResultData'],
                               name=name, role=role,interval_types=interval_types)

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


# Define the route to display the form and handle form submission
@TimerJobsapp.route('/add_timer_job', methods=['POST'])
def add_timer_job():
    try:
        if request.method == 'POST':
            # Retrieve form data
            superid = request.form.get('superid')
            date = request.form.get('date')
            time = request.form.get('time')
            starttime = request.form.get('starttime')
            endtime = request.form.get('endtime')
            process_url = request.form.get('process_url')
            interval_type = request.form.get('interval_type')
            interval = request.form.get('interval')
            notes = request.form.get('notes')
            device_id = request.form.get('device_id')
            notify = request.form.get('notify')
            failed_attempts = request.form.get('failed_attempts')
            print('failed_attempts',failed_attempts,type(failed_attempts))
            if failed_attempts =='None' or failed_attempts =='':
                failed_attempts = 0
            # Add logic to process or save the form data
            # For now, let's just print it
            print(f"Superid: {superid}, Date: {date}, Time: {time}",starttime,endtime,process_url,interval_type,interval,notes,device_id,notify,failed_attempts)
            if notify == 'on':
                notify =1
            else:
                notify =  0
            insert_ScheduleJobs_query = f"""
                INSERT INTO [dbo].[ScheduleJobs] 
                ([SuperId], [ProcessUrl], [StartDate], [StartTime], [EndTime], [intervalType], 
                [Interval],  [TimeOutSec], [Notes], [CreatedBy], [DeviceId], [Notify], [FailedAttemptstoNotify]) 
                VALUES ({superid}, '{process_url}','{convert_date_format(date)}', '{Convert_12hr_to_24hrs(starttime)}', '{Convert_12hr_to_24hrs(endtime)}',
                 '{interval_type}', '{interval}', 30, '{notes}','101',{device_id},{notify},{failed_attempts})
            """
            print(insert_ScheduleJobs_query)
            sqlobj = mssqlhelper.MSSQLHelper(DBTimerJobs)
            data = sqlobj.update(insert_ScheduleJobs_query)
            print(data)
        return redirect(url_for('TimerJobsapp.getScheduleJobs'))  # Redirect to the same form or another page

    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@TimerJobsapp.route('/edit_timer_job', methods=['POST'])
def edit_timer_job():
    try:
        if request.method == 'POST':
            # Retrieve form data
            superid = request.form.get('superid')
            date = request.form.get('date')
            time = request.form.get('time')
            starttime = request.form.get('starttime')
            endtime = request.form.get('endtime')
            process_url = request.form.get('process_url')
            interval_type = request.form.get('interval_type')
            interval = request.form.get('interval')
            notes = request.form.get('notes')
            device_id = request.form.get('device_id')
            notify = request.form.get('notify')
            failed_attempts = request.form.get('failed_attempts')
            # Add logic to process or save the form data
            # For now, let's just print it
            print(f"Superid: {superid}, Date: {date}, Time: {time}",starttime,endtime,process_url,interval_type,interval,notes,device_id,notify,failed_attempts)
            return 'suss'
    except Exception as e:
        return render_template('error-500.html', text=str(e)), 500


@TimerJobsapp.route('/delete_timer_job', methods=['POST'])
def delete_timer_job():
    # Get the timerid from the AJAX request
    timerid = request.form.get('timerjobid')

    insert_ScheduleJobs_query = f""" update  [dbo].[ScheduleJobs] set  [IsActive] = 0  WHERE id = {timerid}; """
    print(insert_ScheduleJobs_query)
    sqlobj = mssqlhelper.MSSQLHelper(DBTimerJobs)
    data = sqlobj.update(insert_ScheduleJobs_query)
    print(data,'data')
    return {'message': f'Timer job {timerid} deleted successfully.'}
