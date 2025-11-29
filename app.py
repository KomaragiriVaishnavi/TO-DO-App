from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("tasks.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        );
    """)
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

# Add task
@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        conn = sqlite3.connect("tasks.db")
        conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect("/")

# Delete task
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Mark as complete
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    conn.execute("UPDATE tasks SET completed = 1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
