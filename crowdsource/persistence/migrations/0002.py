from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crowdsource.persistence import Client

db = create_engine('postgresql://cs:crowdsource@localhost:8890/')
Session = sessionmaker(bind=db)
session = Session()

session.add(Client())
session.add(Client())
session.add(Client())
session.commit()
