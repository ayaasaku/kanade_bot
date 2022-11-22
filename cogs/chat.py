from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
bot = ChatBot(
    'Kanade',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database_uri='sqlite:///database.sqlite3'
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.chinese')
while True:
    try:
        bot_input = bot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break