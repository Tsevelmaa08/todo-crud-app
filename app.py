from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form["task"]
        tasks.append(task)
        return redirect("/")
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    tasks.pop(id)
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        new_task = request.form["task"]
        tasks[id] = new_task
        return redirect("/")
    return render_template("edit.html", task=tasks[id], id=id)

if __name__ == "__main__":
    app.run(debug=True)
