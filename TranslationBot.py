import os
import discord
import openai
from dotenv import load_dotenv

class TranslationBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.reaction_flags = {'🇩🇪': 'de', '🇫🇷': 'fr', '🇬🇧': 'en', '🇷🇺': 'ru', '🇮🇹': 'it'}

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

    async def on_reaction_add(self, reaction, user):
        if user == self.user: # Ignore reactions made by the bot itself
            return
        if reaction.emoji not in self.reaction_flags: # Ignore reactions with unsupported flag emojis
            return
        message = reaction.message
        content = message.content
        translation = self.translate(content, self.reaction_flags[reaction.emoji])
        translated_content = translation
        await message.channel.send(f'**Original Message:** {content}\n**Translation:** {translated_content}', delete_after=45)

    def translate(self, text, target_language):
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Translate this text into {target_language}: {text}",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        translation = response.choices[0].text.strip()
        return translation
