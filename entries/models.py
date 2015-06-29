from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from entries.database import Base
from datetime import datetime

class Entries(Base):
	__tablename__ = "entries"
	__table_args__ = {"useexisting": True}
	id = Column("id", Integer, primary_key=True)
	title = Column("title", String(128))
	member = Column("member", Text)
	date = Column("date",Text)
	url = Column("url", String(140))
	links = relationship("Links")
	Columns = relationship("Columns",order_by='Columns.id',
                         uselist=True)
	Statics = relationship("Statics", order_by='Statics.id',
                         uselist=True)

	def __init__(self, title = None, member=None, date=None, url=None):
		self.title = title
		self.member = member
		self.date = date
		self.url = url

	def  __reper__(self):
		return "<Entries ('%s','%s','5s')>" %(self.title,self.member,self.date)

class Links(Base):
	__tablename__ = "links"
	id = Column("id",Integer, primary_key=True)
	entry_id = Column(Integer, ForeignKey('entries.id',
        onupdate='CASCADE', ondelete='CASCADE'))
	title = Column(Text)
	url = Column(Text)

	def __init__(self, title=None, url=None):
		self.title = title
		self.url = url

	def  __reper__(self):
		return "<Links ('%s','%s')>" %(self.title,self.url)

class Columns(Base):
	__tablename__ = "columns"
	id = Column(Integer, primary_key=True)
	entry_id = Column(Integer, ForeignKey('entries.id',
        onupdate='CASCADE', ondelete='CASCADE'))
	title = Column(String(100))
	text  = Column(String(500))
	image_url = Column(String(200))

	def __init__(self, title=None, text=None, image_url=None):
		self.title = title
		self.text = text
		self.image_url = image_url

	def  __reper__(self):
		return "<Columns ('%s','%s')>" %(self.text,self.image_url)

class Statics(Base):
	__tablename__ = "statics"
	id = Column(Integer, primary_key=True)
	entry_id = Column(Integer, ForeignKey('entries.id',
        onupdate='CASCADE', ondelete='CASCADE'))
	title = Column(String(100))
	text = Column(String(500))
	image_url = Column(String(200))
	link = Column(String(200))


	def __init__(self, title=None, text=None, image_url=None, link=None):
		self.title
		self.text = text
		self.image_url = image_url
		self.link = link


	def  __reper__(self):
		return "<Statics ('%s','%s','%s')>" %(self.text,self.image_url)
