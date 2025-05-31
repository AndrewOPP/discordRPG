from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponse
from src.logs import getLogger
from src.models.user import User
from src.models.role import Role
from src.ui.start_view import StartFightView
from src.ui.profile_view import CreateProfileView
from src.ui.create_embeds import create_start_embed, create_profile_create_embed

logger = getLogger(__name__)


class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Cog {self.__class__.__name__} is loaded")

    @app_commands.command(name="start", description="Начни путешествие и трахни гоблинов")
    async def cmd_start(self, inter: Interaction):
        response: InteractionResponse = inter.response
        user = await User.load(inter.user.id)

        if not user:
            embed = create_profile_create_embed(inter.user)
            await response.send_message(embed=embed, view=CreateProfileView())

        else:
            role = await Role.load(user.role)
            embed = create_start_embed(inter.user, role)
            await response.send_message(embed=embed, view=StartFightView())


async def setup(bot: commands.Bot):
    await bot.add_cog(StartCog(bot))
