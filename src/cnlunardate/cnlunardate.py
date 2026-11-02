"""Concrete cnlunardate type.

See https://en.wikipedia.org/wiki/Chinese_calendar.
"""

from datetime import date, timedelta


MIN_YEAR = 1900
MAX_YEAR = 2100
MIN_DATE = date(1900, 1, 31)
MAX_DATE = date(2100, 12, 31)
_MINORDINAL = 693626  # cnlunardate.min.toordinal()
_MAXORDINAL = 767009  # cnlunardate.max.toordinal()


# 2017
#    1     5    1    7     6
# 0001  0101 0001 0111  0110
# |--|  |------------|  |--|
#   ^         ^          ^
#   |         |          There is a leap month and it is June.
#   |         12 bits for each lunar month with 30 days if 1, or 29 days if 0.
#   If there is a leap month, then it has 30 days if 1, or 29 days if 0.
_LUNAR_YEAR_DATA = \
    [0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,  # 1900-1909
     0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,  # 1910-1919
     0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,  # 1920-1929
     0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,  # 1930-1939
     0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,  # 1940-1949
     0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,  # 1950-1959
     0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,  # 1960-1969
     0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,  # 1970-1979
     0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,  # 1980-1989
     0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,  # 1990-1999
     0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,  # 2000-2009
     0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,  # 2010-2019
     0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,  # 2020-2029
     0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,  # 2030-2039
     0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,  # 2040-2049
     0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,  # 2050-2059
     0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,  # 2060-2069
     0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,  # 2070-2079
     0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,  # 2080-2089
     0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,  # 2090-2099
     0x0d520]  # 2100

# 2017
#    0    f    c    2    3    c
# 0000 1111 1100 0010 0011 1100
# 000011111100001 0001    11100
# Year=2017       Month=1 Day=28
_LUNAR_YEAR_FIRST_DAY_IN_SOLAR = \
    [0x0ed83f, 0x0eda53, 0x0edc48, 0x0ede3d, 0x0ee050, 0x0ee244, 0x0ee439, 0x0ee64d, 0x0ee842, 0x0eea36,  # 1900-1909
     0x0eec4a, 0x0eee3e, 0x0ef052, 0x0ef246, 0x0ef43a, 0x0ef64e, 0x0ef843, 0x0efa37, 0x0efc4b, 0x0efe41,  # 1910-1919
     0x0f0054, 0x0f0248, 0x0f043c, 0x0f0650, 0x0f0845, 0x0f0a38, 0x0f0c4d, 0x0f0e42, 0x0f1037, 0x0f124a,  # 1920-1929
     0x0f143e, 0x0f1651, 0x0f1846, 0x0f1a3a, 0x0f1c4e, 0x0f1e44, 0x0f2038, 0x0f224b, 0x0f243f, 0x0f2653,  # 1930-1939
     0x0f2848, 0x0f2a3b, 0x0f2c4f, 0x0f2e45, 0x0f3039, 0x0f324d, 0x0f3442, 0x0f3636, 0x0f384a, 0x0f3a3d,  # 1940-1949
     0x0f3c51, 0x0f3e46, 0x0f403b, 0x0f424e, 0x0f4443, 0x0f4638, 0x0f484c, 0x0f4a3f, 0x0f4c52, 0x0f4e48,  # 1950-1959
     0x0f503c, 0x0f524f, 0x0f5445, 0x0f5639, 0x0f584d, 0x0f5a42, 0x0f5c35, 0x0f5e49, 0x0f603e, 0x0f6251,  # 1960-1969
     0x0f6446, 0x0f663b, 0x0f684f, 0x0f6a43, 0x0f6c37, 0x0f6e4b, 0x0f703f, 0x0f7252, 0x0f7447, 0x0f763c,  # 1970-1979
     0x0f7850, 0x0f7a45, 0x0f7c39, 0x0f7e4d, 0x0f8042, 0x0f8254, 0x0f8449, 0x0f863d, 0x0f8851, 0x0f8a46,  # 1980-1989
     0x0f8c3b, 0x0f8e4f, 0x0f9044, 0x0f9237, 0x0f944a, 0x0f963f, 0x0f9853, 0x0f9a47, 0x0f9c3c, 0x0f9e50,  # 1990-1999
     0x0fa045, 0x0fa238, 0x0fa44c, 0x0fa641, 0x0fa836, 0x0faa49, 0x0fac3d, 0x0fae52, 0x0fb047, 0x0fb23a,  # 2000-2009
     0x0fb44e, 0x0fb643, 0x0fb837, 0x0fba4a, 0x0fbc3f, 0x0fbe53, 0x0fc048, 0x0fc23c, 0x0fc450, 0x0fc645,  # 2010-2019
     0x0fc839, 0x0fca4c, 0x0fcc41, 0x0fce36, 0x0fd04a, 0x0fd23d, 0x0fd451, 0x0fd646, 0x0fd83a, 0x0fda4d,  # 2020-2029
     0x0fdc43, 0x0fde37, 0x0fe04b, 0x0fe23f, 0x0fe453, 0x0fe648, 0x0fe83c, 0x0fea4f, 0x0fec44, 0x0fee38,  # 2030-2039
     0x0ff04c, 0x0ff241, 0x0ff436, 0x0ff64a, 0x0ff83e, 0x0ffa51, 0x0ffc46, 0x0ffe3a, 0x10004e, 0x100242,  # 2040-2049
     0x100437, 0x10064b, 0x100841, 0x100a53, 0x100c48, 0x100e3c, 0x10104f, 0x101244, 0x101438, 0x10164c,  # 2050-2059
     0x101842, 0x101a35, 0x101c49, 0x101e3d, 0x102051, 0x102245, 0x10243a, 0x10264e, 0x102843, 0x102a37,  # 2060-2069
     0x102c4b, 0x102e3f, 0x103053, 0x103247, 0x10343b, 0x10364f, 0x103845, 0x103a38, 0x103c4c, 0x103e42,  # 2070-2079
     0x104036, 0x104249, 0x10443d, 0x104651, 0x104846, 0x104a3a, 0x104c4e, 0x104e43, 0x105038, 0x10524a,  # 2080-2089
     0x10543e, 0x105652, 0x105847, 0x105a3b, 0x105c4f, 0x105e45, 0x106039, 0x10624c, 0x106441, 0x106635,  # 2090-2099
     0x106849]   # 2100


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def _return_int_if_valid(value):
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        raise TypeError("integer argument expected, got float")
    try:
        value = value.__index__()
    except AttributeError:
        pass
    else:
        if not isinstance(value, int):
            raise TypeError(
                f"__index__ returned non-int (type {type(value).__name__})")
        return value
    orig = value
    try:
        value = value.__int__()
    except AttributeError:
        pass
    else:
        if not isinstance(value, int):
            raise TypeError(
                f"__int__ returned non-int (type {type(value).__name__})")
        import warnings
        warnings.warn(f"an integer is required (got type {type(orig).__name__})",
                      DeprecationWarning,
                      stacklevel=2)
        return value
    raise TypeError(
        f"an integer is required (got type {type(value).__name__})")


