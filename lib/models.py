from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, BigInteger, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    phone = Column(BigInteger)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    
    # Define the relationship to the Role table
    role = relationship("Role", back_populates="auditions")
    
    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String(255), nullable=False)

    # A role can have many auditions
    auditions = relationship("Audition", back_populates="role")

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]    

    def lead(self):
        for audition in self.auditions:
            if audition.hired:
                return audition
        return "No one has been hired for this role yet."

    def understudy(self):
        hired_count = 0
        for audition in self.auditions:
            if audition.hired:
                hired_count += 1
            if hired_count == 2:
                return audition

        return "No understudy has been hired for this role yet."
