from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseUser):
    pass

class UserIn(BaseUser):
    password: str

class UserInDB(BaseUser):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user: UserIn):
    hashed_password = fake_password_hasher(raw_password=user.password)
    user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    print("User kind of saved")
    return user_in_db