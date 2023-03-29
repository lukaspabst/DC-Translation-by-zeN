import os
import discord
import openai


class TranslationBot(discord.Client):

  def __init__(self, *args, **kwargs):
    intents = discord.Intents.default()
    intents.reactions = True
    super().__init__(intents=intents, *args, **kwargs)
    self.reaction_flags = {
      '🇺🇸': 'English',
      '🇨🇳': 'Mandarin Chinese',
      '🇭🇰': 'Cantonese',
      '🇪🇸': 'Spanish',
      '🇧🇩': 'Bengali',
      '🇳🇬': 'Nigerian Pidgin',
      '🇵🇰': 'Punjabi',
      '🇷🇺': 'Russian',
      '🇯🇵': 'Japanese',
      '🇩🇪': 'German',
      '🇺🇦': 'Ukrainian',
      '🇹🇷': 'Turkish',
      '🇫🇷': 'French',
      '🇮🇹': 'Italian',
      '🇵🇭': 'Tagalog',
      '🇻🇳': 'Vietnamese',
      '🇰🇷': 'Korean',
      '🇵🇱': 'Polish',
      '🇷🇴': 'Romanian',
      '🇳🇵': 'Nepali',
      '🇲🇲': 'Burmese',
      '🇳🇱': 'Dutch',
      '🇸🇦': 'Arabic',
      '🇫🇮': 'Finnish',
      '🇨🇦': 'French Canadian',
      '🇨🇿': 'Czech',
      '🇲🇳': 'Mongolian',
      '🇬🇧': 'British English',
      '🇳🇴': 'Norwegian',
      '🇸🇪': 'Swedish',
      '🇺🇾': 'Urdu',
      '🇮🇷': 'Persian',
      '🇬🇷': 'Greek',
      '🇨🇭': 'Swiss German',
      '🇦🇪': 'Arabic (UAE)',
      '🇧🇷': 'Portuguese',
      '🇩🇿': 'Arabic (Algeria)',
      '🇮🇳': 'Hindi',
      '🇵🇹': 'European Portuguese',
      '🇭🇷': 'Croatian',
      '🇮🇪': 'Irish',
      '🇩🇰': 'Danish',
      '🇱🇰': 'Sinhalese',
      '🇸🇰': 'Slovak',
      '🇸🇮': 'Slovenian',
      '🇧🇪': 'Flemish',
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
      description==
      f'\n\n**Original Message:**\n{content[:20]}{"..." if len(content) > 20 else ""}\n\n**Translation:**\n{translated_content}\n\n',
      color=discord.Color.from_rgb(26, 188, 156))

    # Send the embed to a Discord channel
    await message.channel.send(embed=embed, delete_after=60)

  def translate(self, text, target_language):

    try:
      response = openai.Completion.create(
        model="text-davinci-001",
        prompt=f"Translate this text into {target_language}: {text}",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        api_key=os.environ['OPENAI_API_KEY'])

      if response.choices[0].text.strip() == "":
        raise Exception("Translation failed")

      translation = response.choices[0].text.strip()

      # remove leading special characters and whitespace
      while translation and (translation[0].isspace()
                             or not translation[0].isalnum()):
        translation = translation[1:]

      return translation

    except Exception as e:
      print(f"Translation failed: {e}")
      return None


client = TranslationBot()
client.run(os.environ['DISCORD_TOKEN'])
