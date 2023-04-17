from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Hardcoded User Credentials
USERNAME = "admin"
PASSWORD = "password"

# define a route to display the employee table
@app.route("/")
def index():
    return render_template("login.html")

# Dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Add/Update Bugs page
@app.route('/update_bug')
def update_bug():
    return render_template('update_bug.html')

#add Bugs Page
@app.route('/add_bug', methods=['GET', 'POST'])
def add_bug():
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
        resolved_by = request.form.get('resolved_by')
        date_resolved = request.form.get('date_resolved')
        tested_by = request.form.get('tested_by')
        treat_as = request.form.get('treat_as')
        
        # process the form data and store it in the database using PL/SQL
        
        # redirect to a success page
        return render_template('add_bug_success.html')
    
    # if the request method is GET, render the add_bug page with the necessary form data
    programs = ['program1', 'program2', 'program3'] # replace with actual program list
    report_types = ['coding error', 'design error', 'hardware error', 'suggestion']
    severities = ['fatal', 'severe', 'minor']
    employees = ['employee1', 'employee2', 'employee3'] # replace with actual employee list
    areas = ['area1', 'area2', 'area3'] # replace with actual area list
    
    return render_template('add_bug.html', programs=programs, report_types=report_types, severities=severities, employees=employees, areas=areas)

#add Bugs Page
@app.route('/search_bug', methods=['GET', 'POST'])
def search_bug():
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
        resolved_by = request.form.get('resolved_by')
        date_resolved = request.form.get('date_resolved')
        tested_by = request.form.get('tested_by')
        treat_as = request.form.get('treat_as')
        
        # process the form data and store it in the database using PL/SQL
        
        # redirect to a success page
        return render_template('add_bug_success.html')
    
    # if the request method is GET, render the add_bug page with the necessary form data
    programs = ['program1', 'program2', 'program3'] # replace with actual program list
    report_types = ['coding error', 'design error', 'hardware error', 'suggestion']
    severities = ['fatal', 'severe', 'minor']
    employees = ['employee1', 'employee2', 'employee3'] # replace with actual employee list
    areas = ['area1', 'area2', 'area3'] # replace with actual area list
    
    return render_template('search_bug_page.html', programs=programs, report_types=report_types, severities=severities, employees=employees, areas=areas)

# Maintain Database page
@app.route('/maintain_database')
def maintain_database():
    return render_template('maintain_database.html')

# manage employee page
@app.route('/manage_employee')
def manage_employee():
    return render_template('manage_employee.html')

# manage program page
@app.route('/manage_program')
def manage_program():
    return render_template('manage_program.html')

# manage area page
@app.route('/manage_area')
def manage_area():
    return render_template('manage_area.html')

# manage area page
@app.route('/export_data')
def export_data():
    return render_template('export_data.html')

# Login Authentication
@app.route('/', methods=['POST'])
def login_auth():
    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/update',methods=['POST','GET'])
def update():
    return redirect(url_for('manage_employee'))

if __name__ == "__main__":
    app.run(debug=True)
