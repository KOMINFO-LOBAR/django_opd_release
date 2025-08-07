from PIL import Image
import os
def resize_width_to(filepath,width):B=filepath;C=width;A=Image.open(B);D=C/float(A.size[0]);E=int(float(A.size[1])*float(D));A=A.resize((C,E),Image.Resampling.LANCZOS);A.save(B)
def create_thumbnail(filepath,thumbpath,thumbnail_width=500,thumbnail_height=300,background=None):
	M='RGB';L='RGBA';K='transparent';I=thumbpath;C=background;B=thumbnail_height;A=thumbnail_width
	with Image.open(filepath)as J:
		G,H=J.size
		if G>H:D=A;E=int(H*D/G)
		else:E=B;D=int(G*E/H)
		N=(A-D)//2;O=(B-E)//2;F=Image.new(L if C==K else M,(A,B))
		if isinstance(C,(list,tuple))and len(C)==3:F.paste(Image.new(M,(A,B),tuple(C)),(0,0))
		elif C==K:F=Image.new(L,(A,B),(0,0,0,0))
		F.paste(J.resize((D,E),Image.ANTIALIAS),(N,O));F.save(I);return os.path.exists(I)