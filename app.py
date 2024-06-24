from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(700), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __retr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['name']
        task_desc = request.form['description']
        new_task = TODO(name=task_name, description=task_desc)

        #try:
        db.session.add(new_task)
        print(1)
        db.session.commit()
        print(2)
        return redirect('/')
        #except:
        #    return("something happened")

    else:
        tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'something happened'

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task = TODO.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        task.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return("something happened")
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
