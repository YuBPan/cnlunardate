# A Chinese lunar date library for Python 中国农历日期 Python 库

cnlunardate provides a date type for the Chinese lunar calendar, with functionality similar to Python's built-in datetime.date.

## Features

- Construct and manipulate Chinese lunar dates.
- Convert between Chinese lunar dates and Gregorian dates.
- Support leap months.
- Date arithmetic, comparisons, and ordinal conversions.
- Immutable date objects.
- Pickling support.

## Requirements

Python 3.11 or later.

## Installation

```sh
$ python -m pip install cnlunardate
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

## Development

Clone the repository:

```sh
git clone https://github.com/YuBPan/cnlunardate.git
cd cnlunardate
```

Use a virtual environment, install the package and development dependencies:

```sh
python -m venv path/to/venv
source path/to/venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run tests

```sh
python -m pytest
```

## Lint and format checks

python -m ruff check .
python -m ruff format --check .

## License

MIT

## Reference

- [Chinese calendar Wiki](https://en.wikipedia.org/wiki/Chinese_calendar)
- [Hong Kong Observatory – Gregorian-Lunar Calendar Conversion](https://www.hko.gov.hk/tc/gts/time/conversion.htm)
