import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from github_issues import get_issues

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def split_into_chunks(text, max_length=1024):
    if not text or len(text) <= max_length:
        return [text]

    chunks = []
    lines = text.split("\n")
    current_chunk = []
    current_length = 0

    for line in lines:
        line_length = len(line) + 1
        if current_length + line_length > max_length:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_length = len(line)
        else:
            current_chunk.append(line)
            current_length += line_length

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks

@bot.event
async def on_ready():
    print(f"Bot is logged as {bot.user}")

@bot.command()
async def kanban(ctx):
    issues = get_issues("open")

    if not issues:
        open_issues_text = "No Issues."
    else:
        lines = [f"#{issue['number']}: {issue['title']}" for issue in issues]
        open_issues_text = "\n".join(lines)

    embed = discord.Embed(
        title="GitHub Kanban Board",
        description="All Open Issues"
    )

    chunks = split_into_chunks(open_issues_text, 1024)

    for i, chunk in enumerate(chunks):
        field_name = f"Open Issues ({len(issues)})" if i == 0 else "More Issues"
        embed.add_field(name=field_name, value=chunk, inline=False)

    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)
