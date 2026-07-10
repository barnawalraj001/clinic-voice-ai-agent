from sqlalchemy import Column, String
from app.database import Base


class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    state = Column(String)