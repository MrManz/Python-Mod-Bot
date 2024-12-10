from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import discord
from dotenv import load_dotenv
import os
import datetime

global observer

KEYWORDS = ["[JOIN]", "[LEAVE]", "[COMMAND]", "[BAN]"]


def format_message(message):
    splt = message.split("[")
    unix_timestamp = int(datetime.datetime.strptime(splt[0], "%Y-%m-%d %H:%M:%S ").timestamp())
    return f"<t:{unix_timestamp}:f>`{'['.join(splt[1:])}`"


class MyClient(discord.Client):
    async def on_log_updated(self, message):
        channel = self.get_channel(1315700405430128730)
        await channel.send(format_message(message))

    async def on_ready(self):
        channel = self.get_channel(1315700405430128730)

        global observer
        event_handler = MyHandler(self)
        observer.schedule(event_handler, path='/factorio/logs/console.log', recursive=True)
        observer.start()

        await channel.send("Der Log bot arbeitet....")



class MyHandler(FileSystemEventHandler):
    def __init__(self, client):
        self.client = client

    def on_modified(self, event):
        print("File has been modified")
        if not event.is_directory:
            with open('/factorio/logs/console.log') as f:
                for line in f:
                    pass
                last_line = line

            for i in KEYWORDS:
                if i in last_line:
                    client.dispatch("log_updated", last_line)
                    break


            print(last_line)


if __name__ == "__main__":
    observer = Observer()
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = MyClient(intents=discord.Intents.default())
    client.run(TOKEN)
    observer.stop()
    observer.join()
