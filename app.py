from flask import Flask, render_template, request, redirect, session, url_for
from database import db, User, Student

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin123', role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()
        if user:
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = Student.query.all()
    total_students = len(students)
    passed = sum(1 for s in students if s.status() == 'Pass')
    failed = total_students - passed
    return render_template('dashboard.html',
        students=students,
        total=total_students,
        passed=passed,
        failed=failed,
        role=session['role']
    )

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        s = Student(
            name=request.form['name'],
            roll_number=request.form['roll'],
            tamil=float(request.form['tamil']),
            english=float(request.form['english']),
            maths=float(request.form['maths']),
            science=float(request.form['science']),
            social=float(request.form['social'])
        )
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/delete/<int:id>')
def delete_student(id):
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))
    s = Student.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)