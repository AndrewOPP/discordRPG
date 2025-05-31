from discord import Embed, Colour


def create_embed(user, title: str, description: str, colour: Colour = Colour.dark_green()):
    embed = Embed(
        title=title,
        description=description,
        colour=colour)
    embed.set_author(name=f"Сосунок - {user.name}", icon_url=user.avatar)
    embed.set_footer(text="- Убивай или тебя будут теребить в дыру")
    return embed


def create_start_embed(user, role):
    return create_embed(
        user,
        title="🏟️ Арена Гоблинов",
        description=f"`{user.name}`, ты уже есть в наших рядах. Твое призвание - {role.name}!?")


def create_profile_create_embed(user):
    return create_embed(
        user,
        title="🏟️ Арена Гоблинов",
        description=f"`{user.name.capitalize()}`, ты ступаешь на окровавленный песок перед ареной...\n"
                    "Перед тобой - мертвые останки зеленых тварей, кажется кто-то хорошо потрудился.\n\n"
                    "Готов стать следующим goblin-slayer?")


def create_run_embed(user):
    return create_embed(
        user,
        title="🏳️ Позорный Побег!",
        description=f"`{user.name.capitalize()}` в панике сбежал с поля боя, спасая свою шкуру от противника!\n\n"
                    "Толпа освистывает труса, а гоблины смеются до икоты.\n"
                    "Ты не получаешь ни монет, ни опыта. Только стыд...",
        colour=Colour.dark_gray())
