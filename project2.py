import os
import pandas as pd
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
import datetime
announce_list = []
def audio_frm_txt(txt,file_n):
    """This function Converts text to audio"""
    aud= gTTS(text=str(txt),lang='en',slow=True)
    aud.save(file_n)

def audio_compl(audios):
    """This function returns pydubs audio segment"""
    compile=AudioSegment.empty()
    for audio in audios:
        compile +=AudioSegment.from_mp3(audio)
    return compile

def generate_skel():
    audio= AudioSegment.from_mp3('English_Railway.mp3')
    # 1. Generating "May I have your attention please. Train no.-"
    start=18250
    finish=24000
    audioProcessed= audio[start:finish]
    audioProcessed.export("1_audio.mp3",format="mp3")
    # 2. Train no & name
    # 3. Generating "from"
    start=30090
    finish=31050
    audioProcessed= audio[start:finish]
    audioProcessed.export("3_audio.mp3",format="mp3")
    # 4. from city
    # 5. Generating "to"
    start=31300
    finish=32300
    audioProcessed= audio[start:finish]
    audioProcessed.export("5_audio.mp3",format="mp3")
    # 6. To city
    # # 7. Generating "via"
    # start=33190
    # finish=34090
    # audioProcessed= audio[start:finish]
    # audioProcessed.export("7_audio.mp3",format="mp3")
    # 8. Via City
    # 9. Generating "is arriving shortly on platform no. "
    start=36290
    finish=40300
    audioProcessed= audio[start:finish]
    audioProcessed.export("8_audio.mp3",format="mp3")
    # 10. Platform no.
    # 11.Generating "end music"
    start=41050
    finish=42100
    audioProcessed= audio[start:finish]
    audioProcessed.export("10_audio.mp3",format="mp3")
    

def generate_Announcement(file_n):
    df=pd.read_excel(file_n)
    # print(df)
    global announce_list
    for index,item in df.iterrows():
        # 2.Generating Train no & name 
        audio_frm_txt(item['train_no']+" "+item['train_name'],'2_audio.mp3')
        # 4.Generating from city
        audio_frm_txt(item['from'],'4_audio.mp3')
        # 6.Generating To city
        audio_frm_txt(item['to'],'6_audio.mp3')
        # 8.Generating Via City
        audio_frm_txt("via"+" "+item['via'],'7_audio.mp3')
        # 10.Generating  Platform no.
        audio_frm_txt(item['platform'],'9_audio.mp3')

        audios=[f"{i}_audio.mp3" for i in range(1,11)]

        announcement=audio_compl(audios)
        announcement.export(f"announcement_{index+1}.mp3", format="mp3")
        # brdcast=AudioSegment.from_mp3((f"announcement_{index+1}.mp3")
        # play(brdcast)
        
       
        announce_list.append([f"announcement_{index+1}.mp3",str(item['time'])])


if __name__=="__main__":
    print("Generating Skeleton...")
    generate_skel()
    print("Now Generating Announcement...")
    generate_Announcement("Train_Schedule.xlsx")
    print(announce_list)
    # announce_list=[['announcement_1.mp3', '20:20:00'], ['announcement_2.mp3', '20:24:00'], ['announcement_3.mp3', '20:26:00'], ['announcement_4.mp3', '20:28:00'], ['announcement_5.mp3', '17:05:00']]
    # sound = AudioSegment.from_mp3("announcement_3.mp3")
    # play(sound)
    while True :
        x = datetime.datetime.now().strftime("%H:%M:%S")
        for i in range(len(announce_list)):
            y= announce_list[i][1]
            if y[3:5] not in "00,01,02,03,04":
                temp = y[3:5]
                temp = str(int(temp) -5)
                if len(temp) == 1 :
                    y = str(y[:3]+"0"+temp + y[5:])
                else : 
                    y = str(y[:3]+temp + y[5:])
            else :
                temp1=y[0:2]
                temp1=str(int(temp1)-1)
                temp2=y[3:5]
                temp2=str(60-(5-int(temp2)))
                y=temp1 +":"+temp2 + y[5:]
            print(y, "\n")
            if(x == y):
                sound = AudioSegment.from_mp3(announce_list[i][0])
                play(sound)


