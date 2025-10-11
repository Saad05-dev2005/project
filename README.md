Software Functionality Overview
Project Title: Project and Task Management System
Technology Stack: Flask (Python), Flask SQLAlchemy, SQLite, HTML/CSS
Developer: Opeyemi Saad Opemipo
Institution: Lagos State University
Program: ICT Training and Services Management
Supervisor: Mr. Shanu

Introduction
The Project and Task Management System is a web-based application designed to streamline the process of organizing, assigning, and tracking tasks within projects. It supports multiple users with distinct roles and provides a structured interface for managing work efficiently. The system was developed using Flask, a lightweight Python web framework, and SQLAlchemy for database interaction.

User Roles and Access Control
The system implements role-based access, dividing users into two categories:
- Admin:
- Can view all users, projects, and tasks
- Has full control over system data
- Can monitor overall activity and performance

- User:
- Can create and manage personal projects
- Can assign tasks within their own projects
- Can update task status and view progress
Each user logs in with secure credentials, and their role determines the interface and permissions they receive.

Application Workflow
1. User Authentication
Upon launching the application, users are prompted to log in. The system verifies credentials and assigns the appropriate dashboard based on the user’s role.

2. Dashboard Access
- Admin Dashboard displays:
- All registered users
- All projects and tasks
- System-wide statistics
- User Dashboard displays:
- Projects created by the user
- Tasks assigned within those projects
- Task status and deadlines

3. Project Creation
Users can create new projects by providing:
- Project name
- Description
- Deadline
Each project is linked to the user who created it.

4. Task Assignment
Within a project, users can:
- Add tasks
- Set priority (e.g., High, Medium, Low)
- Assign due dates
- Define task status (e.g., Pending, In Progress, Completed)
Tasks are stored and displayed under their respective projects.

5. Task Tracking and Updates
Users can update task status as work progresses. This allows for real-time tracking of project completion and individual responsibilities.

6. Data Persistence
All user, project, and task data is stored in a local SQLite database (site.db). The database is managed automatically by SQLAlchemy and accessed through Flask routes.

Software Logic Summary
- Backend: Flask handles routing, session management, and database operations
- Frontend: HTML templates render dynamic content using Jinja2, CSS and Javascripts
- Database: SQLAlchemy defines models and relationships; SQLite stores data
- Security: Basic authentication ensures role-based access and data protection

Use Case Relevance
This system reflects real-world ICT service management needs, such as:
- Organizing digital workflows
- Assigning and monitoring tasks
- Managing user access and visibility
- Supporting collaborative environments
It demonstrates practical application of software engineering principles, including modular design, database integration, and user interface logic.

Future Improvements
Demonstrate forward-thinking:
- Add user profile editing
- Integrate email alerts for task deadlines
- Deploy to a cloud platform (e.g., Heroku or Render)
- Add analytics for task completion rates


