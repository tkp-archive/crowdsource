from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crowdsource.persistence import Client, Competition, Submission

db = create_engine('postgresql://cs:crowdsource@localhost:8890/')

Client.metadata.create_all(db)
Competition.metadata.create_all(db)
Submission.metadata.create_all(db)

Session = sessionmaker(bind=db)
session = Session()
