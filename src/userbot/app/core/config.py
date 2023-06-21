from pydantic import BaseSettings


class Settings(BaseSettings):
    MYSQL_SERVER: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
