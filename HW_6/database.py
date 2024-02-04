import databases
import sqlalchemy
from passlib.hash import bcrypt

DATABASE_URL = "sqlite:///store.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128), unique=True),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

products = sqlalchemy.Table("products", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("title", sqlalchemy.String(50)),
                            sqlalchemy.Column("description", sqlalchemy.String(300)),
                            sqlalchemy.Column("price", sqlalchemy.Float)
                            )

orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
                          sqlalchemy.Column("prod_id", sqlalchemy.ForeignKey("products.id")),
                          sqlalchemy.Column("date", sqlalchemy.DateTime),
                          sqlalchemy.Column("status", sqlalchemy.String(20))
                          )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

try:
    metadata.create_all(engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")