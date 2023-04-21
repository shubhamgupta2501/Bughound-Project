
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_file
from xml.etree.ElementTree import Element, SubElement, ElementTree
import pymysql.cursors
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'secret'

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'db': 'bughound',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# define a route to display the employee table
@app.route("/")
def index():
   print("login")
   return render_template("login.html")

# Login Authentication
@app.route('/', methods=['POST','GET'])
def login_auth():
    username = request.form['username']
    password = request.form['password']

    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM employees WHERE username = %s', username)
        employee = cursor.fetchone()
        if employee and employee['password'] == password:
            session['loggedin'] = True
            session['username'] = username
            session['user_level'] = employee["userlevel"]
            condition = False
            if session['user_level'] ==3:
                condition = True
            print('here')
            #return render_template('dashboard.html', condition = condition, username = username)   
            return redirect('/dashboard') 
        else:
            message = f"Incorrect username or password"
            flash(message=message)
            return redirect('/')
  

@app.route('/logout', methods=['POST','GET'])
def logout():
    if "loggedin" in session:
        message = f"You are Logged out Succesfully"
        flash(message=message)
        session.pop('loggedin', None)
    else:
        message = f"You need to Login first"
        flash(message=message)
    return redirect('/')
'''
@app.route('/header', methods=['GET'])
def header():
    username = session['username']
    userlevel =session['user_level']
    print("mmmmmm",userlevel,username)
    return render_template('header.html', username=username, userlevel=userlevel ) 
'''
# Dashboard page
@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session['username']
    userlevel =session['user_level']
    #print("pp", username,userlevel)
    condition = False
    if session['user_level'] ==3:
        condition = True
    if "loggedin" in session:
         return render_template('dashboard.html', condition = condition, username=username, userlevel=userlevel)
    else:
        message = f"You need to Login first"
        flash(message=message)
        return render_template('login.html')

@app.route('/insert', methods=['POST'])
def insert():
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        #flash("Data Inserted Successfully")
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        userlevel = request.form['userlevel']
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO employees (name, username, password, userlevel) VALUES (%s, %s, %s, %s)", (name, username, password, userlevel))
            connection.commit()
            emp_id = cursor.lastrowid
            message = f"Employee {name} was successfully added."

        flash(message=message)
        return redirect(url_for('manage_employee'))
    

