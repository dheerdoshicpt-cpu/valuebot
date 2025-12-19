import discord
from discord import app_commands
import yaml
import os
import dotenv

# DO NOT REMOVE
dotenv.load_dotenv()

CONFIG_FILE = "items.yml"


def load_items() -> dict:
    """
    Loads item data from YAML config.
    """
    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}


async def item_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    items = load_items().keys()
    current = current.lower()
    choices = []

    for item in items:
        if current in item.lower():
            choices.append(
                app_commands.Choice(name=item, value=item)
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


@client.tree.command(
    name="value",
    description="Get the value of an item"
)
@app_commands.describe(item="Item name (example: cursed volc)")
@app_commands.autocomplete(item=item_autocomplete)
async def value_command(
    interaction: discord.Interaction,
    item: str
):
    items = load_items()

    if item not in items:
        await interaction.response.send_message(
            "❌ Item not found.",
            ephemeral=True
        )
        return

    data = items[item]

    await interaction.response.send_message(
        f"**{item.title()}**\n"
        f"💰 Value: **{data.get('value', 'N/A')}**\n"
        f"📈 Demand: **{data.get('demand', 'N/A')}**\n"
        f"🔥 Overpay: **{data.get('overpay', 'N/A')}**"
    )


# DO NOT REMOVE
TOKEN = os.getenv("TOKEN")
if TOKEN:
    client.run(TOKEN)
else:
    print("Token not defined")
