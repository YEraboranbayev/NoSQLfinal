# NoSQLfinal
# 🚴 Bike Store API

## 📌 Project Description
Bike Store API is a web application for managing a bicycle store.  
It includes **user authentication, order processing, and MongoDB integration**.

## 🎯 Features
✔ User registration and login (JWT).  
✔ Bicycle management (CRUD: add, update, delete).  
✔ Order creation and management.  
✔ Cloud database integration (MongoDB Atlas).  
✔ Backend deployment on Render.  

---

## ⚡ 1️⃣ Installation & Setup

### 🔹 1. Install Python (if not installed)
```bash
python --version
```
Python **3.7 or later** is required.  

### 🔹 2. Install Dependencies
```bash
git clone <repository_url>
cd <project_folder>
python -m venv venv
source venv/bin/activate  # For macOS/Linux
# For Windows: venv\Scriptsctivate
pip install -r requirements.txt
```

### 🔹 3. Set up MongoDB Atlas & `.env` file
Create a `.env` file and add:
```env
MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/bike_store?retryWrites=true&w=majority"
SECRET_KEY="supersecretkey"
```

### 🔹 4. Start FastAPI server
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
👉 API available at **`http://127.0.0.1:8000/docs`** (Swagger UI).  

---

## 📊 2️⃣ Database Schema

### 📌 `users` (Users)
| Field    | Type     | Description        |
|----------|---------|--------------------|
| `_id`    | ObjectId | Unique ID         |
| `name`   | String   | User's name       |
| `email`  | String   | Unique email      |
| `password` | String | Hashed password   |
| `role`   | String   | `admin` or `user` |

### 📌 `bikes` (Bicycles)
| Field   | Type     | Description     |
|---------|---------|-----------------|
| `_id`   | ObjectId | Unique ID       |
| `title` | String   | Bicycle name    |
| `price` | String   | Price           |
| `image` | String   | Image URL       |

### 📌 `orders` (Orders)
| Field    | Type     | Description         |
|----------|---------|---------------------|
| `_id`    | ObjectId | Unique ID         |
| `userId` | ObjectId | User's ID         |
| `bikeId` | ObjectId | Bicycle's ID      |
| `status` | String   | `pending`, `completed`, `cancelled` |

---

## 🔗 3️⃣ API Endpoints

### 🔹 Users (`users`)
- `POST /register` — Register a new user
- `POST /login` — User login (JWT)
- `GET /users` — List users (**admin only**)
- `DELETE /users/{id}` — Delete user (**admin only**)

### 🔹 Bicycles (`bikes`)
- `GET /bikes` — Get all bicycles
- `POST /bikes` — Add a bicycle (**admin only**)
- `PUT /bikes/{id}` — Update a bicycle (**admin only**)
- `DELETE /bikes/{id}` — Delete a bicycle (**admin only**)

### 🔹 Orders (`orders`)
- `GET /orders` — Get user orders (**admin sees all**)
- `POST /orders` — Create an order
- `PUT /orders/{id}` — Update order status (**admin only**)
- `DELETE /orders/{id}` — Delete an order (**admin only**)

---

## 🚀 4️⃣ Deployment

### 🔹 Backend (FastAPI) → Render
1. Create an account at [Render](https://dashboard.render.com)
2. Add a new web service (`New Web Service`)
3. Connect your repository and set the start command:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 10000
   ```
4. Add environment variables:
   ```env
   MONGO_URI="mongodb+srv://..."
   SECRET_KEY="your-secret-key"
   ```
5. Click **Deploy** 🚀

### 🔹 Database → MongoDB Atlas
1. Create an account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Add **M0 Free Tier** cluster
3. Allow `0.0.0.0/0` in **Network Access**
4. Copy the **MongoDB URI** and paste it into `.env`

### 🔹 Frontend → GitHub Pages / Netlify
1. Upload `index.html`, `login.html`, `script.js` to GitHub
2. Enable **GitHub Pages** in `Settings → Pages`
3. Get a link: `https://your-username.github.io/bike-store/`

---

## 📜 5️⃣ Logging
Logs are stored in the console and a `logs.txt` file.  
They help track:  
✔ Errors during response generation.  
✔ Request processing times.  
✔ MongoDB interactions.  

---

## 🔧 6️⃣ Possible Improvements
- ✅ Support for multiple languages  
- ✅ Advanced search and order filtering  
- ✅ Improved API security (rate limiting)  
- ✅ Optimization for large datasets  

---

## 👥 7️⃣ Authors
Developed by **Boranbayev Yersultan and Samodelkov Maksym**  

---

## 📜 8️⃣ License
This project is licensed under the **MIT License**.  
