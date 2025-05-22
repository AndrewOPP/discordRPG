from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DS_",
        env_file_encoding="utf-8",
        extra="allow")


class LoggingConfig(BaseSettings):
    debug: bool = True
    cmd_convert_revert: bool = False


class Config(BaseSettings):
    discord: Settings = Settings()
    logging: LoggingConfig = LoggingConfig()

    @classmethod
    def load(cls) -> "Config":
        return cls()


settings = Config.load()
