# A Chinese lunar date Python library 中国农历日期 Python 库

[![Build Status](https://travis-ci.org/YuBPan/cnlunardate.svg?branch=master)](https://travis-ci.org/YuBPan/cnlunardate)
[![codecov](https://codecov.io/gh/YuBPan/cnlunardate/branch/master/graph/badge.svg)](https://codecov.io/gh/YuBPan/cnlunardate)

## Installation

```console
$ pip install cnlunardate
```

## Usage

Basic operations:

```python
>>> from cnlunardate import cnlunardate

>>> # Basic constructors
>>> cnlunardate(2017, 6, 1) # 4th attribute defaults to False (month is not leap)
cnlunardate.cnlunardate(2017, 6, 1, False)
>>> cnlunardate(2017, 6, 1, True) # (month is leap)
cnlunardate.cnlunardate(2017, 6, 1, True)

>>> # Conversions from/to solar date
>>> from datetime import date
>>> d = cnlunardate.fromsolardate(date(2017, 6, 24))
>>> d
cnlunardate.cnlunardate(2017, 6, 1, False)
>>> d.tosolardate()
datetime.date(2017, 6, 24)
```

Other supported operations as datetime.date (including pickling):

```python
>>> d = cnlunardate.fromordinal(736504) # 736504th day after 0001, 1, 1
>>> d
cnlunardate.cnlunardate(2017, 6, 1, False)
>>> d.toordinal()
736504

>>> # A cnlunardate object is immutable; all operations produce a new object
>>> d.replace(year=2018)
cnlunardate.cnlunardate(2018, 6, 1, False)
>>> d.replace(isLeapMonth=True)
cnlunardate.cnlunardate(2017, 6, 1, True)

>>> d
cnlunardate.cnlunardate(2017, 6, 1, False)
>>> d.weekday() # 0 = Monday
5
>>> d.isoweekday() # 1 = Monday
6
>>> t = d.timetuple()
>>> for i in t:
...     print(i)
...
2017            # year
6               # month
24              # day
0
0
0
5               # weekday (0 = Monday)
175             # 175th day in the year
-1
>>> ic = d.isocalendar()
>>> for i in ic:
...     print(i)
...
2017            # ISO year
25              # ISO week number
6               # ISO day number ( 1 = Monday )

>>> today = cnlunardate.today()
>>> today
cnlunardate.cnlunardate(2019, 11, 22, False)
>>> import time
>>> today == cnlunardate.fromtimestamp(time.time())
True

>>> cnlunardate.min
cnlunardate.cnlunardate(1900, 1, 1, False)
>>> cnlunardate.max
cnlunardate.cnlunardate(2100, 12, 1, False)
```

Errors:

```python
>>> cnlunardate(2101, 1, 1)
ValueError: year 2101 must be in 1900..2100
>>> cnlunardate(2017, 13, 1)
ValueError: month 13 must be in 1..12
>>> cnlunardate(2017, 1, 30)
ValueError: day 30 must be in 1..29
>>> cnlunardate(2017, 1, 1, True)
ValueError: month 1 is not leap in 2017

>>> from datetime import timedelta
>>> cnlunardate.min - timedelta(days=1)
OverflowError: result out of range
>>> cnlunardate.max + timedelta(days=1)
OverflowError: result out of range

>>> cnlunardate("Hello")
TypeError: an integer is required (got type str)
```

## Testing

```console
$ pytest

```

## License

MIT

## Reference

- [Chinese calendar Wiki](https://en.wikipedia.org/wiki/Chinese_calendar)
- [公曆與農曆對照表 - 香港天文台](https://www.hko.gov.hk/tc/gts/time/conversion.htm)
