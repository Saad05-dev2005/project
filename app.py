from flask import Flask, abort, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import abort
from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, PasswordField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, input_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    projects = db.relationship('Project', backref='owner', lazy=True)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)
    
    @property
    def progress(self):
            if not self.tasks:
                return 0
            completed_tasks = sum(1 for task in self.tasks if task.status == 'completed')
            return int((completed_tasks / len(self.tasks)) * 100) 
    
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[Length(max=150)])
    last_name = StringField('Last Name', validators=[Length(max=150)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    submit = SubmitField('Register')
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already exists. Please choose a different one.')
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered. Please choose a different one.')

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    assign_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Project')  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[], default=None)
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')
    description = TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Add Task')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Registration successful!", "success")
        return redirect(url_for('dashboard'))
    else:
        if request.method == "POST":
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field.capitalize()} - {error}", "danger")
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:logout_user()
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter((User.email==login_input) | (User.username==login_input)).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid login credentials. Please try again.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')
                           
@app.route('/dashboard')
@login_required
def dashboard():
    if is_admin():
        projects = Project.query.all()
        users = User.query.all()
        tasks = Task.query.all()

        total_users = len(users)
        total_projects = len(projects)
        total_tasks = len(tasks)
        complete_tasks = sum(1 for task in tasks if task.status == 'completed')
        pending_tasks = total_tasks - complete_tasks
        completion_rate = int((complete_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        return render_template("admin_dashboard.html", projects=projects, users=users, tasks=tasks,
                               total_users=total_users, total_projects=total_projects,
                               total_tasks=total_tasks, complete_tasks=complete_tasks,
                               pending_tasks=pending_tasks, completion_rate=completion_rate)
    else:
        projects = Project.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', name=current_user.username, projects=projects)

def is_admin():
    return current_user.is_authenticated and current_user.role == "admin"

@app.route('/manage_users')
@login_required
def manage_users():
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('manage_users.html'))
    users = User.query.order_by(User.username).all()
    return render_template('manage_users.html', users=users)

@app.route('/add_task/<int:project_id>', methods=['GET', 'POST'])
@login_required
def add_task(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        if project.user_id != current_user.id:
            abort(403)  # Forbidden
        form = TaskForm()
        if form.validate_on_submit():
            due_date = form.due_date.data if form.due_date.data else None
            new_task = Task(
                title=form.title.data,
                description=form.description.data,
                due_date=due_date,
                priority=form.priority.data,
                project_id=project.id
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('tasks', project_id=project.id))
    return render_template('add_task.html', project=project, form=TaskForm())

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)

    class EditUserForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        username = StringField('Username', validators=[DataRequired()])
        role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')])
        first_name = StringField('First Name')
        last_name = StringField('Last Name')
        phone = StringField('Phone')
        submit = SubmitField('Update')

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = form.role.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', form=form, user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for('manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('manage_users'))

@app.route('/toggle_role/<int:user_id>', methods=['POST'])
@login_required
def toggle_role(user_id):
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot change your own role.", "warning")
        return redirect(url_for('manage_users'))

    user.role = 'admin' if user.role == 'user' else 'user'
    db.session.commit()
    flash(f"User '{user.username}' role changed to {user.role}.", "success")
    return redirect(url_for('manage_users'))

@app.route('/task/<int:project_id>')
@login_required
def tasks(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id and not is_admin():
        abort(403)  # Forbidden
    return render_template('tasks.html', project=project, tasks=project.tasks)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
        form = ProjectForm()
        if current_user.role == 'admin':
            form.assign_to.choices = [(u.id, u.username) for u in User.query.order_by(User.username).all()]
        else:
            form.assign_to.choices = [(current_user.id, current_user.username)]
            form.assign_to.data = current_user.id 
        if form.validate_on_submit():
            project = Project(name=form.name.data.strip(), description=(form.description.data.strip() or None), user_id=form.assign_to.data)
            db.session.add(project)
            db.session.commit()
            flash("Project created successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            print(form.errors)
        return render_template('add_project.html', form=form)

@app.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.project.user_id != current_user.id and not is_admin():
        abort(403)
    task.status = 'completed'
    db.session.commit()
    flash("Task marked as completed.", "success")
    return redirect(url_for('tasks', project_id=task.project_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_user')
def add_user():
    new_user = User(email='testuser@example.com', username='testuser', password=generate_password_hash('testpass', method='pbkdf2:sha256', salt_length=8))
    db.session.add(new_user)
    db.session.commit()
    return f"User {new_user.username} added!"

@app.route('/get_users')
def get_users():
    users = User.query.all()
    return "<br>".join([f"User {user.username}, Email: {user.email}" for user in users])

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(email='admin@example.com', username='admin', password=generate_password_hash('admin123', method='pbkdf2:sha256', salt_length=8), role='admin')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created with username 'admin' and password 'admin123'")
        else:
            print("Admin user already exists.")
    app.run(debug=True)

