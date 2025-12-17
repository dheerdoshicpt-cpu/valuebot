import discord
from discord import app_commands
import json
import os


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def load_items():
    with open("items.json", "r") as f:
        return json.load(f)


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

    return choices[:25]  # Disco

