#!/usr/bin/env python
# coding: utf-8

import os
import discord
import openai
import nest_asyncio


nest_asyncio.apply()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# print(DISCORD_TOKEN,OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


# Class to fetch message intent from discord and send data to Discord after getting generated text from open ai service
class ChatBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} is connected to Discord')

    async def on_message(self, message):
        if message.author == self.user:
            return
        cmd, msg, assistant_response = None, None, "Start by using any one of the following query: \n/hpAi\n/chatGpt\n/hpBot"
        msg = [message.content]
        for text in ['/hpAi', '/chatGpt', '/hpBot']:
            if msg[0].startswith(text):
                msg[0] = msg[0].replace(text, '')
                msg[0] = msg[0].strip()
                cmd = text
        print(cmd, msg)
        if cmd in ['/hpAi', '/chatGpt', '/hpBot']:
            response = openai.Completion.create(
                #                 response = openai.ChatCompletion.create(
                model="code-cushman-001",
                temperature=0.001,
                max_tokens=500,
                top_p=0.005,
                frequency_penalty=0,
                presence_penalty=0,
                prompt=msg[0]
            )
            assistant_response = response['choices'][0]['text']
        await message.channel.send(assistant_response)


client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)
