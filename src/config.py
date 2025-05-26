from pydantic_settings import BaseSettings, SettingsConfigDict


class GameConfig(BaseSettings):
    exp_reward_base: int = 20
    exp_coef_reward: float = 1.2

    coin_reward_base: int = 10
    coins_coef_reward_per_lvl: float = 2.5


class DiscordSettings(BaseSettings):
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
    discord: DiscordSettings = DiscordSettings()
    logging: LoggingConfig = LoggingConfig()
    game: GameConfig = GameConfig()

    @classmethod
    def load(cls) -> "Config":
        return cls()


settings = Config.load()
