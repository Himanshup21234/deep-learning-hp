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
        input_content = [message.content]
        print(message.content)
        for text in ['/ai', '/chatgpt', '/bot']:
            # For gpt 4
            if message.attachments:
                for attachment in message.attachments:
                    image_bytes = await attachment.read()
                    input_content.append({"image": image_bytes})
            if input_content[0].startswith(text):
                input_content[0] = input_content[0].replace(text, '')
                response = openai.Completion.create(
                    model="code-cushman-001",
                    temperature=0.7,
                    max_tokens=100,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    prompt=input_content[0]
                )
                assistant_response = response['choices'][0]['text']
                print(assistant_response)
                await message.channel.send(assistant_response)


client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)
