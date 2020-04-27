import pytz
from tzlocal import get_localzone
from datetime import datetime

dt = datetime.today()
local = str(get_localzone())
print(local)
print(type(local))
print(pytz.timezone(str(get_localzone())).localize(datetime(dt.year,dt.month,dt.day,10)))