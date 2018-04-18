from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Sequence, Boolean
from flask_bootstrap import Bootstrap


app = Flask(__name__, static_url_path='/static')
Bootstrap(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
session = db.session


class Todo(db.Model):
    __tablename__ = 'todos'
    id_todo_seq = Sequence('todos_id_todo_seq', metadata=db.metadata)

    id_todo = Column(Integer, server_default=id_todo_seq.next_value(), primary_key=True)
    description = Column(Text)
    complete = Column(Boolean)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_all_todos')
def get_todos():
    todos = session.query(Todo).all()
    d = []
    for todo in todos:
        d.append({'id_todo': todo.id_todo, 'description': todo.description, 'complete': todo.complete})
    return jsonify({'result': d})


@app.route('/add', methods=['POST'])
def add():
    try:
        if 'description' in request.args and request.args['description'] != "":
            todo = Todo(description=request.args['description'], complete=False)
            session.add(todo)
            session.commit()
            return jsonify({'status': 'success'})
    except:
        session.rollback()
        return jsonify({'status': 'error'})


@app.route('/<id_todo>', methods=['PUT'])
def modify(id_todo):
    try:
        todo = session.query(Todo).filter(Todo.id_todo == id_todo).first()
        todo.complete = not todo.complete
        session.commit()
        return jsonify({'status': 'success'})
    except:
        session.rollback()
        return jsonify({'status': 'error'})


@app.route('/<id_todo>', methods=['DELETE'])
def delete(id_todo):
    try:
        session.query(Todo).filter(Todo.id_todo == id_todo).delete()
        session.commit()
        return jsonify({'status': 'success'})
    except:
        session.rollback()
        return jsonify({'status': 'error'})


if __name__ == '__main__':
    app.run()

