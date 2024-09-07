import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import init_app, get_db

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.instance_path, 'todo.sqlite')

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

init_app(app)

@app.route('/')
def index():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    db = get_db()
    db.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    db.commit()
    tasks = db.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    return render_template('task_list.html', tasks=tasks)

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    new_status = not task['completed']
    db.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, id))
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    return render_template('task.html', task=task)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return ''  # Return an empty string instead of a 204 status

if __name__ == '__main__':
    app.run(debug=True)