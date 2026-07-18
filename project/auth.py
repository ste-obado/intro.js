from datetime import datetime, timedelta
from passlib import context
from jose import jwt, JWTError

from context import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

# Define the password hashing context
pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

#hash password
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

#verify password
def verify_password(password:str,hashed_password:str) -> bool:
    return pwd_context.verify(password,hashed_password)

#TOKENS
#creating access tokens
def access_token(data:dict)-> str:
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_access_token(token:str)->dict:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print("payload",payload)
        return payload
    except JWTError as e:
        print(e)
        return None