@app.route('/edit', methods=['POST','GET'])
def edit():
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        emp_id = request.form['emp_id']
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        userlevel = request.form['userlevel']
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE employees SET name=%s, username=%s, password=%s, userlevel=%s WHERE emp_id=%s", (name, username, password, userlevel, emp_id))
            connection.commit()
            
            message = f"Employee {name} was successfully updated."
        
        flash(message=message)
        return redirect(url_for('manage_employee'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM employees WHERE emp_id=%s", (id_data,))
        
        connection.commit()
        message=f"Employee with id {id_data} was succesfully deleted"
    
        flash(message=message)
        return redirect(url_for('manage_employee'))
    
@app.route('/add_program', methods=['POST'])
def add_program():

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        program = request.form['program']
        program_release = request.form['release']
        program_version = request.form['version']
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO programs (program,program_release,program_version) VALUES (%s, %s, %s)", (program, program_release, program_version))
            connection.commit()
            prog_id = cursor.lastrowid
            message = f"Program {program} was successfully added."
        
        flash(message=message)
        return redirect(url_for('manage_program'))
    
@app.route('/edit_program', methods=['POST','GET'])
def edit_program():
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        prog_id = request.form['prog_id']
        program = request.form['program']
        program_release = request.form['release']
        program_version = request.form['version']
        
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE programs SET program=%s, program_release=%s, program_version=%s WHERE prog_id=%s", (program,program_release, program_version,prog_id))
            connection.commit()
            
            message = f"Program {program} was successfully updated."
        
        flash(message=message)
        return redirect(url_for('manage_employee'))

@app.route('/delete_program/<string:id_data>', methods = ['GET'])
def delete_program(id_data):

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM programs WHERE prog_id=%s", (id_data,))
        
        connection.commit()
        message=f"Program with id {id_data} was succesfully deleted"
    
        flash(message=message)
        return redirect(url_for('manage_employee'))


@app.route('/add_area', methods=['POST'])
def add_area():

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        print(request.form)
        area = request.form['area']
        
        prog_id = request.form['prog_id']
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM programs")
            result = cursor.fetchone()
            print(result['COUNT(*)'])
            connection.commit()
            '''


            cursor.execute("SELECT prog_id FROM programs where program=%s",(program,))
            prog_id = cursor.fetchone()
            print(prog_id)
            '''



            if result['COUNT(*)'] == 0:
                message="Cannot add area - programs table is empty."
            else:
                print(area, prog_id)
                cursor.execute("INSERT INTO areas (area,prog_id) VALUES (%s, %s)", (area, prog_id))
                connection.commit()
                prog_id = cursor.lastrowid
                message = f"Area {area} was successfully added."


        flash(message=message)
        return redirect(url_for('manage_area'))
    
@app.route('/edit_area', methods=['POST','GET'])
def edit_area():
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        prog_id = request.form['prog_id']
        area = request.form['area']
        area_id = request.form['area_id']
       
        
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("UPDATE areas SET area=%s, prog_id=%s WHERE area_id=%s", (area,prog_id, area_id))
            connection.commit()
            
            message = f"Areas {area} was successfully updated."
       
        flash(message=message)
        return redirect(url_for('manage_area'))

@app.route('/delete_area/<string:id_data>', methods = ['GET'])
def delete_area(id_data):

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM areas WHERE area_id=%s", (id_data,))
        
        connection.commit()
        message=f"Area with id {id_data} was succesfully deleted"
    
        flash(message=message)
        return redirect(url_for('manage_area'))


# Add/Update Bugs page
@app.route('/update_bug')
def update_bug():
    username = session['username']
    userlevel =session['user_level']

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    report_types = ['coding error', 'design error', 'hardware error', 'suggestion', 'Documentation', 'Query']
    severities = ['fatal', 'severe', 'minor']
    #employees = ['employee1', 'employee2', 'employee3'] # replace with actual employee list
    #areas = ['area1', 'area2', 'area3'] # replace with actual area list
    priority=[1,2,3,4,5,6]
    status=['Open', 'Closed', 'Resolved']
    resolution=['Pending', 'Fixed', 'Irreproducible', 'Deferred', 'As designed', 'Withdrawn by reporter', 'Need more info', 'Disagree with suggestion', 'Duplicate']
    resolution_version=[1,2,3,4]
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM bug')
        data = cursor.fetchall()
        connection.commit()


        cursor.execute('SELECT * FROM programs')
        programs = cursor.fetchall()
        connection.commit()

        cursor.execute('SELECT * FROM areas')
        areas = cursor.fetchall()
        connection.commit()

        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        connection.commit()

        print(data)
    
    return render_template('update_bug.html',username=username,userlevel=userlevel, bugs=data, programs=programs, report_types=report_types, severities=severities, employees=employees, areas=areas, resolution=resolution, resolution_version=resolution_version, priority=priority, status=status)

@app.route('/delete_bug/<string:id_data>', methods = ['GET'])
def delete_bug(id_data):

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM bug WHERE bug_id=%s", (id_data,))
        
        connection.commit()
        message=f"Bug with id {id_data} was succesfully deleted"
    
        flash(message=message)
        return redirect(url_for('update_bug'))




@app.route('/edit_bug', methods=['POST','GET'])
def edit_bug():
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == "POST":
        print(request.form)
        bug_id = request.form.get('bug_id')
        
        program = request.form.get('program')
        report_type = request.form.get('report_type')
        severity = request.form.get('severity')
        problem_summary = request.form.get('problem_summary')
        reproducible = request.form.get('reproducible')
        problem = request.form.get('problem')
        reported_by = request.form.get('reported_by')
        date_reported = request.form.get('date_reported')
        functional_area = request.form.get('functional_area')
        assigned_to = request.form.get('assigned_to')
        comments = request.form.get('comments')
        status = request.form.get('status')
        priority = request.form.get('priority')
        resolution = request.form.get('resolution')
        resolution_version = request.form.get('resolution_version')
        resolution_by = request.form.get('resolution_by')
        date_resolved = request.form.get('date_resolved')
        tested_by = request.form.get('tested_by')
        
        # Get the file attachment from the form
        attachment = request.files["attachment"]
        # Get the filename of the attachment
        file_name = attachment.filename

        # Read the contents of the file
        attachment = attachment.read()
        
    
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT prog_id FROM programs WHERE program=%s", (program,))
            prog_id = cursor.fetchone()
        
            connection.commit()

            cursor.execute("SELECT area_id FROM areas WHERE area=%s", (functional_area,))
            area_id = cursor.fetchone()
        
            connection.commit()
            print("UPDATE bug SET program=%s, report_type=%s, severity=%s, problem_summary=%s, reproducible=%s, problem=%s, reported_by=%s, date_reported=%s, functional_area=%s, assigned_to=%s, comments=%s, status=%s, priority=%s, resolution=%s, resolution_version=%s, resolution_by=%s, date_resolved=%s, tested_by=%s, prog_id=%s, area_id=%s, attachment=%s, filename=%s WHERE bug_id=%s", (program, report_type, severity, 
                                            problem_summary, reproducible, problem, reported_by, 
                                            date_reported, functional_area, assigned_to, comments, 
                                            status, priority, resolution, resolution_version, resolution_by,
                                            date_resolved, tested_by, prog_id['prog_id'], area_id['area_id'], attachment, file_name, bug_id))
            cursor.execute("UPDATE bug SET program=%s, report_type=%s, severity=%s, problem_summary=%s, reproducible=%s, problem=%s, reported_by=%s, date_reported=%s, functional_area=%s, assigned_to=%s, comments=%s, status=%s, priority=%s, resolution=%s, resolution_version=%s, resolution_by=%s, date_resolved=%s, tested_by=%s, prog_id=%s, area_id=%s, attachment=%s, filename=%s WHERE bug_id=%s", (program, report_type, severity, 
                                            problem_summary, reproducible, problem, reported_by, 
                                            date_reported, functional_area, assigned_to, comments, 
                                            status, priority, resolution, resolution_version, resolution_by,
                                            date_resolved, tested_by, prog_id['prog_id'], area_id['area_id'], attachment,file_name, bug_id))
            connection.commit()
            
            message = f"Bug with name {program} was successfully updated."
        
        flash(message=message)
        return redirect(url_for('update_bug'))


#add Bugs Page
@app.route('/add_bug', methods=['GET', 'POST'])
def add_bug():
    username = session['username']
    userlevel =session['user_level']
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == 'POST':
        program = request.form.get('program')
        report_type = request.form.get('report_type')
        severity = request.form.get('severity')
        problem_summary = request.form.get('problem_summary')
        reproducible = request.form.get('reproducible')
        problem = request.form.get('problem')
        reported_by = request.form.get('reported_by')
        date_reported = request.form.get('date_reported')
        functional_area = request.form.get('functional_area')
        assigned_to = request.form.get('assigned_to')
        comments = request.form.get('comments')
        status = request.form.get('status')
        priority = request.form.get('priority')
        resolution = request.form.get('resolution')
        resolution_version = request.form.get('resolution_version')
        resolution_by = request.form.get('resolution_by')
        date_resolved = request.form.get('date_resolved')
        tested_by = request.form.get('tested_by')
        
        # Get the file attachment from the form
        attachment = request.files["attachment"]
        # Get the filename of the attachment
        file_name = attachment.filename

        # Read the contents of the file
        attachment = attachment.read()
        
        

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            

            cursor.execute("SELECT prog_id FROM programs WHERE program=%s", (program,))
            prog_id = cursor.fetchone()
        
            connection.commit()

            cursor.execute("SELECT area_id FROM areas WHERE area=%s", (functional_area,))
            area_id = cursor.fetchone()
        
            connection.commit()

            
            print("INSERT INTO bug (program, report_type, severity, problem_summary, reproducible, problem, reported_by, date_reported, functional_area, assigned_to, comments, status, priority, resolution, resolution_version, resolution_by,date_resolved, tested_by, prog_id, area_id, attachment, filename) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)", (program, report_type, severity, 
                                            problem_summary, reproducible, problem, reported_by, 
                                            date_reported, functional_area, assigned_to, comments, 
                                            status, priority, resolution, resolution_version, resolution_by,
                                            date_resolved, tested_by, prog_id['prog_id'], area_id['area_id'], attachment, file_name))
            cursor.execute("INSERT INTO bug (program, report_type, severity, problem_summary, reproducible, problem, reported_by, date_reported, functional_area, assigned_to, comments, status, priority, resolution, resolution_version, resolution_by,date_resolved, tested_by, prog_id, area_id, attachment, filename) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)", (program, report_type, severity, 
                                            problem_summary, reproducible, problem, reported_by, 
                                            date_reported, functional_area, assigned_to, comments, 
                                            status, priority, resolution, resolution_version, resolution_by,
                                            date_resolved, tested_by, prog_id['prog_id'], area_id['area_id'], attachment, file_name))
            connection.commit()
            
            bug_id= cursor.lastrowid
            message = f"Bug with id {bug_id} was successfully added."
        
        
        # process the form data and store it in the database using PL/SQL
        
        # redirect to a success page
        flash(message=message)
        return redirect(url_for('add_bug'))

    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM programs')
        programs = cursor.fetchall()
        connection.commit()

        cursor.execute('SELECT * FROM areas')
        areas = cursor.fetchall()
        connection.commit()

        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        connection.commit()
    # if the request method is GET, render the add_bug page with the necessary form data
    #programs = programs # replace with actual program list
    report_types = ['coding error', 'design error', 'hardware error', 'suggestion', 'Documentation', 'Query']
    severities = ['fatal', 'severe', 'minor']
    #employees = ['employee1', 'employee2', 'employee3'] # replace with actual employee list
    #areas = ['area1', 'area2', 'area3'] # replace with actual area list
    priority=[1,2,3,4,5,6]
    status=['Open', 'Closed', 'Resolved']
    resolution=['Pending', 'Fixed', 'Irreproducible', 'Deferred', 'As designed', 'Withdrawn by reporter', 'Need more info', 'Disagree with suggestion', 'Duplicate']
    resolution_version=[1,2,3,4]
    return render_template('add_bug.html', programs=programs, report_types=report_types, severities=severities, employees=employees, areas=areas, resolution=resolution, resolution_version=resolution_version, priority=priority, status=status, username=username, userlevel=userlevel)

# Maintain Database page
@app.route('/maintain_database')
def maintain_database():
    username = session['username']
    userlevel =session['user_level']
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    

    if session['user_level'] != 3:
        condition = False
        return render_template('dashboard.html', condition = condition, username=username, userlevel=userlevel)
    
    return render_template('maintain_database.html', username=username, userlevel=userlevel)

# manage employee page
@app.route('/manage_employee')
def manage_employee():
    username = session['username']
    userlevel =session['user_level']
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
     

    if session['user_level'] != 3:
        condition = False
        return render_template('dashboard.html', condition = condition, username=username, userlevel=userlevel)
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM employees')
        data = cursor.fetchall()
        connection.commit()
     
        return render_template('manage_employee.html', employees=data, username=username, userlevel=userlevel)

# manage program page
@app.route('/manage_program')
def manage_program():
    username = session['username']
    userlevel =session['user_level']
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if session['user_level'] != 3:
        condition = False
        return render_template('dashboard.html', condition = condition, username=username, userlevel=userlevel)
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM programs')
        data = cursor.fetchall()
        connection.commit()
     
        return render_template('manage_program.html', program=data, username=username, userlevel=userlevel)

# manage area page
@app.route('/manage_area')
def manage_area():
    username = session['username']
    userlevel =session['user_level']
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if session['user_level'] != 3:
        condition = False
        return render_template('dashboard.html', condition = condition, username=username, userlevel=userlevel)
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM areas')
        data = cursor.fetchall()
        connection.commit()
        cursor.execute('SELECT * FROM programs')
        programs = cursor.fetchall()
        connection.commit()
    return render_template('manage_area.html', areas=data, programs=programs, username=username, userlevel=userlevel)

@app.route('/update',methods=['POST','GET'])
def update():
    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')

    return redirect(url_for('manage_employee'))


#add Bugs Page
@app.route('/search_bug', methods=['GET', 'POST'])
def search_bug():
    username = session['username']
    userlevel =session['user_level']

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if request.method == 'POST':
        field_values={
        'program': request.form.get('program'),
        'report_type': request.form.get('report_type'),
        'severity': request.form.get('severity'),
        'problem_summary': request.form.get('problem_summary'),
        'reproducible': request.form.get('reproducible'),
        'problem': request.form.get('problem'),
        'reported_by': request.form.get('reported_by'),
        'date_reported': request.form.get('date_reported'),
        'functional_area': request.form.get('functional_area'),
        'assigned_to': request.form.get('assigned_to'),
        'comments': request.form.get('comments'),
        'status': request.form.get('status'),
        'priority': request.form.get('priority'),
        'resolution': request.form.get('resolution'),
        'resolution_version': request.form.get('resolution_version'),
        'resolution_by': request.form.get('resolution_by'),
        'date_resolved': request.form.get('date_resolved'),
        'tested_by': request.form.get('tested_by')
        }
        print(field_values)
        if field_values['date_reported']=='':
            field_values['date_reported']=None

        # build the SQL query based on user inputs
        sql = "SELECT * FROM bug"
        conditions = []
        for field, value in field_values.items():
            if value!=None:
                conditions.append(f"{field} = '{value}'")
            

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
       


        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            print(sql)
            cursor.execute(sql)
            search_result=cursor.fetchall()
            print(search_result)
            connection.commit()

            cursor.execute('SELECT * FROM programs')
            programs = cursor.fetchall()
            connection.commit()

            cursor.execute('SELECT * FROM areas')
            areas = cursor.fetchall()
            connection.commit()

            cursor.execute('SELECT * FROM employees')
            employees = cursor.fetchall()
            connection.commit()
        # if the request method is GET, render the add_bug page with the necessary form data
        #programs = programs # replace with actual program list
        report_types = ['coding error', 'design error', 'hardware error', 'suggestion', 'Documentation', 'Query']
        severities = ['fatal', 'severe', 'minor']
        #employees = ['employee1', 'employee2', 'employee3'] # replace with actual employee list
        #areas = ['area1', 'area2', 'area3'] # replace with actual area list
        priority=[1,2,3,4,5,6]
        status=['Open', 'Closed', 'Resolved']
        resolution=['Pending', 'Fixed', 'Irreproducible', 'Deferred', 'As designed', 'Withdrawn by reporter', 'Need more info', 'Disagree with suggestion', 'Duplicate']
        resolution_version=[1,2,3,4]


        

        
        # process the form data and store it in the database using PL/SQL
        
        # redirect to a success page
        return render_template('search_bug_result.html', result=search_result, username=username, userlevel=userlevel,programs=programs, report_types=report_types, severities=severities, employees=employees, areas=areas, resolution=resolution, resolution_version=resolution_version, priority=priority, status=status)
    
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM programs')
        programs = cursor.fetchall()
        connection.commit()

        cursor.execute('SELECT * FROM areas')
        areas = cursor.fetchall()
        connection.commit()

        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        connection.commit()
    # if the request method is GET, render the add_bug page with the necessary form data
    #programs = programs # replace with actual program list
    report_types = ['coding error', 'design error', 'hardware error', 'suggestion', 'Documentation', 'Query']
    severities = ['fatal', 'severe', 'minor']
    #employees = ['employee1', 'employee2', 'employee3'] # replace with actual employee list
    #areas = ['area1', 'area2', 'area3'] # replace with actual area list
    priority=[1,2,3,4,5,6]
    status=['Open', 'Closed', 'Resolved']
    resolution=['Pending', 'Fixed', 'Irreproducible', 'Deferred', 'As designed', 'Withdrawn by reporter', 'Need more info', 'Disagree with suggestion', 'Duplicate']
    resolution_version=[1,2,3,4]
    return render_template('search_bug_page.html', programs=programs, report_types=report_types, severities=severities, employees=employees, areas=areas, resolution=resolution, resolution_version=resolution_version, priority=priority, status=status, username=username, userlevel=userlevel)

@app.route("/view_attachment/<string:filename>")
def view_attachment(filename):
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        cursor.execute("SELECT attachment FROM bug WHERE filename = %s", (filename,))

        data = cursor.fetchone()
        print(data)
        

    return send_file(BytesIO(data['attachment']), attachment_filename=filename, as_attachment=True)




# export data
@app.route('/export_data', methods=['GET', 'POST'])
def export_data():

    if "loggedin" not in session:
         message = f"You need to Login first"
         flash(message=message)
         return render_template('login.html')
    
    if session['user_level'] != 3:
        condition = False
        return render_template('dashboard.html', condition = condition)
    
    if request.method == 'POST':
        table_name = request.form['table_name']
        data_type = request.form['data_type']
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            

            cursor.execute(f'SELECT * FROM {table_name}')
            rows = cursor.fetchall()
            # create a root element for the XML file
            root = Element(table_name)
            
            # iterate over the rows and create subelements for each record
            for row in rows:
                record = SubElement(root, "record")
                for key, value in row.items():
                    field = SubElement(record, key)
                    field.text = str(value)
            
            # generate the XML file and save it to disk
            tree = ElementTree(root)
            if data_type == "xml":
                tree.write(f"{table_name}.xml", encoding="utf-8", xml_declaration=True)
            elif data_type == "ascii":
                with open(f"{table_name}.txt", "w") as f:
                    for row in rows:
                        for key, value in row.items():
                            f.write(f"{key}: {value}\n")
                        f.write("\n")
            else:
                print("Invalid data type")
            
            # close the database connection
            cursor.close()
            connection.close()
            message = f"Table {table_name} with type {data_type} was successfully exported."
            flash(message=message)
            return redirect(url_for('export_data'))


    return render_template('export_data.html')


if __name__ == "__main__":
    app.run(debug=True)

