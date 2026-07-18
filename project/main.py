from database import engine,Base ,get_db
from fastapi import FastAPI,Depends,HTTPException
from models import User
from sqlalchemy.orm import Session
from schema import user,profileupdate
from auth import hash_password,verify_password,access_token
from context import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from protected import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"World"}

# creating user account
@app.post("/users/")
def  create_user(user:user,db:Session=Depends(get_db)):
    #Check if user email exists
    if db.query(User).filter(User.email==user.email).first() is not None:
        return {"message": "User with this email already exists"}
    
    password = hash_password(user.password)
    db_user=User(name=user.name,email=user.email,age=user.age,password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#login user and generate access token
@app.post("/user/login")
#def login(user:Userlog_in,db:Session=Depends(get_db)):
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db:Session=Depends(get_db)):  
         
    #get user from database if the email match  
    existing_user=db.query(User).filter(User.email==form_data.username).first()

#what if user not exixst
    if existing_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    
    #verify user password
    if not verify_password(form_data.password,existing_user.password):
        raise HTTPException(status_code=401,detail="Invalid email or password")
    
   
    token = access_token({"sub": str(existing_user.id)})
    return {"access_token": token, "token_type": "bearer"}

#------PROTECTED ROUTES------#



@app.get("/users")
def get_user(user:User = Depends(get_current_user),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user.id).first()
    return user


#verify access token and return user profile
@app.get("/profile")
def profile(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
   user=db.query(User).filter(User.id==user.id).first()
   return {"email": user.email,"username":user.name, "message": f"welcome back {user.name}"}

#retun dashboard for logged in user
@app.patch("/profile_edit")
def dashboard(update :profileupdate, user:User= Depends(get_current_user),db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.id==user.id).first()
     
    #update only files changed by the user
    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    
    return {"message": "profile edited succefully"}

 #removing user by id   
@app.delete("/user")
def del_user(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user.id).first()
    if user is not None:
        db.delete(user)
        db.commit()
        return {"user": user, "message": "User account deleted successfully"}
    else:
        return {"message":"user not found"}




    


