import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# DB initialize
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# HOME
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    if request.method == "POST":
        task = request.form["task"]
        c.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
        conn.commit()

    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# EDIT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()

    if request.method == "POST":
        new_task = request.form["task"]
        c.execute("UPDATE tasks SET content=? WHERE id=?", (new_task, id))
        conn.commit()
        conn.close()
        return redirect("/")

    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
