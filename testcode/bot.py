import telepot
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

telegram_token = "6129613380:AAGbL2T-ogOaIK4v2YTPe4zTD9pzBikKLEA"

# 파일 경로 찾기
def get_dir_list(dir):
    str_list = ""
    if os.path.exists(dir):
        file_list = os.listdir(dir)
        file_list.sort()

        for f in file_list :
            full_path = os.path.join(dir,f)
            if os.path.isdir(full_path):
                f = "[" + f + "]"
            str_list += f
            str_list += "\n"
    str_list.strip()
    return str_list


def handler(msg):
    content_type, chat_Type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True) 

    print(msg)
    
    # if content_type == "text" :
    #     bot.sendMessage(chat_id, "[반사] {}".format(msg["text"]))
    # /dir c:\\workspace (쟈ㅜ)
    if content_type == "text":
        str_message = msg["text"]
        if str_message[0:1] == "/":
            args = str_message.split(" ")
            command = args[0]
            del args[0]

            if command == "/dir" or command == "/목록":
                filepath = " ".join(args)
                if filepath.strip() == " ":
                    bot.sendMessage(chat_id, "/dir [대상폴더]로 입력해주세요.")
       
                else:
                    filelist = get_dir_list(filepath)
                    bot.sendMessage(chat_id,filelist)

            elif command[0:4] == "/get": 
                filepath = " ".join(args)
                if os.path.exists(filepath):
                    try:
                        if command == "/getfile":
                            bot.sendDocument(chat_id, open(filepath, "rb"))
                        elif command == "/getimage":
                            bot.sendPhoto(chat_id, open(filepath, "rb"))
                        elif command == "/getaudio":
                            bot.sendAudio(chat_id, open(filepath, "rb"))
                        elif command == "/getvideo" : #/getvideo c:\test\movie.mp4
                            bot.sendVideo(chat_id, open(filepath, "rb"))
                    except Exception as e:
                        bot.sendMessage(chat_id, "파일 전송 실패 {}".format(e))
                else: 
                    bot.sendMessage(chat_id, "파일이 존재하지 않습니다.")

bot = telepot.Bot(telegram_token)
bot.message_loop(handler,run_forever=True)
