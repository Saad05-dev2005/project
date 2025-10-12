
# Project Title: Project and Task Management System

**Developer:** Opeyemi Saad Opemipo  
**Institution:** Lagos State University  
**Program:** ICT Training and Services Management  
**Supervisor:** Mr. Shanu  

---

## Introduction

The Project and Task Management System is a web-based application designed to streamline the process of organizing, assigning, and tracking tasks within projects. Built with Flask (Python) and SQLAlchemy, it supports multiple users with distinct roles and provides a structured interface for efficient work management.

---

## Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (via SQLAlchemy ORM)
- **Frontend:** HTML (Jinja2 templates), CSS
- **Authentication:** Flask-Login

---

## User Roles and Access Control

- **Admin:**
  - View all users, projects, and tasks
  - Full control over system data
  - Monitor overall activity and performance

- **User:**
  - Create and manage personal projects
  - Assign and update tasks within their own projects
  - Track task status and progress

Each user logs in with secure credentials; their role determines their interface and permissions.

---

## Application Workflow

1. **User Authentication:**  
	Users log in and are directed to dashboards based on their role.

2. **Dashboard Access:**  
	- **Admin Dashboard:** All users, projects, tasks, and system statistics  
	- **User Dashboard:** User’s own projects, tasks, and deadlines

3. **Project Creation:**  
	Users create projects by providing a name, description, and deadline.

4. **Task Assignment:**  
	Within projects, users add tasks, set priorities and due dates, and define status (Pending, In Progress, Completed).

5. **Task Tracking:**  
	Users update task status as work progresses, enabling real-time tracking of project completion.

6. **Data Persistence:**  
	All data is stored in a local SQLite database (`site.db`), managed automatically by SQLAlchemy.

---

## Software Logic Summary

- **Backend:** Flask handles routing, session management, and database operations.
- **Frontend:** Jinja2 HTML templates render dynamic content; CSS for styling.
- **Database:** SQLAlchemy defines models and relationships; SQLite stores data.
- **Security:** Basic authentication ensures role-based access and data protection.

---

## Use Case Relevance

This system addresses real-world ICT service management needs:
- Organizing digital workflows
- Assigning and monitoring tasks
- Managing user access and visibility
- Supporting collaborative environments

It demonstrates practical software engineering principles: modular design, database integration, and user interface logic.

---

## Future Improvements

- Add user profile editing
- Integrate email alerts for task deadlines
- Deploy to a cloud platform (e.g., Heroku or Render)
- Add analytics for task completion rates

---


