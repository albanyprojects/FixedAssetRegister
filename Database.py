from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

SERVER = 
DATABASE = 
USERNAME = 
PASSWORD = 



url = URL.create(
    "mssql+pyodbc",# brings in the import 
    username="jayden", # is me, any edit done for now would be on my account under my name, inside of this account will eventually be the authentication
    password=PASSWORD,  # password
    host="10.1.101.141",  #the private IP of the server with the sql database on it
    port=1433, # the forwarded port
    database="jayden",
    query={
        "driver": "ODBC Driver 18 for SQL Server",  #this is different depending on the pc you have, this one needs odbc driver 18, if theres an error and this isnt the original machine, change it to 17.
        "Encrypt": "no", # needs specifying. 
        "TrustServerCertificate": "yes", # if no, then the api just wouldnt load. 
    },
)

engine = create_engine(url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

if __name__ == "__main__":            #only one database is really being used, so main is the one. 
    try:
        connection = engine.connect()
        print("Database connection successful")
        connection.close()
    except Exception as e:
        print("Database connection failed:")
        print(e)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # db is a local modifier. the server wont close until the user does it in the terminal
