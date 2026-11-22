import discord
import os
from dotenv import load_dotenv
import random

class Question:
    def __init__(self, question, answer, extras):
        self.question = question
        self.answer = answer
        self.extras = extras

    def getInfo(self):
        return self.question, self.answer, self.extras

censored = []

questions = [
    Question("q1", "a1", [1,2,3]),
    Question("q2", "a2", [1,2,3]),
    Question("q3", "a3", [1,2,3])
]
#questions = {"question": "q1", "answer":"a1", "extras":[1,2,3]}


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER = os.getenv("DISCORD_SERVER")


intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


class TriviaButton(discord.ui.View):
    def __init__(self, answerPos):
        super().__init__()
        self.answerPos = answerPos
        self.addButtons()


    def addButtons(self):
        buttons = ["A","B","C","D"]

        async def correct(interaction):
            msg = "Correct"
            if interaction.user.id in censored:
                censored.remove(interaction.user.id)
                msg = msg + "\nYou have been uncensored"
            await interaction.response.edit_message(content=msg, view=None)
        async def incorrect(interaction):
            msg = "Incorrect"
            if interaction.user.id not in censored:
                censored.append(interaction.user.id)
                msg = msg + "\nYou have been censored"
            await interaction.response.edit_message(content=msg, view=None)


        for choice in buttons:
            triviaButton = discord.ui.Button(label=choice, style=discord.ButtonStyle.primary)
            if buttons.index(choice) == self.answerPos:
                triviaButton.callback = correct
            else:
                triviaButton.callback = incorrect
            self.add_item(triviaButton)

@tree.command(
    name="censor",
    description="censor person",
    guild=discord.Object(id=SERVER)
)
async def censor(interaction, target: discord.User):
    targetID = target.id
    if targetID not in censored:
        censored.append(targetID)
    msg = target.name + " has been censored.\nThey must answer a League of Legends trivia question."
    await interaction.response.send_message(msg, silent=True)




@tree.command(
    name="trivia",
    description="league of legends trivia",
    guild=discord.Object(id=SERVER)
)
async def trivia(interaction):
    quiz = random.choice(questions)
    question, answer, extras = quiz.getInfo()

    answers = [answer] + extras
    random.shuffle(answers)
    answerPos = answers.index(answer)

    msg = f'{question}\nA:{answers[0]}\nB:{answers[1]}\nC:{answers[2]}\nD:{answers[3]}'

    await interaction.response.send_message(msg, view=TriviaButton(answerPos), silent=True)


@tree.command(
    name="test",
    description="Test command",
    guild=discord.Object(id=SERVER)
)
async def test(interaction):
    await interaction.response.send_message("test message")

@client.event
async def on_message(message):
    if message.author.id in censored:
        await message.delete()
        await message.channel.send(f"<@{message.author.id}>\nYou are being censored.\nYou must answer a trivia question to be uncensored.")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER))
    print("Ready")


client.run(TOKEN)