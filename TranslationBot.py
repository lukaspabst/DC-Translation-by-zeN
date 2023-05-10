import discord
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Coded by zeN

class TranslationBot(discord.Client):

  def __init__(self, *args, **kwargs):
    intents = discord.Intents.default()
    intents.reactions = True
    super().__init__(intents=intents, *args, **kwargs)
    self.reaction_flags = {
      '🇺🇸': 'en',
      '🇨🇳': 'zh-cn',
      '🇭🇰': 'zh-hk',
      '🇪🇸': 'es',
      '🇧🇩': 'bn',
      '🇳🇬': 'pcm',
      '🇵🇰': 'pa',
      '🇷🇺': 'ru',
      '🇯🇵': 'ja',
      '🇩🇪': 'de',
      '🇺🇦': 'uk',
      '🇹🇷': 'tr',
      '🇫🇷': 'fr',
      '🇮🇹': 'it',
      '🇵🇭': 'tl',
      '🇻🇳': 'vi',
      '🇰🇷': 'ko',
      '🇵🇱': 'pl',
      '🇷🇴': 'ro',
      '🇳🇵': 'ne',
      '🇲🇲': 'my',
      '🇳🇱': 'nl',
      '🇸🇦': 'ar',
      '🇫🇮': 'fi',
      '🇨🇦': 'fr-ca',
      '🇨🇿': 'cs',
      '🇲🇳': 'mn',
      '🇬🇧': 'en-gb',
      '🇳🇴': 'no',
      '🇸🇪': 'sv',
      '🇺🇾': 'ur',
      '🇮🇷': 'fa',
      '🇬🇷': 'el',
      '🇨🇭': 'de-ch',
      '🇦🇪': 'ar-ae',
      '🇧🇷': 'pt',
      '🇩🇿': 'ar-dz',
      '🇮🇳': 'hi',
      '🇵🇹': 'pt-pt',
      '🇭🇷': 'hr',
      '🇮🇪': 'ga',
      '🇩🇰': 'da',
      '🇱🇰': 'si',
      '🇸🇰': 'sk',
      '🇸🇮': 'sl',
      '🇧🇪': 'nl-be'
    }

  async def on_ready(self):
    print(f'Logged in as {self.user.name} ({self.user.id})')
    print('------')

  async def on_reaction_add(self, reaction, user):
    if user.bot:
      return

    if reaction.message.author.name == "Translation by zeN":
      return

    print("on_reaction_add called!")
    if reaction.emoji not in self.reaction_flags:
      print("on_reaction_add emoji not in reaction.flags!")
      return

    print(f'Received reaction {reaction.emoji} from user {user.name}')
    print(f'reaction: {reaction.message}')
    message = await reaction.message.channel.fetch_message(reaction.message.id)
    print(f'Message: {message.content}')
    if not message.content:
      print("Message content is empty!")
      return

    content = message.content
    print(self.reaction_flags[reaction.emoji])
    translation = self.translate(content, self.reaction_flags[reaction.emoji])
    translated_content = translation
    print(f'Translated message from {content} to {translated_content}')

    # Create a Discord embed with the gradient as the border color
    embed = discord.Embed(
      title=f'**Author:** {message.author.name}',
      description=
      f'\n\n**Original Message:**\n{content[:20]}{"..." if len(content) > 20 else ""}\n\n**Translation:**\n{translated_content}\n\n',
      color=discord.Color.from_rgb(26, 188, 156))

    # Send the embed to a Discord channel
    await message.channel.send(embed=embed, delete_after=60)

  def translate(self, text, target_language):

    try:
      endpoint = "https://translate.googleapis.com/translate_a/single"
      params = {
          "client": "gtx",
          "sl": "auto",
          "tl": target_language,
          "dt": "t",
          "q": text
      }
      response = requests.get(endpoint, params=params)
      translation = response.json()[0][0][0]

      # remove leading special characters and whitespace
      while translation and (translation[0].isspace()
                             or not translation[0].isalnum()):
        translation = translation[1:]

      return translation

    except Exception as e:
      print(f"Translation failed: {e}")
      return None


client = TranslationBot()
client.run(os.getenv('DISCORD_TOKEN'))
