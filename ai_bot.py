import discord
import google.generativeai as genai
from dotenv import load_dotenv
from discord.ext import commands
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!" , intents=intents)

genai.configure(api_key = os.getenv("AI_TOKEN"))
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history = [])

def ask_openai(prompt):
    full_prompt = f"{prompt}\n(Please limit the response to 2000 characters.)"
    response = chat.send_message(full_prompt)

    return response.text

@bot.event
async def on_ready():
    print(f"Hey I'm AI bot {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "Hello":
        await message.channel.send("Hey, how can I help you?")
    elif bot.user.mentioned_in(message):
        prompt = message.content[len("@AI Bot"):].strip()
        response = ask_openai(prompt)
        await message.channel.send(response)
        
bot.run(os.getenv('BOT_TOKEN'))