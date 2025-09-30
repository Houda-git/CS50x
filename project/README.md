# My To-Do List Website
#### Video Demo:  https://www.youtube.com/watch?v=SUQBv5YFMOU
#### Description:
#### To-Do List Web App

For my final project in CS50’s Introduction to Computer Science, I wanted to create something that not only applied the programming concepts I learned throughout the course, but also solved a problem I personally face on a daily basis: staying organized and managing tasks. That’s why I chose to build a To-Do List Web Application.

The main purpose of this project is to provide a simple, user-friendly, and efficient way to organize tasks. Unlike static websites, this project combines both front-end and back-end development to create a fully interactive experience. Users can log in, create categories, add tasks, track their progress, and see how much they’ve accomplished in a clean and structured interface.

I wanted this project to go beyond just being a “list of tasks.” The idea was to simulate what a real-world application looks like, where a user has their own account, can securely log in, and store personal information that persists across sessions. This is why I included a login and authentication system, where user credentials are securely stored using hashed passwords.

The progress tracker was another feature I added to make the app more engaging. Instead of simply checking off tasks, users can see a visual indicator of their productivity — for example, a percentage or progress bar showing how many tasks they’ve completed out of the total. This gamification element motivates users to keep finishing their tasks.

From a technical perspective, I used:

Flask as the backend framework because of its simplicity and flexibility for small web projects. It allowed me to handle routes, manage sessions, and connect easily to the database.

SQLite for the database, since it’s lightweight, requires no setup, and is perfect for projects of this scale. I designed a schema that includes tables for users, categories, and tasks, which helped me practice database normalization and relationships.

CS50 Library for simplifying SQL queries, which made it easier to interact with the database.

HTML, CSS, and JavaScript to build the front-end, ensuring the interface was both functional and visually appealing. I also used Jinja2 templates to render dynamic content from Flask directly into the HTML.

I also learned a lot about structuring a full-stack project. For example, I separated my files into templates/ and static/ folders so that HTML, CSS, and JavaScript code are well-organized. This not only follows Flask conventions but also mirrors real-world web development practices.

One of the challenges I faced was integrating everything together — ensuring that the front-end interacted correctly with the back-end, and that the database queries worked as expected. Debugging issues such as user sessions, login states, and database updates taught me the importance of carefully tracking data flow across the application.

Another challenge was making the application scalable and reusable. I didn’t just want a single to-do list for all users; instead, I designed the app so that each registered user has their own account, their own categories, and their own tasks. This meant implementing user-specific queries and making sure that data isolation was respected.

Overall, this project represents a culmination of all the skills I developed in CS50:

Problem-solving and algorithmic thinking to structure the logic of the app.

Database management to design and query relational data.

Web development to connect front-end and back-end.

Security practices to handle passwords safely.

This project is special to me because it’s not just an assignment — it’s a tool I could actually use in my daily life to stay productive. More importantly, it shows me how far I’ve come since the first lecture of CS50, when programming felt overwhelming. Now, I can confidently design, build, and deploy a web application from scratch.

In the future, I’d like to expand this project by adding new features such as deadline reminders, a calendar view, email notifications, and a more polished interface using frameworks like Bootstrap or TailwindCSS. I also plan to deploy it online using Heroku or Render so that others can try it out easily.

To me, this project embodies what CS50 is all about: starting from zero, learning step by step, and finally building something real and meaningful.

#### Features

- Task Categorization: Organize tasks into categories.

- Progress Tracker: Visual progress of tasks completed.

- CS50 Library Integration: Simplifies SQL queries and database management.

- Login System: Secure user authentication.

#### Technologies Used

- Python + Flask

- CS50 Library (for SQL and convenience)

- SQLite

- HTML, CSS, JavaScript, Jinja2 templates

#### Project Structure
```
project/
│
├── templates/
│   ├── index.html
│   ├── layout.html
│   └── login.html
│
├── static/
│   ├── css/
│   └── js/
│
├── app.py
├── schema.sql
├── helpers
├── todo.db
└── README.md
``
#### How to Run Locally

##### Clone the repository:

git clone https://github.com/code50/180598520.git
cd project

##### Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

##### Install dependencies, including CS50 library:

pip install -r requirements.txt
pip install cs50

##### Initialize the database:

flask init-db

##### Run the app:

flask run

#### ⚠️ Note:
 Users without a CS50 account can run this project as long as the CS50 Python library is installed. A CS50 account is not required.



