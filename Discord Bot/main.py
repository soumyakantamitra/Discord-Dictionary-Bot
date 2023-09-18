import discord
import os	
import requests
import json
import logging
from keep_alive import keep_alive

intents = discord.Intents().all()
client = discord.Client(intents = intents)

# Configure logging with a relative path for the log file
logging.basicConfig(
    filename='bot_errors.log',  # This creates the log file in your project's directory
    level=logging.ERROR,       # Log only ERROR and higher severity
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	data = json.loads(response.text)
	quote = f"{data[0]['q']}\n -{data[0]['a']}"
	return(quote)

def eng_word_def(word):
	url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
	response = requests.get(url)
	data = json.loads(response.text)
	
	if data and isinstance(data, list) and len(data) > 0:
		first_meaning = data[0].get("meanings", [])
		if first_meaning:
			first_definition = first_meaning[0].get("definitions", [])
			if first_definition:
				return first_definition[0].get("definition", "No definition found.")

def eng_word():
	response = requests.get("https://random-word-api.vercel.app/api?words=1")
	data = json.loads(response.text)
	word = data[0]
	sentence = f"{word}\nDefinition: {eng_word_def(word)}"
	return sentence

@client.event
async def on_error(event, *args, **kwargs):
    # Log the error message
    logging.error(f"An error occurred in event '{event}':", exc_info=True)

@client.event
async def on_ready():
	print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

	msg = message.content
	
	if msg.startswith('$ping'):
		await message.channel.send('Pong!')

	if msg.startswith('$inspire'):
		quote = get_quote()
		await message.channel.send(quote)

	if msg.startswith('$learn'):
		vocab = eng_word()
		await message.channel.send(vocab)

	if msg.startswith('$define'):
		word = msg.split('$define', 1)[1]
		sentence = f"{word}\nDefinition: {eng_word_def(word)}"
		await message.channel.send(sentence)


keep_alive()
try:
	client.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
	print("\nBlocked by discord\n")
	os.system("python restarter.py")
	os.system('kill 1')