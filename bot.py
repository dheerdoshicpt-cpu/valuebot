import discord
from discord import app_commands
import json
import os
import dotenv
from data import Database, Item

# DO NOT REMOVE
dotenv.load_dotenv()


async def item_autocomplete(interaction: discord.Interaction,current: str):
    current = current.lower()
    choices = []

    for item in Database().items:
        if current.lower() in item.name:
            choices.append(
                app_commands.Choice(name=item.name, value=item.name)
            )
    
    return choices[:25]

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Bot synced & ready")

client = MyClient()

@client.tree.command(name="value", description="Get the value of an item")
@app_commands.describe(item="Item name (example: cursed volc)")
@app_commands.autocomplete(item=item_autocomplete)
async def value_command(interaction: discord.Interaction, item: str):
    db = Database()
    
    item_obj = db.get_item(item)
    if item_obj:
        await interaction.response.send_message(
            f"**{item_obj.name}**\n"
            f"💰 Value: **{item_obj.value}**\n"
            f"📈 Demand: **{item_obj.demand}**\n"
            f"🔥 Overpay: **{item_obj.overpay}**"
        )
    else:
        await interaction.response.send_message(
            "❌ Item not found.",
            ephemeral=True
        )

# DO NOT REMOVE
TOKEN = os.getenv("TOKEN")
if TOKEN:
    client.run(TOKEN)
else:
    print("Token not defined")
