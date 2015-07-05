#coding:utf-8

from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import datetime
from entries.models import Entries, Links, Columns, Statics
from entries.database import db_session, engine
import os
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE = "/tmp/ourtimes.db"
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin_user'
PASSWORD = 'ssa_2015'


app = Flask(__name__)
app.config.from_object(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/", methods=["GET"])
def show_top():
	entries = Entries.query.all()
	return render_template("top.html",entries=entries)

@app.route("/<id>",methods=["GET"])
def show_content(id):
	entry = Entries.query.filter_by(id=id).first()
	links = Links.query.filter_by(entry_id=id).all()
	columns = Columns.query.filter_by(entry_id=id).all()
	statics = Statics.query.filter_by(entry_id=id).all()
	pic = ["image/s1.jpg","image/s2.jpg","image/s3.jpg","image/s4.jpg","image/s5.jpg","image/s6.jpg","image/s7.jpg","image/s8.jpg","image/s9.jpg","image/s10.jpg"]
	return render_template("content.html",entry=entry,links=links,statics=statics,columns=columns,pic=pic)

@app.route("/column/<id>", methods=["GET"])
def show_column(id):
	column = Columns.query.filter_by(id=id).first()
	entry = Entries.query.filter_by(id=column.entry_id).first()
	return render_template("readmore.html",column=column,entry=entry)

@app.route("/statics/<id>", methods=["GET"])
def show_static(id):
	static = Statics.query.filter_by(id=id).first()
	entry = Entries.query.filter_by(id=static.entry_id).first()
	return render_template("readmore.html",static=static,entry=entry)

@app.route("/admin", methods=["GET", "POST"])
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
	links = Links.query.filter_by(entry_id=id).all()
	columns = Columns.query.filter_by(entry_id=id).all()
	statics = Statics.query.filter_by(entry_id=id).all()
	if entry is None:
		abort(404)
	return render_template("detail.html",entry=entry,links=links,statics=statics,columns=columns)


@app.route("/detail/<id>", methods=["POST"])
def edit_detail(id=None):
	if id is None:
		abort(404)
	entry = Entries.query.filter_by(id=id).first()
	links = Links.query.filter_by(entry_id=id).all()
	columns = Columns.query.filter_by(entry_id=id).all()
	statics = Statics.query.filter_by(entry_id=id).all()
	entry.title = request.form["title"]
	entry.member = request.form["member"]
	entry.date = request.form["date"]
	entry.url = request.form["g_image"]
	columns[0].title = request.form["c1_title"]
	columns[0].text = request.form["column1"]
	columns[0].image_url = request.form["c1_image"]
	columns[1].title = request.form["c2_title"]
	columns[1].text = request.form["column2"]
	columns[1].image_url = request.form["c2_image"]
	statics[0].title = request.form["s_title"]
	statics[0].text = request.form["statics"]
	statics[0].image_url = request.form["s_image"]
	statics[0].link = request.form["s_link"]
	links[0].title = request.form["news1"]
	links[0].url = request.form["n1_link"]
	links[1].title = request.form["news2"]
	links[1].url = request.form["n2_link"]
	links[2].title = request.form["news3"]
	links[2].url = request.form["n3_link"]
	links[3].title = request.form["news4"]
	links[3].url = request.form["n4_link"]
	links[4].title = request.form["news5"]
	links[4].url = request.form["n5_link"]
	links[5].title = request.form["news6"]
	links[5].url = request.form["n6_link"]
	links[6].title = request.form["news7"]
	links[6].url = request.form["n7_link"]
	links[7].title = request.form["news8"]
	links[7].url = request.form["n8_link"]
	links[8].title = request.form["news9"]
	links[8].url = request.form["n9_link"]
	links[9].title = request.form["news10"]
	links[9].url = request.form["n10_link"]
	entry.Columns = columns
	entry.links = links
	entry.Statics = statics
	db_session.add(entry)
	db_session.commit()
	return redirect(url_for("show_detail", id=id))

@app.route("/new", methods=["GET"])
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
	entry = Entries(request.form["title"],request.form["member"],date,request.form["g_image"])
	column1 = Columns(request.form["c1_title"],request.form["column1"],request.form["c1_image"])
	column2 = Columns(request.form["c2_title"],request.form["column2"],request.form["c2_image"])
	columns = [column1, column2]
	entry.Columns = columns
	statics = [Statics(request.form["s_title"],request.form["statics"],request.form["s_image"],request.form["s_link"])]
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

@app.route("/0520/del/<id>",methods=["GET"])
def delete(id):
	target = db_session.query(Entries).get(id)
	db_session.delete(target)
	db_session.commit()
	return redirect("entries")

if __name__ == '__main__':
    app.run()