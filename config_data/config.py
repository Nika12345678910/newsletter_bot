from dataclasses import dataclass
from environs import Env


@dataclass
class Database:
    user: str
    password: str
    host: str
    port: str
    database: str


    def create_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"



@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    db: Database


def load_config(path: str|None = None):
    env = Env()
    Env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=Database(
            user=env("USER"),
            password=env("PASSWORD"),
            host=env("HOST"),
            port=env("PORT"),
            database=env("DATABASE")
        )
    )