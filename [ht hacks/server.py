
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask,render_template, session

from flask import Flask, request, render_template, request
from sqlalchemy.sql.expression import select
from os import path

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# create db for tasks  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///msgs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dbt = SQLAlchemy(app)

# db model 
class Messages(dbt.Model):
    id = dbt.Column(dbt.Integer, primary_key=True)
    content = dbt.Column(dbt.Text, nullable=False)
    date_created = dbt.Column(dbt.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
            return f"Post('{self.date_created}', '{self.content}')"
dbt.create_all(app=app)

# page routes 
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        body = request.form.get("desc")

        new_msg = Messages( content=body)
        dbt.session.add(new_msg)
        dbt.session.commit()
        return render_template('index.html')
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)