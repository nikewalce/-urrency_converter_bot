import os
from currency_bot import CurrencyBot
from dotenv import load_dotenv

def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    if not token:
        raise EnvironmentError("Не найден TOKEN в переменных окружениях")

    bot = CurrencyBot(token)
    bot.run()

if __name__ == "__main__":
    main()