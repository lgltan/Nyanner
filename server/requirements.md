# Initial Installation
```pip install fastapi python-dotenv sqlalchemy pymysql "python-jose[cryptography]" "passlib[bcrypt]" python-multipart```

# .env
```
DB_URL = "mysql+pymysql://{db_username}:{db_password}@localhost:3306/{db_name}"
SECRET_KEY = "WHY_IS_IT_9AM"
ALGORITHM = "HS256"
```

# Running the server
In ```./server``` run the following command in the terminal:
```fastapi dev main.py```

# Running the server
In ```./client``` run the following command in the terminal:
```npm install```
```npm start```