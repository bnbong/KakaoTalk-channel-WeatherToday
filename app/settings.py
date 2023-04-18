from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    PG_USER : str = Field(
        default="kakaoweatherbotuser",
        description="PostgreSQL DB Owner's name",
    )
    PG_PASSWORD : str = Field(
        default="kakaoweatherbotpassword",
        description="PostgreSQL DB password",
    )
    PG_HOSTNAME : str = Field(
        default="localhost",
        description="PostgreSQL DB host's name",
    )
    PG_PORT : str = Field(
        default="5432",
        description="PostgreSQL DB hosting port",
    )
    PG_DBNAME : str = Field(
        default="kakaoweatherbotdb",
        description="PostgreSQL DB name",
    )

    class Config:
        env_file = '.env'
