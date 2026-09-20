from app.core.security import hash_password
from app.models.user import User
from sqlalchemy.orm import Session
class UserRepository:
    def __init__(self):
        self.model=User

    def get(self, db: Session, user_id):        
        return db.get(User, user_id)

    def get_all(self, db: Session):            
        return db.query(User).all()

    def get_by_username(self, db:Session, username:str):
        return db.query(User).filter(User.username==username).first()

    def get_by_id(self, db:Session, user_id):
        return db.query(User).filter(User.user_id== user_id).first()   
    
    def get_all_by_role(self, db:Session, role:str):
        return db.query(User).filter(User.role == role).first()
    
    def create(self, db: Session, data: dict):
        plain_password = data.pop("password", None)
        
        if plain_password:
            data["hashed_password"] = hash_password(plain_password)
        
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: User, data:dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete (self, db: Session, db_obj:User):
        db.delete(db_obj)
        db.commit()
        
    
user_repository=UserRepository()
        
        
        
    
