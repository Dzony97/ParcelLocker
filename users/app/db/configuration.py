from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativBase


class Base(DeclarativBase):
    pass


sa = SQLAlchemy(model_class=Base)