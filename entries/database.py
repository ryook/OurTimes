from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

# databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ourtimes.db')
database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

def init_db():
    import entries.models
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
	manager.run()