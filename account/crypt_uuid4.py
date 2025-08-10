_A='-'
import uuid,hashlib,base64
class ClsCryptUuid4:
	mResult='';mSalt='';mData=''
	def left(B,s,amount):
		A=amount
		if A>len(s):return s
		else:return s[:A]
	def right(B,s,amount):
		A=amount
		if A>len(s):return s
		else:return s[-A:]
	def mid(C,s,offset,amount):
		B=amount;A=offset
		if B>len(s):return s
		else:return s[A:A+B]
	def str_to_hex(A,s):return''.join([('0'+hex(ord(A)).split('x')[1])[-2:]for A in s])
	def hex_to_str(A,x):return''.join([chr(int(x[A:A+2],16))for A in range(0,len(x),2)])
	def str_to_bytes(A,b):return bytes.fromhex(''.join([hex(ord(A)).replace('x','0')[-2:]for A in b]))
	def bytes_to_str(A,b):return''.join([chr(A)for A in b])
	def enc_text(B,pText):
		E=uuid.uuid4().hex;D=round(len(E)/4);H=B.left(E,D);I=B.right(E,D);F=H+_A+B.str_to_hex(str(pText))+_A+I;F=B.str_to_bytes(F);A=base64.b64encode(F);A=B.bytes_to_str(A);A=B.str_to_hex(A);D=round(len(A)/8);G='';C=0
		while C<len(A):
			if C%D==0 and C>0:G+=_A
			G+=A[C];C+=1
		return G
	def dec_text(A,pText):
		D=pText.replace(_A,'')
		try:
			C=A.hex_to_str(D);C=A.str_to_bytes(C);B=base64.b64decode(C);B=A.bytes_to_str(B)
			if B.find(_A)>-1:F,E,G=B.split(_A);return A.hex_to_str(str(E))
			else:return''
		except:return''
	def hash_text(B,pText):A=uuid.uuid4().hex;A=B.left(A,4);C=hashlib.sha256(A.encode()+pText.encode()).hexdigest()+_A+A;B.mResult=C;return C
	def check_data(A,hashed_password,user_password):A.hash_text_rm(hashed_password);return A.mData==hashlib.sha256(A.mSalt.encode()+user_password.encode()).hexdigest()
	def hash_text_(E):
		B=[];G,F=E.mResult.split(_A);C=len(F);A=0
		while A<len(G):B.append(E.mid(G,A,C));A+=C
		A=0
		while A<len(F):B.append(E.mid(F,A,C));A+=C
		D='';A=0
		while A<len(B):
			if D!='':D+=_A
			D+=B[A];A+=1
		return D
	def hash_text_rm(B,pData):
		A=pData.split(_A)
		if len(A)>1:
			B.mSalt=A[len(A)-1];D='';C=0
			while C<len(A)-1:D+=A[C];C+=1
			B.mData=D
		else:B.mData='';B.mSalt=''