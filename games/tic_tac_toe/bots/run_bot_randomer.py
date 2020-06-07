import argparse

from bot_randomer import BotRandomer

parser = argparse.ArgumentParser()

parser.add_argument('--id', default=1, type=int)
parser.add_argument('--ip', default="localhost", type=str)
parser.add_argument('--port', default=5050, type=int)
parser.add_argument('--token', default="password", type=str)

args = parser.parse_args()

bot = BotRandomer()
bot.set_auth(args.id, args.token)
bot.connect(args.ip, args.port)
