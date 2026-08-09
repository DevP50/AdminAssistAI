import os
from dotenv import load_dotenv
load_dotenv()
class BaseConfig:
    #This class contains the basic configuration the flask app must have
    SECRET_KEY = os.getenv('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError("SECRET KEY VALUE REQUIRED FOR STARTUP!")
    
    if FEATHERLESS_API_KEY := os.getenv('FEATHERLESS_API_KEY') is None:
        raise ValueError("FEATHERLESS_API_KEY VALUE REQUIRED FOR STARTUP!")

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE URI REQUIRED FOR STARTUP")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    ALLOWED_EXTENSIONS = {"xlsx", "xls"}
    
