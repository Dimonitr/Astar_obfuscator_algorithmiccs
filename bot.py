import os
import telebot
from urllib.request import urlretrieve
import subprocess

BOT_TOKEN = '<BOT_TOKEN>' #Placeholder for the Telegram bot token

bot = telebot.TeleBot(BOT_TOKEN, num_threads=40)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi!\n\n Send me a picture and a quality of the output (in range 1-10).")

@bot.message_handler(content_types=['photo'])
def image_time(message):
    data = urlretrieve(bot.get_file_url(message.photo[2].file_id))
    downscale = 10
    try:
        print(message.caption)
        downscale = int(message.caption)
        if downscale in range(1, 11):
          downscale *= 10
          bot.reply_to(message, "On it 🦾🪄...")
        else:
          downscale = 10
          bot.reply_to(message, "Ehh, you failed to just give me a correct number🙄... (Now, it will be obfuscated with lowest quality)")
    except:
        if message.caption != None:
            bot.reply_to(message, "Ehh, you failed to just give me a number🙄... (Now, it will be obfuscated with lowest quality)")
        else:
            bot.reply_to(message, "On it 🦾🪄...")
    in_file = open(data[0], "rb") # opening for [r]eading as [b]inary
    data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close() 
    
    out_file = open(str(message.chat.id)+str(message.message_id)+".jpg", "wb") # open for [w]riting as [b]inary
    out_file.write(data)
    out_file.close()

    subprocess.run(["python", "artist.py", "--image", str(message.chat.id)+str(message.message_id)+".jpg", "--downscale", str(downscale)])

    in_file = open(str(message.chat.id)+str(message.message_id)+".jpg", "rb") # opening for [r]eading as [b]inary
    data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    os.remove(str(message.chat.id)+str(message.message_id)+".jpg")
    bot.send_photo(message.chat.id, data, reply_to_message_id=message.message_id)

bot.infinity_polling()