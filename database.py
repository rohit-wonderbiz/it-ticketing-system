from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mssql+pymssql://sa:User123@DESKTOP-KUTTPQR/TicketDB"

engine = create_engine(URL_DATABASE, pool_size=10, max_overflow=30)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# from sqlalchemy import create_engine, exc
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.exc import OperationalError

# SQLALCHEMY_DATABASE_URL = "mssql+pymssql://sa:User123@DESKTOP-KUTTPQR/TicketDB"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def test_connection():
#     try:
#         # Create a session
#         session = SessionLocal()
        
#         # Just checking if the session could be created
#         print("Connection to the database successful!")
        
#         # Close the session
#         session.close()
#     except exc.SQLAlchemyError as e:
#         print(f"Database error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Call the test_connection function to check the connection
# if __name__ == "__main__":
#     test_connection()