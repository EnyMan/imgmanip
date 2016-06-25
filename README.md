# Imgmanip

Simple tool that's cuts stereoscopic img in half and "hides" additional files in it.

# Usage

imgmanip source file...  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Creates new file `source.secret.jpg` where source is the file that is cut in half  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;file... are files hidden in it  
imgmanip source
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Extracts data from source  
imgmanip -g  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Launches imgmanip in gui form 

# Requirements

+ Python 3+
+ Pillow

# Notes

Created cut image is saved in current working directory.  
Extracted images are also created in current working directory.  
While working from GUI the cut file is saved in the same directory as the original was and extracted files in the same directory as source the source image was.  
Upon extraction the source image is not deleted.