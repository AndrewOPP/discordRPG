import asyncio
from random import randint
import discord
from discord import ButtonStyle, Interaction, InteractionResponse
from discord.ui import View, Button
from src.models.battle import BattleManager, Battle
from src.ui.create_embeds import create_start_embed, create_run_embed
from src.ui.run_view import RunView


class NextFightView(View):
    """Кнопка для Продолжения боя/побега на поле битвы"""
    def __init__(self, battle_manager: BattleManager):
        super().__init__()
        self.battle_manager: BattleManager = battle_manager
        self.battle: Battle = battle_manager.battle

    @discord.ui.button(label="Следующий бой!", style=ButtonStyle.red)
    async def clb_next_fight_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        await self.battle_manager.next_fight()
        await response.edit_message(embed=self.battle_manager.battle.create_embed_battle(), view=FightView(self.battle_manager))

    @discord.ui.button(label="Уйти.", style=ButtonStyle.gray)
    async def clb_quit_button(self, inter: Interaction, button: Button):
        ...


class FightView(View):
    """Кнопка для атаки/побега на поле битвы"""
    def __init__(self, battle_manager: BattleManager):
        super().__init__()
        self.battle_manager: BattleManager = battle_manager
        self.battle: Battle = battle_manager.battle

    @discord.ui.button(label="Атака", style=ButtonStyle.red)
    async def clb_attack_button(self, inter: Interaction, button: Button):
        # TODO: Чтобы реакция была только от того кто автор сообщения
        response: InteractionResponse = inter.response

        self.battle.player_attack(button)
        await response.edit_message(embed=self.battle.create_embed_battle(), view=self)
        if not self.battle.end_fight:
            progres_bar = ["▱ " for _ in range(5)]
            for i in range(len(progres_bar)):
                progres_bar[i] = "▰ "
                await inter.message.edit(embed=self.battle.create_embed_battle(progres_bar), view=self)
                await asyncio.sleep(randint(2, 6) / 10)

            self.battle.enemy_attack(button)
            await inter.message.edit(embed=self.battle.create_embed_battle(), view=self)

        if self.battle.end_fight:
            reward = self.battle.generate_fight_reward()
            end_embed = self.battle.create_embed_finish_battle(**reward)
            await self.battle.player.save_user(**reward)
            await inter.message.edit(embed=end_embed, view=NextFightView(self.battle_manager))

    @discord.ui.button(label="Побег с позором", style=ButtonStyle.gray)
    async def clb_run_button(self, inter: Interaction, button: Button):
        response: InteractionResponse = inter.response

        await self.battle.player.save_user()
        embed = create_run_embed(inter.user)
        await response.edit_message(embed=embed, view=RunView())


