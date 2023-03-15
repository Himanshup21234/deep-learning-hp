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
        #print(message.content)
        msg = [message.content]
        # For gpt 4
        # if message.attachments:
        #     for attachment in message.attachments:
        #         image_bytes = await attachment.read()
        #         msg.append({"image": image_bytes})

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
                # gpt-3.5-turbo,text-curie-001, code-cushman-001, code-davinci-002,text-davinci-003
                temperature=0.1,
                max_tokens=100,
                top_p=0.05,
                frequency_penalty=0,
                presence_penalty=0,
                prompt=msg[0]
                #                             message=[{"role":"user","content":input_content}]
            )
            #                 assistant_response = response['choices'][0]['message']['content']
            assistant_response = response['choices'][0]['text']
        #         print(assistant_response)
        await message.channel.send(assistant_response)


client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)
