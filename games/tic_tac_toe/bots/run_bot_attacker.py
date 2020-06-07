import argparse

from bot_attacker import BotAttacker

parser = argparse.ArgumentParser()

parser.add_argument('--id', default=1, type=int)
parser.add_argument('--ip', default="localhost", type=str)
parser.add_argument('--port', default=5050, type=int)
parser.add_argument('--token', default="password", type=str)

args = parser.parse_args()

bot = BotAttacker()
bot.set_auth(args.id, args.token)
bot.connect(args.ip, args.port)
