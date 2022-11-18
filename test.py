from datetime import datetime,timedelta
from django_opd.commonf import get_natural_datetime as g
print('---')
for i in range(0,33):a=datetime.now()-timedelta(days=i);print(g(a))
print('---')
for i in range(0,33):a=datetime.now()-timedelta(weeks=i);print(g(a))