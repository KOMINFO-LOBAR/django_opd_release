import os
from PIL import Image
def get_size_format(b,factor=1024,suffix='B'):
	B=suffix;A=factor
	for C in ['','K','M','G','T','P','E','Z']:
		if b<A:return f"{b:.2f}{C}{B}"
		b/=A
	return f"{b:.2f}Y{B}"
def compress_img(image_name,new_size_ratio=0.9,quality=90,width=None,height=None,replace=True):
	J='[+] New Image shape:';H=height;G=width;F=quality;D=new_size_ratio;C=image_name;A=Image.open(C);print('[*] Image shape:',A.size);E=os.path.getsize(C);print('[*] Size before compression:',get_size_format(E))
	if D<1.0:A=A.resize((int(A.size[0]*D),int(A.size[1]*D)),Image.LANCZOS);print(J,A.size)
	elif G and H:A=A.resize((G,H),Image.LANCZOS);print(J,A.size)
	K,L=os.path.splitext(C);B=f"{K}{L}"
	try:A.save(B,quality=F,optimize=True)
	except OSError:A=A.convert('RGB');A.save(B,quality=F,optimize=True)
	print('[+] New file saved:',B);I=os.path.getsize(B);print('[+] Size after compression:',get_size_format(I));M=I-E;print(f"[+] Image size change: {M/E*100:.2f}% of the original image size.")
if __name__=='__main__':
	import argparse;parser=argparse.ArgumentParser(description='Simple Python script for compressing and resizing images');parser.add_argument('image',help='Target image to compress and/or resize');parser.add_argument('-j','--to-jpg',action='store_true',help='Whether to convert the image to the JPEG format');parser.add_argument('-q','--quality',type=int,help='Quality ranging from a minimum of 0 (worst) to a maximum of 95 (best). Default is 90',default=90);parser.add_argument('-r','--resize-ratio',type=float,help='Resizing ratio from 0 to 1, setting to 0.5 will multiply width & height of the image by 0.5. Default is 1.0',default=1.0);parser.add_argument('-w','--width',type=int,help='The new width image, make sure to set it with the `height` parameter');parser.add_argument('-hh','--height',type=int,help='The new height for the image, make sure to set it with the `width` parameter');args=parser.parse_args();print('='*50);print('[*] Image:',args.image);print('[*] Quality:',args.quality);print('[*] Resizing ratio:',args.resize_ratio)
	if args.width and args.height:print('[*] Width:',args.width);print('[*] Height:',args.height)
	print('='*50)