from pydantic import BaseModel,field_validator, EmailStr
from typing import Optional

class user(BaseModel):
    name: str
    email: EmailStr
    age: int
    password: str

   
    
    #verify age is valid
    @field_validator('age')
    def validate_age(cls,age):
        if age < 18 or age > 100:
            raise ValueError("Age must be above 18 and below 100")
        return age 
    

    #verify password is provided
    @field_validator('password')
    def password_existance(cls,password):
        if password is None:
            raise ValueError("Password is required")
        return password
    
    #verify password is provided and at least 8 characters long
    @field_validator('password')
    def password_length(cls,password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password

    

   
class Userlog_in(BaseModel):
    email: str
    password:str

    #verify email is valid
    @field_validator('email')
    def validate_email(cls,email):
          if '@' not in email:
             raise ValueError("Invalid email address")
          return email
    
    #verify password is provided
    @field_validator('password')
    def password_existance(cls,password):
        if password is None:
            raise ValueError("Password is required")
        return password

class profileupdate(BaseModel):
    email: Optional[str] = None
    name : Optional[str] = None
    age : Optional[str] = None
    class Config:
        form_atrributes=True
        
