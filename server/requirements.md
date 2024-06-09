# Initial Installation
```pip install fastapi python-dotenv sqlalchemy pymysql```

# .env
```DB_URL = "mysql+pymysql://{db_username}:{db_password}@localhost:3306/{db_name}"```

# Running the server
In ```./server``` run the following command in the terminal:
```fastapi dev main.py```