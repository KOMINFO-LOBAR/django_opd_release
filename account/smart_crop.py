import json,sys
from PIL import Image
from smartcrop import SmartCrop
def smart_crop(inputfile,outputfile,width,height):
	I='RGB';F=height;E=width;D=inputfile;C='top_crop';A=Image.open(D)
	if A.mode not in(I,'RGBA'):sys.stderr.write(f"{A.mode} convert from mode='{D}' to mode='RGB'\n");G=Image.new(I,A.size);G.paste(A);A=G
	J=SmartCrop();B=J.crop(A,width=100,height=int(F/E*100));K=B[C]['x'],B[C]['y'],B[C]['width']+B[C]['x'],B[C]['height']+B[C]['y'];H=A.crop(K);H.thumbnail((E,F),Image.Resampling.LANCZOS);H.save(outputfile,'JPEG',quality=90)