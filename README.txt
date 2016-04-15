-------------------------------------------------------------------------------
Documentation:
-------------------------------------------------------------------------------

DJ_Cojo_nudo takes a seed file as input and outputs into the seed folder
a .WAV file with a session that sounds like a professional mix done by a DJ.
A different mix is output every time the program is run.

The program has been tested on MacBook Pro with OSX 10.11.3(El Capitan) and
Python 2.7.11

The following libraries are used:
- librosa
- numpy
- scipy
- seaborn
- time
- datetime
- re
- os
- random

Apart from Librosa, the libraries listed here are standard and should be
installed on most systems
------------------------------------------------------------------------------
INSTRUCTIONS:
------------------------------------------------------------------------------
1) The files in the zip folder should be placed in the same directory as the
   directories "./seed", "./features" and "./tracks"
2) Open terminal
3) Go to the workspace folder (folder with dj_final.py, RunMe.py)
4) Run """python RunMe.py"""
5) A file named "music_output_yymmdd_hhmmss.wav" will be written by the program.
6) If there is any error regarding the input directories, please change lines
   19 - 21 of the "RunMe.py" file, to point to the corresponding directories.

------------------------------------------------------------------------------
AUTHORS
------------------------------------------------------------------------------
DJ_Cojo_nudo was made by Jaume Parera and Pritish Chandna of Universitat Pompeu
Fabra, Barcelona, Spain. For any doubts, questions or feedback, the
aforementioned can be contacted at:

jaume.parera01@estudiant.upf.edu
pritish.chandna01@estudiant.upf.edu

------------------------------------------------------------------------------
LICENCE:
------------------------------------------------------------------------------
DJ_Cojo_nudo is (not) copyright (c) 2016 by DJ_Cojo_nudo Team.
This copyright notice applies to all documents in the source code
archive, except as otherwise noted (mostly in the lib-src subdirectories).
