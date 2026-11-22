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


questions = [
    Question("q1", "a1", [1,2,3]),
    Question("q2", "a2", [1,2,3]),
    Question("q3", "a3", [1,2,3])
]


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
            await interaction.response.edit_message(content="correct", view=None)
        async def incorrect(interaction):
            await interaction.response.edit_message(content="incorrect", view=None)


        for choice in buttons:
            triviaButton = discord.ui.Button(label=choice, style=discord.ButtonStyle.primary)
            if buttons.index(choice) == self.answerPos:
                triviaButton.callback = correct
            else:
                triviaButton.callback = incorrect
            self.add_item(triviaButton)



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
    print(answers)

    msg = f'{question}\nA:{answers[0]}\nB:{answers[1]}\nC:{answers[2]}\nD:{answers[3]}'

    await interaction.response.send_message(msg, view=TriviaButton(answerPos))


@tree.command(
    name="test",
    description="Test command",
    guild=discord.Object(id=SERVER)
)
async def test(interaction):
    await interaction.response.send_message("test message")



@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER))
    print("Ready")


client.run(TOKEN)