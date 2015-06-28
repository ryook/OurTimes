#coding:utf-8

from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import datetime
from entries.models import Entries, Links, Columns, Statics
from entries.database import db_session


DATABASE = "/tmp/ourtimes.db"
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'a'

app = Flask(__name__)
app.config.from_object(__name__)

# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# @app.before_request
# def before_request():
# 	g.db = connect_db()

# @app.after_request
# def after_request(response):
# 	g.db.close()
# 	return response

@app.route("/", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		if request.form["username"] != app.config["USERNAME"]:
			error = "Invalid username"
		elif request.form["password"] != app.config["PASSWORD"]:
			error = "Invalid password"
		else:
			session["logged_in"] = True
			flash("you were logged in")
			return redirect(url_for("show_entries"))
	return render_template("login.html", error=error)

@app.route("/logout")
def logout():
	session.pop("logged_in", None)
	flash("you were logged out")
	return redirect(url_for("login"))

@app.route("/entries", methods=["GET"])
def show_entries():
	# cur = g.db.execute("select date, title, member from entries order by id desc")
	# entries = [dict(date=row[0], title=row[1], member=row[2]) for row in cur.fetchall()]
	entries = Entries.query.all()
	return render_template("show_entries.html",entries=entries)

@app.route("/detail/<id>", methods=["GET"])
def show_detail(id):
	entry = Entries.query.filter_by(id=id).first()
	links = Links.query.filter_by(entry_id=id).first()
	if entry is None:
		abort(404)
	print entry.__getattribute__
	return render_template("detail.html",entry=entry,links=links)

@app.route("/detail/<id>", methods=["POST"])
def edit_detail(id=None):
    if id is None:
    	abort(404)
    d = datetime.datetime.today()
    date = datetime.date(d.year, d.month, d.day)
    content = Entries.query.filter_by(id=id).first()
    content.title = request.form["title"]
    content.member = request.form["member"]
    content.date = date
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("detail.html",entry=content))



@app.route("/new", methods=["GET", "POST"])
def new():
	return render_template("post.html")

@app.route("/add", methods=["POST"])
def add_entry():
	print request.form
	# message = ""
	if not session.get("logged_in"):
		abort(401)
	d = datetime.datetime.today()
	date = datetime.date(d.year, d.month, d.day)
	entry = Entries(request.form["title"],request.form["member"],date)
	column1 = Columns(request.form["column1"],request.form["c1_image"])
	column2 = Columns(request.form["column2"],request.form["c2_image"])
	columns = [column1, column2]
	entry.Columns = columns
	statics = [Statics(request.form["statics"],request.form["s_image"],request.form["s_link"])]
	entry.Statics = statics
	link1 = Links(request.form["news1"],request.form["n1_link"])
	link2 = Links(request.form["news2"],request.form["n2_link"])
	link3 = Links(request.form["news3"],request.form["n3_link"])
	link4 = Links(request.form["news4"],request.form["n4_link"])
	link5 = Links(request.form["news5"],request.form["n5_link"])
	link6 = Links(request.form["news6"],request.form["n6_link"])
	link7 = Links(request.form["news7"],request.form["n7_link"])
	link8 = Links(request.form["news8"],request.form["n8_link"])
	link9 = Links(request.form["news9"],request.form["n9_link"])
	link10 = Links(request.form["news10"],request.form["n10_link"])
	links = [link1, link2, link3, link4, link5, link6, link7, link8, link9, link10]
	entry.links = links
	db_session.add(entry)
	db_session.commit()
	flash("New entry was successfully posted")
	return redirect(url_for("show_entries"))

# def add_link():
# 	id = Entries.query.filter_by(id=id).first()



if __name__ == '__main__':
    app.run()