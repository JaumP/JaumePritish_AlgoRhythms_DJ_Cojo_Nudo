import re
import os
from os import listdir
import numpy as np
import dj_final
from dj_final import song
import time as ti
from datetime import date
import random
import librosa



# dir. of features, songs
# dirfeatures = "/Users/jaume/Desktop/algorhythms_testdata/features"
# dirtracks = "/Users/jaume/Desktop/algorhythms_testdata/tracks"
# seed_folder = "/Users/jaume/Desktop/algorhythms_testdata/seed"

dirfeatures = "./features"
dirtracks = "./tracks"
seed_folder = "./seed"
number_of_songs=5

length_of_songs=(15/number_of_songs+1)*60
time_in_mins_session = 15
taim_secs_session = 15*60
barsfade = 8


files = os.listdir(dirfeatures)


#seed analysis
f=file(seed_folder+"/seed.beat_secs",'rb')
beats_seed=np.loadtxt(f)
f.close()
f=file(seed_folder+"/seed.tempo",'rb')
seed_tempo=np.loadtxt(f)
f.close()
f = file(seed_folder+"/seed.genre",'rb')
seed_genre = f.read()
input_genre = seed_genre
f.close()
seed_song1,sr= librosa.core.load(path=seed_folder+"/seed.mp3",sr=44100,mono=False)

find = re.compile(r"^[^.]*")
c=[re.search(find, l).group(0) for l in files]

genres=[]
d = list(set(c))
e=[]
for name in d:
    files=name+".genre"
    if os.path.isfile(dirfeatures+"/"+files):
        numfile = file(dirfeatures+"/"+files, 'rb')
        genres.append(numfile.read().replace("\n",""))
        numfile.close()
        e.append(name)
indices = [i for i, s in enumerate(genres) if input_genre in s]

f=[]


def find_tempo(audio_list,indices,seed_tempo,no_songs):
    tempos=[]
    for i in indices:
        name=audio_list[i]
        f=file(dirfeatures+"/"+name+".tempo",'rb')
        tempos.append(np.loadtxt(f))
        f.close()
    return abs(np.array(tempos)-seed_tempo).argsort()[:no_songs*2]


gaga=find_tempo(e,indices,seed_tempo,number_of_songs)
gaga=random.sample(gaga,number_of_songs)

# find songs to put into class
gaga2 = []
for l in gaga:
    gaga2.append(e[indices[l]])

# class for each song
def class_listof_songs(listofsongs,length_of_songs):
    sr=44100
    songnameBeats = []
    tempo2 =[]
    genre2=[]
    song2=[]
    arrayed=[]
    for songname in listofsongs:
        f=file(dirfeatures+"/"+songname+".beat_secs",'rb')
        beats=np.loadtxt(f)
        f.close()
        f=file(dirfeatures+"/"+songname+".tempo",'rb')
        tempo=np.loadtxt(f)
        f.close()
        f = file(dirfeatures+"/"+songname+".genre",'rb')
        genre = f.read()
        f.close()
        song1,sr= librosa.core.load(path=dirtracks+"/"+songname+".mp3",sr=sr,mono=False)

        songnameBeats.append(beats)
        tempo2.append(float(tempo))
        genre2.append(genre)
        song2.append(song1)
        class_song=song(song1,tempo,beats,sr,length_of_songs)
        arrayed.append(class_song)
    # return songnameBeats, tempo2, genre2, song2,sr
    return arrayed

baba = class_listof_songs(gaga2,length_of_songs)
baba[0].cut_song(length_of_songs)
baba[0].fade_out(8,baba[1])
baba[0].subidon(baba[2])
baba[0].direct(baba[3])
baba[0].filter_out(8,baba[4])
baba[0].write_song(taim_secs_session,barsfade)
