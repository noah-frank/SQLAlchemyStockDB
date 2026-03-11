from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

from sqlalchemy import create_engine
engine = create_engine("sqlite:///test_database.db", echo=True) # sqlite:// in memory

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session

with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants", 
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")

    session.add_all([spongebob, sandy, patrick])
    session.commit()


print("### SELECT MULTIPLE USERS ###")
from sqlalchemy import select

session = Session(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

for user in session.scalars(stmt):
    print("USER :", user)


print("### SELECT USING JOIN ###")
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)
sandy_address = session.scalars(stmt).one()
print("SANDY ADDRESS :", sandy_address)

print("### MAKE CHANGES ###")
stmt = select(User).where(User.name=="patrick")
patrick = session.scalars(stmt).one()

patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"
session.commit()

stmt = select(Address)
for address in session.scalars(stmt):
    print("ADDRESS :", address)

print("### SOME DELETES ###")

sandy = session.get(User, 2)
sandy.addresses.remove(sandy_address) # Removes one of sandy's addresses

session.flush() # Removes address from user_id == 2 (sandy) in results without committing the results

# `patrick` declaration
# stmt = select(User).where(User.name=="patrick")
# patrick = session.scalars(stmt).one()
session.delete(patrick) # DELETES whole patrick column

session.commit() # Commits the changes made above

stmt = select(User)
for user in session.scalars(stmt):
    print("USER :", user)

stmt = select(Address)
for address in session.scalars(stmt):
    print("ADDRESS :", address)