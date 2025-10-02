# Copilot Instructions for AI Coding Agents

## Project Overview

This is a Flask web application for project and task management. It uses SQLAlchemy ORM for data modeling and Flask-Login for authentication. The app supports user registration, login, role-based dashboards (admin/user), project creation, and task tracking.

## Architecture & Data Flow

- **Single-file app**: All backend logic is in `app.py`.
- **Database**: SQLite (`instance/site.db`) via SQLAlchemy models (`User`, `Project`, `Task`).
- **Templates**: HTML files in `templates/` (e.g., `dashboard.html`, `admin_dashboard.html`).
- **Static files**: CSS in `static/`.
- **Virtual environment**: All dependencies in `env/`.

### Data Relationships
- `User` has a `role` field (`user` or `admin`).
- `Project` is linked to `User` via `user_id`.
- `Task` is linked to `Project`.
- `Project.progress` computes completion % from associated tasks.

## Developer Workflows

- **Run the app**:
	- Activate venv:
		- PowerShell: `./env/Scripts/Activate.ps1`
		- CMD: `env/Scripts/activate.bat`
	- Start server: `python app.py`
- **Database setup**: Tables auto-created on app start (`db.create_all()` in `app.py`).
- **Dependencies**: Use `pip install <package>` with venv activated. Packages in `env/Lib/site-packages/`.
- **Debugging**: App runs in debug mode (`app.run(debug=True)`).

## Project-Specific Patterns & Conventions

- **Authentication**: Use `@login_required` for protected routes. Role checks via `is_admin()` helper.
- **Error handling**: Use `abort(403)` for forbidden access.
- **Password hashing**: Use `werkzeug.security.generate_password_hash` (`pbkdf2:sha256`).
- **Template updates**: Edit HTML in `templates/`, CSS in `static/`.
- **Adding models/routes**: Define in `app.py`, update templates as needed.

## Integration Points

- **Flask extensions**:
	- `flask_sqlalchemy` (ORM)
	- `flask_login` (auth)
	- `flask_migrate`/`alembic` (installed, not actively used)
- **External packages**:
	- `werkzeug` (passwords)
	- `jinja2` (templating)

## Examples

- **Protect a route**:
	```python
	@app.route('/admin')
	@login_required
	def admin_panel():
			if not is_admin():
					abort(403)
			# ...existing code...
	```
- **Add a new field to a model**:
	```python
	class Project(db.Model):
			# ...existing code...
			new_field = db.Column(db.String(100), nullable=True)
	```

## Key Files & Directories

- `app.py`: Main backend logic
- `templates/`: HTML templates
- `static/`: CSS files
- `instance/site.db`: SQLite database
- `env/`: Python virtual environment

---

**Feedback requested:**
Are any workflows, conventions, or architectural details missing or unclear? Please specify so these instructions can be improved.
