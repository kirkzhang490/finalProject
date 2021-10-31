from sqlalchemy import create_engine  
from sqlalchemy import Table,Column, String,Integer
from sqlalchemy import select,delete, update
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker


db_string = "postgresql://postgres:kaikai49@localhost:5430"

db = create_engine(db_string)  
base = declarative_base()
Session = sessionmaker(db)  
session = Session()

class Users(base):  
    __tablename__ = 'users'
    id =  Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    categories = Column(String)
    feedback = Column(String)

    def create(self, name, categories, feedback):
        result =  session.query(Users).filter(Users.name==name).first()
        if result is not None:
            return 'duplicated name try again'
        try:
            stmt = Users(name=name, categories=categories, feedback=feedback)  
            session.add(stmt)
            session.commit()
        except:
            return 'not able to create this time'
        return self.queryByName(name)
        
    
    def queryByName(self, name):
        result =  session.query(Users).filter(Users.name==name).one()
        return 'Created name: ' + result.name + ' categories: ' + result.categories + ' feedback: ' + result.feedback + 'id: ' + str(result.id)
    
    def dropTable(self):
        session.query(Users).delete()
        session.commit()

    def allUsers(self):
        users_ = session.query(Users)
        result = []
        for user in users_:  
            result.append({
                'name': user.name,
                'categories': user.categories,
                'feedback': user.feedback
            })
        print(result)
        return result
    
    def updateUser(self,name, categories, feedback):
        check =  session.query(Users).filter(Users.name==name).first()
        if check is None:
            return 'user not exist'
        try:
            session.query(Users).filter(Users.name == name).update({"categories": categories, 'feedback': feedback})
            session.commit()
        except:
            return 'not able to update this time'
        return 'success updated'
    
    def insertFeedBack(self,name, feedback):
        record =  session.query(Users).filter(Users.name==name).first()
        if record is None:
            return 'user not exist'
        try:
            newFeedback = ','.join([record.feedback,feedback])
            session.query(Users).filter(Users.name == name).update({'feedback': newFeedback})
            session.commit()
        except:
            return 'not able to insert feedback this time'
        return 'success insert'

# # Delete
# stmt = delete(Users).where(Users.name == 'Doctor Strange')
# result = session.execute(stmt)
# session.commit()

# Create 
# doctor_strange = Users(name="Doctor Strange", categories="Scott Derrickson", feedback="2016")  
# session.add(doctor_strange)  
# session.commit()

#update
# stmt = update(Users).where(Users.name == 'kirk Strange').values(name = "Some2016Film")
# result = session.execute(stmt)
# session.commit()

# Users.__table__.drop(db)
# base.metadata.create_all(db)    