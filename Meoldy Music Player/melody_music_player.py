import customtkinter
import tkinterDnD
import os
import vlc
import time
# from just_playback import Playback
from PIL import Image, ImageTk

# customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
# app.geometry("400x780")
app.geometry("1000x800")
app.title("Melody Mucic Player")

##############################################################################################################################
cDir = os.getcwd()
folder_name = "songs"
folder = os.path.join(cDir, folder_name)

songs = []
current_song = 0
playing = False
vol = 50
song_name = ""

pPath = os.path.join(cDir, "ui")
ui_size = 50



for r, d, f in os.walk(folder):
            for file in f:
                file_path = os.path.join(r, file)
                file_path=file_path.replace("C:\\", "C:\\\\")
                songs.append(file_path)



def play(path):
    global current_song
    global playing
    global file
    global song_name

    if playing:
         file.pause()
    
    song_name = os.path.basename(path)
    song_name = song_name.replace(".mp3", "")
    nameLabel.configure(text = song_name)

    current_song = songs.index(path)
    playing = True
    file = vlc.MediaPlayer(path)
    file.audio_set_volume(vol)
    file.play()
    photo =ImageTk.PhotoImage(Image.open(pPath+"\_playing.png").resize((ui_size,ui_size)))
    pl.configure(image=photo)

def pause():
    global playing
    if playing:
        # print("yes")
        file.pause()
        playing = False
        print(current_song)
        photo =ImageTk.PhotoImage(Image.open(pPath+"\_play.png").resize((ui_size,ui_size)))
        pl.configure(image=photo)
    else:

        # print("no")
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
    #  print(str(var.get()))
    # print(volume_slider.get())
    global vol
    vol = volume_slider.get()
    vol *= 100
    vol = int(vol)
    print(vol)
    file.audio_set_volume(vol)




##############################################################################################################################

frame1 = customtkinter.CTkScrollableFrame(master=app, width=1000, height=500)
frame1.pack(pady=20, padx=20)

for i,song in enumerate(songs):
    
    name = os.path.basename(song)
    name = name.replace(".mp3", "")

    b = customtkinter.CTkButton(frame1, width=1000, height=50, text=name, command=lambda k = song: play(k))
    b.grid(row=i, column=0, padx=20)


frame4 = customtkinter.CTkFrame(master=app, width=200, height=150, corner_radius=0)
frame4.pack(side="right")


var=customtkinter.StringVar()
volume_slider = customtkinter.CTkSlider(frame4, from_=0, to=1, number_of_steps=100, command=volume, orientation="vertical")
volume_slider.grid(row=0, column=3, rowspan=3,padx=(150, 10), sticky="ns")

frame2 = customtkinter.CTkFrame(master=app, width=500, height=50, corner_radius=0)
frame2.pack(pady=(5,20), padx=20, fill="both")

nameLabel = customtkinter.CTkLabel(frame2, font=customtkinter.CTkFont(size=20, weight="bold"), width=200)
nameLabel.grid(row=0, column=4, padx=20, pady=(20, 20))

frame3 = customtkinter.CTkFrame(master=app, width=500, height=150, corner_radius=0)
frame3.pack(side = "left",pady=20, padx=20)



photo =ImageTk.PhotoImage(Image.open(pPath+"\_previous.png").resize((ui_size,ui_size)))
pv = customtkinter.CTkButton(frame3,image=photo, text="", compound="right", fg_color="transparent", width=0, command=lambda k = song: previous())
pv.grid(row=0, column=0, padx=5)


photo =ImageTk.PhotoImage(Image.open(pPath+"\_play.png").resize((ui_size,ui_size)))
pl = customtkinter.CTkButton(frame3,image=photo, text="", compound="right", fg_color="transparent", width=0, command=lambda k = song: pause())
pl.grid(row=0, column=1, padx=5)


photo =ImageTk.PhotoImage(Image.open(pPath+"\_next.png").resize((ui_size,ui_size)))
pn = customtkinter.CTkButton(frame3,image=photo, text="", compound="right", fg_color="transparent", width=0, command=lambda k = song: next())
pn.grid(row=0, column=2, padx=5)

# volume_slider = customtkinter.CTkSlider(frame2)# orientation="vertical"
# # # volume_slider.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
# # volume_slider.grid(row=1, column = 15)


# volLabel = customtkinter.CTkLabel(frame3, font=customtkinter.CTkFont(size=20, weight="bold"), width=800, text=vol)
# volLabel.grid(row=2, column=3, padx=20, pady=5)







app.mainloop()