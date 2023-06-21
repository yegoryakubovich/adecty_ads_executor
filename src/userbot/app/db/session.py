from peewee import MySQLDatabase

from core.config import settings

SessionLocal = MySQLDatabase(
    database=settings.MYSQL_DATABASE, host=settings.MYSQL_SERVER, port=settings.MYSQL_PORT,
    user=settings.MYSQL_USER, password=settings.MYSQL_ROOT_PASSWORD,
    charset='utf8mb4', autoconnect=False,
)
