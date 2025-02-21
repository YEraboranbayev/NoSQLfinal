from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from passlib.context import CryptContext 
from jose import JWTError, jwt 
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["bike_store"]
bikes_collection = db["bikes"]
users_collection = db["users"]
orders_collection = db["orders"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Bike(BaseModel):
    title: str
    price: str
    image: str

class User(BaseModel):
    name: str
    email: str
    password: str
    role: str  # "admin" или "user"

class Order(BaseModel):
    userId: str
    bikeId: str
    status: str  # "pending", "completed", "cancelled"
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.get("/bikes")
def get_bikes():
    bikes = list(bikes_collection.find({}, {"_id": 0})) 
    return {"bikes": bikes}

@app.put("/bikes/{bike_id}")
def update_bike(bike_id: str, bike: Bike):
    result = bikes_collection.update_one({"_id": ObjectId(bike_id)}, {"$set": bike.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Велосипед не найден")
    return {"message": "Велосипед обновлён"}

@app.delete("/bikes/{bike_id}")
def delete_bike(bike_id: str):
    result = bikes_collection.delete_one({"_id": ObjectId(bike_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Велосипед не найден")
    return {"message": "Велосипед удалён"}


@app.get("/users")
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  
    return {"users": users}

@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь обновлён"}

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь удалён"}

@app.get("/orders")
def get_orders():
    orders = list(orders_collection.find())
    for order in orders:
        order["_id"] = str(order["_id"])  # ✅ Преобразуем _id в строку
        order["userId"] = str(order["userId"])
        order["bikeId"] = str(order["bikeId"])
    return {"orders": orders}

@app.put("/orders/{order_id}")
def update_order(order_id: str, order: Order):
    result = orders_collection.update_one({"_id": ObjectId(order_id)}, {"$set": order.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"message": "Заказ обновлён"}

@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    result = orders_collection.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"message": "Заказ удалён"}

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise HTTPException(status_code=401, detail="Ошибка авторизации")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")

@app.post("/register")
def register(user: UserRegister):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    hashed_password = hash_password(user.password)
    user_data = {"name": user.name, "email": user.email, "password": hashed_password, "role": "user"}
    users_collection.insert_one(user_data)
    
    return {"message": "Пользователь зарегистрирован!"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Добро пожаловать, {user['email']}! Ваш уровень доступа: {user['role']}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
