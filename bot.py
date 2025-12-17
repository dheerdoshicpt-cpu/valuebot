import discord
from discord import app_commands
import json
import os
import dotenv
dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")

def load_items():
    with open("items.json", "r") as f:
        return json.load(f)
async def item_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    items = load_items()
    current = current.lower()

    return [
        app_commands.Choice(name=item, value=item)
        for item in items.keys()
        if current in item.lower()
    ]
  
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
    if item in items:
        data = items[item]
        await interaction.response.send_message(
            f"**{item.title()}**\n"
            f"💰 Value: **{data['value']}**\n"
            f"📈 Demand: **{data['demand']}**\n"
            f"🔥 Overpay: **{data['overpay']}**"
        )
    else:
        await interaction.response.send_message(
            "❌ Item not found.",
            ephemeral=True
        )

if TOKEN:
    client.run(TOKEN)
else:
    print("Token not defined")
