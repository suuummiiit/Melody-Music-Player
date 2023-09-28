import customtkinter
import tkinterDnD
import os
import vlc
import time
from PIL import Image, ImageTk


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("1000x800")
app.title("Melody Mucic Player")

##############################################################################################################################
cDir = os.getcwd()
folder_name = "audios"
folder = os.path.join(cDir, folder_name)

songs = []
current_song = 0
playing = False
vol = 50

song_name = ""
pPath = os.path.join(cDir, "ui")

ui_size = 50
trackLength = 0
point = 0



for r, d, f in os.walk(folder):
            for file in f:
                file_path = os.path.join(r, file)
                file_path=file_path.replace("C:\\", "C:\\\\")
                songs.append(file_path)



def play(path, st = 0):
    global current_song
    global playing
    global file
    global song_name
    global trackLength
    global t
    global media

    if playing:
         file.stop()
    
    song_name = os.path.basename(path)
    song_name = song_name.replace(".mp3", "")
    nameLabel.configure(text = song_name)

    current_song = songs.index(path)
    playing = True

    # file = vlc.MediaPlayer(path)
    file = vlc.MediaPlayer()
    media = vlc.Media(path)
    media.add_option(f'start-time={st}')
    file.set_media(media)
    file.play()

    time.sleep(0.1)
    trackLength = file.get_length()
    trackLength /= 1000
    trackLength = int(trackLength)

    timeSlider.configure(from_=0, to=trackLength, number_of_steps=trackLength, state="normal")
    timeSlider.set(st)

    volume_slider.configure(state="normal")

    photo =ImageTk.PhotoImage(Image.open(pPath+"\_playing.png").resize((ui_size,ui_size)))
    pl.configure(image=photo)

def pause():
    global playing
    if playing:
        file.pause()
        playing = False
        photo =ImageTk.PhotoImage(Image.open(pPath+"\_play.png").resize((ui_size,ui_size)))
        pl.configure(image=photo)
    else:
        try:
            file.pause()
            playing = True
        except:
            play(songs[0])
            playing = True
        photo =ImageTk.PhotoImage(Image.open(pPath+"\_playing.png").resize((ui_size,ui_size)))
        pl.configure(image=photo)

def previous():
    global current_song
    if current_song == 0:
        current_song = len(songs)-1
    else:
         current_song -= 1
    play(songs[current_song])


def next():
    global current_song
    if current_song == len(songs)-1:
        current_song = 0
    else:
         current_song += 1
    play(songs[current_song])


def volume(var):
    global vol
    vol = volume_slider.get()
    vol = int(vol)
    file.audio_set_volume(vol)
    volLabel.configure(text=str(vol))


def track(val):
        global point

        point = timeSlider.get()
        point = int(point)
        play(songs[current_song], st=point)



def settrack():
    if playing:
        point = timeSlider.get()
        point = int(point)
        point+=1
        timeSlider.set(point)
    app.after(1000, settrack)






##############################################################################################################################

nameFrame = customtkinter.CTkScrollableFrame(master=app, width=1000, height=500)
nameFrame.pack(pady=(20,5), padx=20)

for i,song in enumerate(songs):
    name = os.path.basename(song)
    name = name.replace(".mp3", "")

    b = customtkinter.CTkButton(nameFrame, width=1000, height=50, text=name, command=lambda k = song: play(k))
    b.grid(row=i, column=0, padx=20)



frameV = customtkinter.CTkFrame(master=app, width=200, height=150, fg_color="transparent")
frameV.pack(side="right")

volLabel = customtkinter.CTkLabel(frameV, font=customtkinter.CTkFont(size=15, weight="bold"), text=str(vol))
volLabel.grid(row=0, column=0)

var=customtkinter.StringVar()
volume_slider = customtkinter.CTkSlider(frameV, from_=0, to=100, number_of_steps=100, command=volume, orientation="vertical", progress_color="white", state="disabled")
volume_slider.grid(row=1, column=0, rowspan=3,padx=(10, 10), sticky="ns")


frameN = customtkinter.CTkFrame(master=app, width=800)
frameN.pack(fill="both",padx=20)


nameLabel = customtkinter.CTkLabel(frameN, font=customtkinter.CTkFont(size=20, weight="bold"), text="No track selected")
nameLabel.pack()


frameB = customtkinter.CTkFrame(master=app, width=500, height=150, corner_radius=0, fg_color="transparent")
frameB.pack(pady=(50,40), padx=20)


photo =ImageTk.PhotoImage(Image.open(pPath+"\_previous.png").resize((ui_size,ui_size)))
pv = customtkinter.CTkButton(frameB,image=photo, text="", compound="right", fg_color="transparent", width=0, command=lambda k = song: previous())
pv.grid(row=0, column=0, padx=5)


photo =ImageTk.PhotoImage(Image.open(pPath+"\_play.png").resize((ui_size,ui_size)))
pl = customtkinter.CTkButton(frameB,image=photo, text="", compound="right", fg_color="transparent", width=0, command=lambda k = song: pause())
pl.grid(row=0, column=1, padx=5)


photo =ImageTk.PhotoImage(Image.open(pPath+"\_next.png").resize((ui_size,ui_size)))
pn = customtkinter.CTkButton(frameB,image=photo, text="", compound="right", fg_color="transparent", width=0, command=lambda k = song: next())
pn.grid(row=0, column=2, padx=5)



frameT = customtkinter.CTkFrame(master=app, width=500, corner_radius=0, fg_color="transparent")
frameT.pack(fill="both")

val=customtkinter.StringVar()
timeSlider = customtkinter.CTkSlider(frameT, from_=0, to=1, number_of_steps=100, width=800,progress_color="white", state="disabled")
timeSlider.bind("<ButtonRelease-1>", track)
timeSlider.pack()
timeSlider.set(0)


app.after(1000, settrack)
app.mainloop()