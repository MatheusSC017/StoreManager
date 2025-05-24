from sqlalchemy import Column, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship
from app.models.order import Order


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    orders = relationship("Order", back_populates="client")
