import numpy as np

import librosa
import os

from scipy.io.wavfile import write

import seaborn
seaborn.set(style='ticks')

import scipy
import time as ti
from datetime import date



class song(object):
    def __init__(self,audio,tempo,beat_times,sr,length_of_songs):
        self.audio_left=audio[0,:]
        self.audio_right=audio[1,:]
        self.tempo=tempo
        self.beat_times=beat_times
        self.length_of_songs=length_of_songs
        self.sr=sr
        bars=[]
        for i in range(len(self.beat_times)/4-1):
            bars.append([beat_times[i*4],beat_times[(i+1)*4]])
        self.bars=np.array(bars)

    def cut_song(self,time_in_secs):
        idx = (np.abs(self.bars[:,1]-time_in_secs)).argmin()
        self.bars=self.bars[:idx+1,:]
        self.audio_left=self.audio_left[:int(self.bars[-1][1]*self.sr)]
        self.audio_right=self.audio_right[:int(self.bars[-1][1]*self.sr)]



    def fade_out(self,nob,song2):
        song2.change_temp(self.tempo)
        song2.cut_song(self.length_of_songs)
        fader_l=self.audio_left[int(self.bars[-nob-1][1]*self.sr):]
        fader_r=self.audio_right[int(self.bars[-nob-1][1]*self.sr):]
        fader=np.arange(float(len(fader_l)))/float(len(fader_l))
        fader_l=fader_l*fader[::-1]
        fader_r=fader_r*fader[::-1]
        haha=song2.audio_left[int(song2.beat_times[0]*self.sr):int(song2.beat_times[0]*self.sr)+len(self.audio_left[int(self.bars[-nob-1][1]*self.sr):])]*fader

        self.audio_left[int(self.bars[-nob-1][1]*self.sr):]=fader_l+haha

        self.audio_left=np.concatenate((self.audio_left,song2.audio_left[len(haha):]))

        haha=song2.audio_right[int(song2.beat_times[0]*self.sr):int(song2.beat_times[0]*self.sr)+len(self.audio_right[int(self.bars[-nob-1][1]*self.sr):])]*fader

        self.audio_right[int(self.bars[-nob-1][1]*self.sr):]=fader_r+haha

        self.audio_right=np.concatenate((self.audio_right,song2.audio_right[len(haha):]))
        tempo, beats = librosa.beat.beat_track(y=self.audio_left, sr=self.sr)
        self.beat_times=librosa.frames_to_time(beats, sr=self.sr)
        bars=[]
        for i in range(len(self.beat_times)/4-1):
            bars.append([self.beat_times[i*4],self.beat_times[(i+1)*4]])
        self.bars=np.array(bars)
    # def change_temp():

    def filter_out(self,nob,song2):
        song2.change_temp(self.tempo)
        song2.cut_song(self.length_of_songs)
        l=scipy.signal.firwin( numtaps=10, cutoff=300, nyq=self.sr/2)
        h=-l
        h[10/2]=h[10/2]+1
        fader_l=self.audio_left[int(self.bars[-nob-1][1]*self.sr):]
        fader_r=self.audio_right[int(self.bars[-nob-1][1]*self.sr):]
        fader=np.arange(float(len(fader_l)))/float(len(fader_l))
        fader_l=scipy.signal.lfilter(l,1.0,fader_l*fader[::-1])
        fader_r=scipy.signal.lfilter(l,1.0,fader_r*fader[::-1])
        haha=scipy.signal.lfilter(h,1.0,(song2.audio_left[int(song2.beat_times[0]*self.sr):int(song2.beat_times[0]*self.sr)+len(self.audio_left[int(self.bars[-nob-1][1]*self.sr):])]*fader))

        self.audio_left[int(self.bars[-nob-1][1]*self.sr):]=fader_l+haha

        self.audio_left=np.concatenate((self.audio_left,song2.audio_left[len(haha):]))

        haha=scipy.signal.lfilter(h,1.0,(song2.audio_right[int(song2.beat_times[0]*self.sr):int(song2.beat_times[0]*self.sr)+len(self.audio_right[int(self.bars[-nob-1][1]*self.sr):])]*fader))

        self.audio_right[int(self.bars[-nob-1][1]*self.sr):]=fader_r+haha

        self.audio_right=np.concatenate((self.audio_right,song2.audio_right[len(haha):]))
        tempo, beats = librosa.beat.beat_track(y=self.audio_left, sr=self.sr)
        self.beat_times=librosa.frames_to_time(beats, sr=self.sr)
        bars=[]
        for i in range(len(self.beat_times)/4-1):
            bars.append([self.beat_times[i*4],self.beat_times[(i+1)*4]])
        self.bars=np.array(bars)


    def subidon(self,song2):
        song2.change_temp(self.tempo)
        song2.cut_song(self.length_of_songs)
        beat1_left=self.audio_left[int(self.bars[-1,0]*self.sr):int(self.bars[-1,1]*self.sr)]
        beat1_right=self.audio_right[int(self.bars[-1,0]*self.sr):int(self.bars[-1,1]*self.sr)]
        beat2_left=beat1_left[:len(beat1_left)/4]
        beat3_left=beat2_left[:len(beat2_left)/2]
        beat4_left=beat3_left[:len(beat3_left)/2]
        beat5_left=beat4_left[:len(beat4_left)/2]
        self.audio_left=np.concatenate((self.audio_left,np.tile(beat1_left,3),np.tile(beat2_left,8),np.tile(beat3_left,16),np.tile(beat4_left,16),np.zeros(len(beat1_left[:int(len(beat1_left)/2)])),song2.audio_left[int(song2.beat_times[0]*self.sr):]))
        beat2_right=beat1_right[:len(beat1_right)/4]
        beat3_right=beat2_right[:len(beat2_right)/2]
        beat4_right=beat3_right[:len(beat3_right)/2]
        beat5_right=beat4_right[:len(beat4_right)/2]
        self.audio_right=np.concatenate((self.audio_right,np.tile(beat1_right,3),np.tile(beat2_right,8),np.tile(beat3_right,16),np.tile(beat4_right,16),np.zeros(len(beat1_left[:int(len(beat1_left)/2)])),song2.audio_left[int(song2.beat_times[0]*self.sr):]))
        tempo, beats = librosa.beat.beat_track(y=self.audio_left, sr=self.sr)
        self.beat_times=librosa.frames_to_time(beats, sr=self.sr)
        bars=[]
        for i in range(len(self.beat_times)/4-1):
            bars.append([self.beat_times[i*4],self.beat_times[(i+1)*4]])
        self.bars=np.array(bars)

    def change_temp(self,tempo2):
        ratio=tempo2/self.tempo
        write("temp.wav",self.sr*ratio,self.audio_left)
        self.audio_left,sr = librosa.core.load(path="temp.wav",sr=self.sr,mono=True)
        write("temp.wav",self.sr*ratio,self.audio_right)
        self.audio_right,sr = librosa.core.load(path="temp.wav",sr=self.sr,mono=True)
        os.remove("temp.wav")
        tempo, beats = librosa.beat.beat_track(y=self.audio_left, sr=self.sr)
        self.beat_times=librosa.frames_to_time(beats, sr=self.sr)
        bars=[]
        for i in range(len(self.beat_times)/4-1):
            bars.append([self.beat_times[i*4],self.beat_times[(i+1)*4]])
        self.bars=np.array(bars)
        self.tempo=tempo2

    def direct(self,song2):
        song2.change_temp(self.tempo)
        song2.cut_song(self.length_of_songs)
        self.audio_left=np.concatenate((self.audio_left[:int(self.beat_times[-1]*self.sr)],song2.audio_left[int(song2.beat_times[0]*self.sr):]))
        self.audio_right=np.concatenate((self.audio_right[:int(self.beat_times[-1]*self.sr)],song2.audio_right[int(song2.beat_times[0]*self.sr):]))
        tempo, beats = librosa.beat.beat_track(y=self.audio_left, sr=self.sr)
        self.beat_times=librosa.frames_to_time(beats, sr=self.sr)
        bars=[]
        for i in range(len(self.beat_times)/4-1):
            bars.append([self.beat_times[i*4],self.beat_times[(i+1)*4]])
        self.bars=np.array(bars)

    def write_song(self,time_session,nob):

        #cut at "time_session" mins
        idx = (np.abs(self.bars[:,1]-time_session)).argmin()
        self.bars=self.bars[:idx+1,:]
        self.audio_left=self.audio_left[:int(self.bars[-1][1]*self.sr)]
        self.audio_right=self.audio_right[:int(self.bars[-1][1]*self.sr)]

        # fade out
        fader_l=self.audio_left[int(self.bars[-nob-1][1]*self.sr):]
        fader_r=self.audio_right[int(self.bars[-nob-1][1]*self.sr):]
        fader=np.arange(float(len(fader_l)))/float(len(fader_l))
        fader_l=fader_l*fader[::-1]
        fader_r=fader_r*fader[::-1]

        self.audio_left=np.concatenate((self.audio_left,fader_l[:]))
        self.audio_right=np.concatenate((self.audio_right,fader_r[:]))



        #write wav
        today =  ti.strftime('%Y%m%d')
        today2 = today[2:8]
        time = ti.strftime('%H%M%S')
        fafa=np.array([self.audio_left,self.audio_right]).T
        write("music_output_"+today2+"_"+time+".wav",44100,fafa)
