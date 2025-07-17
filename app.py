from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

# Función para crear las tablas si no existen
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            tid INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS done (
            did INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            task_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/addTask', methods=['GET'])
def add_task():
    task = request.args.get('task')
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks(task) VALUES(?)", (task,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/getTasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    row = cursor.fetchone()
    conn.close()
    return render_template("index.html", tasks=row)

@app.route('/move-to-done/<int:id>/<string:task_name>')
def move_to_done(id, task_name):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO done(task, task_id) VALUES(?,?)", (task_name,id))
    cursor.execute("DELETE FROM tasks WHERE tid = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/deleteTask/<int:id>')
def deleteTask(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE tid=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete-completed/<int:id>')
def deleteCompletedTask(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM done WHERE did=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/')
def home():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    row = cursor.fetchall()
    cursor.execute("SELECT * FROM done")
    row2 = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=row, done=row2)

# IMPORTANTE: Ejecutar creación de tablas al iniciar
if __name__ == "__main__":
    init_db()
    app.run(debug=True)


