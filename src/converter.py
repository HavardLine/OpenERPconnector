from datetime import datetime
from dateutil import tz

def utc_to_local(utc_string):
  from_zone = tz.tzutc()
  to_zone = tz.tzlocal()

  # utc = datetime.utcnow()
  utc = datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S')

  # Tell the datetime object that it's in UTC time zone since 
  # datetime objects are 'naive' by default
  utc = utc.replace(tzinfo=from_zone)

  # return local time
  return utc.astimezone(to_zone)