def _return_bool_if_valid(value):
    if isinstance(value, bool):
        return value
    try:
        value = value.__bool__()
    except AttributeError:
        pass
    else:
        if not isinstance(value, bool):
            raise TypeError(
                f"__bool__ returned non-bool (type {type(value).__name__})")
        return value
    raise TypeError(f"a bool is required (got type {type(value).__name__})")


def _get_bits_in_range_with_shift(bits, range_len, shift):
    return (bits & (((1 << range_len) - 1) << shift)) >> shift


def _leap_month_in_bits(bits):
    return _get_bits_in_range_with_shift(bits, 4, 0)


def _months_in_bits(bits):
    return _get_bits_in_range_with_shift(bits, 12, 4)


def _leap_month_days_in_bits(bits):
    return _get_bits_in_range_with_shift(bits, 4, 16)


def _month_bit_in_months_bits(bits, month):
    return _get_bits_in_range_with_shift(bits, 1, 12 - month)


def _days_in_leapable_month(year, month, isLeapMonth):
    idx = year - MIN_YEAR
    lunar_bits = _LUNAR_YEAR_DATA[idx]
    if isLeapMonth:
        leap_month = _leap_month_in_bits(lunar_bits)
        if leap_month == 0 or leap_month != month:
            raise ValueError(f"month {month} is not leap in {year}")
        else:
            return 30 if _leap_month_days_in_bits(lunar_bits) else 29
    months_bits = _months_in_bits(lunar_bits)
    return 1 if year == MAX_YEAR and month == 12 else 30 if _month_bit_in_months_bits(months_bits, month) else 29


def _check_date_fields(year, month, day, isLeapMonth):
    year = _return_int_if_valid(year)
    month = _return_int_if_valid(month)
    day = _return_int_if_valid(day)
    isLeapMonth = _return_bool_if_valid(isLeapMonth)
    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ValueError(f"year {year} must be in {MIN_YEAR}..{MAX_YEAR}")
    if not 1 <= month <= 12:
        raise ValueError(f"month {month} must be in 1..12")
    dim = _days_in_leapable_month(year, month, isLeapMonth)
    if not 1 <= day <= dim:
        raise ValueError(f"day {day} must be in 1..{dim}")
    return year, month, day, isLeapMonth


