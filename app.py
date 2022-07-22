from asyncio import tasks
from datetime import datetime
import flask
from flask_sqlalchemy import SQLAlchemy
app = flask.Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

string = ""
with open("var/www/bingxuhu_server/logs/accessloc.log") as logfile:
    string = logfile.read()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route("/task-master",methods=['POST','GET'])
def task_master():
    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return flask.redirect('/task-master')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return flask.render_template("task-master/index.html", tasks = tasks)

@app.route("/task-master/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)


    db.session.delete(task_to_delete)
    db.session.commit()
    return flask.redirect('/task-master')

@app.route("/task-master/update/<int:id>",methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if flask.request.method == 'POST':
        task.content = flask.request.form['content']

        try:
            db.session.commit()
            return flask.redirect('/task-master')
        except:
            return 'There was issue updating.'
    else:
        return flask.render_template('/task-master/update.html',task=task)

@app.route("/access")
def access():
    return string

if __name__ == "__main__":
    app.run(debug=True, threaded=False)