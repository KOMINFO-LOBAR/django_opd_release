import calendar,datetime
def get_last_day_of_month(year,month):return calendar.monthrange(year,month)[1]
def add_months(sourcedate,months):B=sourcedate;A=B.month-1+months;C=B.year+A//12;A=A%12+1;D=min(B.day,get_last_day_of_month(C,A));return datetime.datetime(C,A,D)
def get_week_date(year,month,day):
	A=calendar.Calendar();A=A.monthdatescalendar(year,month);E=False;D=0
	for D in range(0,len(A)-1):
		for F in A[D]:
			if F.day==day:E=True;break
		if E:break
	B=A[D][0];B=datetime.datetime(B.year,B.month,B.day,0,0,0);C=A[D][6];C=datetime.datetime(C.year,C.month,C.day,23,59,59);return B,C