def _convert_lunar_first_day_to_solar_by_idx(idx):
    soalr_bits = _LUNAR_YEAR_FIRST_DAY_IN_SOLAR[idx]
    return date(_get_bits_in_range_with_shift(soalr_bits, 15, 9),
                _get_bits_in_range_with_shift(soalr_bits, 4, 5),
                _get_bits_in_range_with_shift(soalr_bits, 5, 0))


def _convert_lunar_year_to_months_by_idx(idx):
    lunar_bits = _LUNAR_YEAR_DATA[idx]
    if_leap_month_has_30_days = _leap_month_days_in_bits(lunar_bits)
    twelve_months_bits = _months_in_bits(lunar_bits)
    leap_month = _leap_month_in_bits(lunar_bits)

    NUM_MONTH_BITS = 12
    months = [(NUM_MONTH_BITS - shift, 30 if ((twelve_months_bits >> shift) & 1)
               else 29, False) for shift in range(NUM_MONTH_BITS - 1, -1, -1)]
    if leap_month:
        months.insert(
            leap_month, (leap_month, 30 if if_leap_month_has_30_days else 29, True))
    return months


def _solar2ymdl(s):
    if s < MIN_DATE or MAX_DATE < s:
        raise ValueError(f"date {s} must be in {MIN_DATE}..{MAX_DATE}")
    idx = s.year - MIN_YEAR
    solar_first_day = _convert_lunar_first_day_to_solar_by_idx(idx)
    if s < solar_first_day:
        idx -= 1
        solar_first_day = _convert_lunar_first_day_to_solar_by_idx(idx)

    # Why +1? To make days diff between 01/01 and 01/01 be 1 not 0
    days_diff = (s - solar_first_day).days + 1
    lunar_months = _convert_lunar_year_to_months_by_idx(idx)
    for i in range(len(lunar_months)):
        if days_diff > lunar_months[i][1]:
            days_diff -= lunar_months[i][1]
        else:
            break
    return solar_first_day.year, lunar_months[i][0], days_diff, lunar_months[i][2]


def _ymdl2solar(y, m, d, l):
    idx = y - MIN_YEAR
    solar_first_day = _convert_lunar_first_day_to_solar_by_idx(idx)
    lunar_months = _convert_lunar_year_to_months_by_idx(idx)
    days_diff = sum(month[1] for month in lunar_months if (month[0] < m) or (
        month[0] == m and month[2] == False and l == True)) + d - 1
    solar = solar_first_day + timedelta(days=days_diff)
    return solar


class cnlunardate:
    """Concrete cnlunardate type.

    Constructors:

    __new__()
    fromsolardate()
    fromtimestamp()
    fromordinal()
    today()

    Operators:

    __repr__, __str__
    __eq__, __le__, __lt__, __ge__, __gt__, __hash__
    __add__, __radd__, __sub__ (add/radd only with timedelta arg)

    Methods:

    tosolardate()
    timetuple()
    toordinal()
    replace()

    weekday()
    isoweekday()
    isocalendar()

    Properties (read-only):
    year, month, day, isLeapMonth
    """
    __slots__ = '_year', '_month', '_day', '_isLeapMonth', '_hashcode'

    def __new__(cls, year, month=None, day=None, isLeapMonth=False):
        """Constructor

        Arguments:

        year, month, day (required, base 1)
        isLeapMonth (default to false)
        """
        if (month is None and
            isinstance(year, (bytes, str)) and len(year) == 5 and
                1 <= ord(year[2:3]) <= 12):
            # Pickle support
            if isinstance(year, str):
                try:
                    year = year.encode('latin1')
                except UnicodeEncodeError:
                    # More informative error message.
                    raise ValueError(
                        "Failed to encode latin1 string when unpickling "
                        "a cnlunardate object. "
                        "pickle.load(data, encoding='latin1') is assumed.")
            self = object.__new__(cls)
            self.__setstate(year)
            self._hashcode = -1
            return self
        year, month, day, isLeapMonth = _check_date_fields(
            year, month, day, isLeapMonth)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._isLeapMonth = isLeapMonth
        self._hashcode = -1
        return self

    # Additional constructors

    @classmethod
    def fromsolardate(cls, s):
        """Construct a cnlunardate from a solar date."""
        return cls(*_solar2ymdl(s))

    @classmethod
    def fromtimestamp(cls, t):
        """Construct a cnlunardate from a POSIX timestamp (like time.time())."""
        return cls.fromsolardate(date.fromtimestamp(t))

    @classmethod
    def fromordinal(cls, n):
        """Construct a cnlunardate from a proleptic Gregorian ordinal."""
        return cls.fromsolardate(date.fromordinal(n))

    @classmethod
    def today(cls):
        """Construct a cnlunardate from date.today()."""
        return cls.fromsolardate(date.today())

    # Conversions to string

    def __repr__(self):
        """Convert to formal string, for repr()."""
        return f"{self.__class__.__module__}."\
            f"{self.__class__.__qualname__}"\
            f"({self._year}, {self._month}, {self._day}, {self._isLeapMonth})"

    __str__ = __repr__

    # Read-only field accessors

    @property
    def year(self):
        """year (1900-2100)"""
        return self._year

    @property
    def month(self):
        """month (1-12)"""
        return self._month

    @property
    def day(self):
        """day (1-30)"""
        return self._day

    @property
    def isLeapMonth(self):
        """isLeapMonth (bool)"""
        return self._isLeapMonth

    # Standard conversions, __eq__, __le__, __lt__, __ge__, __gt__,
    # __hash__ (and helpers)

    def tosolardate(self):
        """Return a solar date for the cnlunardate."""
        return _ymdl2solar(self._year, self._month, self._day, self._isLeapMonth)

    def timetuple(self):
        """Return local time tuple compatible with time.localtime()."""
        return _ymdl2solar(self._year, self._month, self._day, self._isLeapMonth).timetuple()

    def toordinal(self):
        """Return a proleptic Gregorian ordinal for the cnlunardate."""
        return _ymdl2solar(self._year, self._month, self._day, self._isLeapMonth).toordinal()

    def replace(self, year=None, month=None, day=None, isLeapMonth=None):
        """Return a new cnlunardate with new values for the specified fields."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        if isLeapMonth is None:
            isLeapMonth = self._isLeapMonth
        return type(self)(year, month, day, isLeapMonth)

    # Comparisons of cnlunardate objects with other.

    def _cmp(self, other):
        assert isinstance(other, cnlunardate)
        y, m, d, l = self._year, self._month, self._day, self._isLeapMonth
        y2, m2, d2, l2 = other._year, other._month, other._day, other._isLeapMonth
        return _cmp((y, m, d, l), (y2, m2, d2, l2))

    def __eq__(self, other):
        if isinstance(other, cnlunardate):
            return self._cmp(other) == 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, cnlunardate):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, cnlunardate):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, cnlunardate):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, cnlunardate):
            return self._cmp(other) > 0
        return NotImplemented

    def __hash__(self):
        if self._hashcode == -1:
            self._hashcode = hash(self._getstate())
        return self._hashcode

    # Computations

    def __add__(self, other):
        """Add a cnlunardate to a timedelta."""
        if isinstance(other, timedelta):
            o = self.toordinal() + other.days
            if _MINORDINAL <= o <= _MAXORDINAL:
                return type(self).fromordinal(o)
            raise OverflowError("result out of range")
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract two cnlunardates, or a cnlunardate and a timedelta."""
        if isinstance(other, timedelta):
            return self + timedelta(-other.days)
        if isinstance(other, cnlunardate):
            days1 = self.toordinal()
            days2 = other.toordinal()
            return timedelta(days1 - days2)
        return NotImplemented

    def weekday(self):
        """Return day of the week, where Monday == 0 ... Sunday == 6."""
        return (self.toordinal() + 6) % 7

    # Day-of-the-week and week-of-the-year, according to ISO

    def isoweekday(self):
        """Return day of the week, where Monday == 1 ... Sunday == 7."""
        return self.toordinal() % 7 or 7

    def isocalendar(self):
        """Return a 3-tuple containing ISO year, week number, and weekday."""
        return _ymdl2solar(self._year, self._month, self._day, self._isLeapMonth).isocalendar()

    # Pickle support.

    def _getstate(self):
        yhi, ylo = divmod(self._year, 256)
        return bytes([yhi, ylo, self._month, self._day, self._isLeapMonth]),

    def __setstate(self, string):
        yhi, ylo, self._month, self._day, self._isLeapMonth = string
        self._year = yhi * 256 + ylo

    def __reduce__(self):
        return (self.__class__, self._getstate())


cnlunardate.min = cnlunardate(1900, 1, 1)
cnlunardate.max = cnlunardate(2100, 12, 1)
cnlunardate.resolution = timedelta(days=1)
