"""Test cnlunardate."""

import unittest
import pickle

from cnlunardate import cnlunardate
from cnlunardate import MIN_YEAR, MAX_YEAR

from datetime import timedelta

pickle_loads = {pickle.loads, pickle._loads}
pickle_choices = [(pickle, pickle, proto)
                  for proto in range(pickle.HIGHEST_PROTOCOL + 1)]
assert len(pickle_choices) == pickle.HIGHEST_PROTOCOL + 1


class TestCnlunardateOnly(unittest.TestCase):

    def test_delta_non_days_ignored(self):
        dt = cnlunardate(2000, 1, 2)
        delta = timedelta(days=1)
        days = timedelta(delta.days)
        self.assertEqual(days, timedelta(1))

        dt2 = dt + delta
        self.assertEqual(dt2, dt + days)

        dt2 = delta + dt
        self.assertEqual(dt2, dt + days)

        dt2 = dt - delta
        self.assertEqual(dt2, dt - days)

        delta = -delta
        days = timedelta(delta.days)
        self.assertEqual(days, timedelta(-1))

        dt2 = dt + delta
        self.assertEqual(dt2, dt + days)

        dt2 = delta + dt
        self.assertEqual(dt2, dt + days)

        dt2 = dt - delta
        self.assertEqual(dt2, dt - days)


class SubclassDate(cnlunardate):
    sub_var = 1


class TestCnlunardate(unittest.TestCase):

    theclass = cnlunardate

    def test_basic_attributes(self):
        dt = self.theclass(2017, 6, 1, True)
        self.assertEqual(dt.year, 2017)
        self.assertEqual(dt.month, 6)
        self.assertEqual(dt.day, 1)
        self.assertEqual(dt.isLeapMonth, True)

    def test_roundtrip(self):
        for dt in (self.theclass(1900, 1, 1),
                   self.theclass.today()):
            # Verify dt -> string -> cnlunardate identity.
            s = repr(dt)
            self.assertTrue(s.startswith("cnlunardate."))
            s = s[len("cnlunardate."):]
            dt2 = eval(s)
            self.assertEqual(dt, dt2)

            # Verify identity via reconstructing from pieces.
            dt2 = self.theclass(dt.year, dt.month, dt.day)
            self.assertEqual(dt, dt2)

    def test_ordinal_conversions(self):
        # Check some fixed values.
        for y, m, d, n in [(1900, 1, 1, 693626),  # 1900, 1, 31
                           (1945, 10, 8, 710347),  # 1945, 11, 12
                           (2100, 12, 1, 767009)]:  # 2100, 12, 31
            d = self.theclass(y, m, d)
            self.assertEqual(n, d.toordinal())
            fromord = self.theclass.fromordinal(n)
            self.assertEqual(d, fromord)

        # Check first and last days of year spottily across the whole
        # range of years supported.
        for year in range(MIN_YEAR+1, MAX_YEAR+1, 7):
            # Verify (year, 1, 1) -> ordinal -> y, m, d, l is identity.
            d = self.theclass(year, 1, 1)
            n = d.toordinal()
            d2 = self.theclass.fromordinal(n)
            self.assertEqual(d, d2)
            # Verify that moving back a day gets to the end of year-1.
            if year > 1:
                d = self.theclass.fromordinal(n-1)
                try:
                    d2 = self.theclass(year-1, 12, 30)
                except ValueError:
                    d2 = self.theclass(year-1, 12, 29)
                self.assertEqual(d, d2)
                self.assertEqual(d2.toordinal(), n-1)

        # Test every day in a year with and without leap month.
        for year, dim, hasLeapMonth, leapMonth, leapMonthDays in \
                (2017, [29, 30, 29, 30, 29, 29, 29, 30, 29, 30, 30, 30], True, 6, 30), \
                (2018, [29, 30, 29, 30, 29, 29, 30, 29, 30, 29, 30, 30], False, -1, -1):
            n = self.theclass(year, 1, 1).toordinal()
            for month, maxday in zip(range(1, len(dim)+1), dim):
                for day in range(1, maxday+1):
                    d = self.theclass(year, month, day)
                    self.assertEqual(d.toordinal(), n)
                    self.assertEqual(d, self.theclass.fromordinal(n))
                    n += 1
                if hasLeapMonth and month == leapMonth:
                    for day in range(1, leapMonthDays+1):
                        d = self.theclass(year, month, day, True)
                        self.assertEqual(d.toordinal(), n)
                        self.assertEqual(d, self.theclass.fromordinal(n))
                        n += 1

    def test_extreme_ordinals(self):
        a = self.theclass.min
        a = self.theclass(a.year, a.month, a.day)
        aord = a.toordinal()
        b = a.fromordinal(aord)
        self.assertEqual(a, b)

        self.assertRaises(ValueError, lambda: a.fromordinal(aord - 1))

        b = a + timedelta(days=1)
        self.assertEqual(b.toordinal(), aord + 1)
        self.assertEqual(b, self.theclass.fromordinal(aord + 1))

        a = self.theclass.max
        a = self.theclass(a.year, a.month, a.day)
        aord = a.toordinal()
        b = a.fromordinal(aord)
        self.assertEqual(a, b)

        self.assertRaises(ValueError, lambda: a.fromordinal(aord + 1))

        b = a - timedelta(days=1)
        self.assertEqual(b.toordinal(), aord - 1)
        self.assertEqual(b, self.theclass.fromordinal(aord - 1))

    def test_bad_constructor_arguments(self):
        # missing arguments
        self.assertRaises(TypeError, self.theclass)
        self.assertRaises(TypeError, self.theclass, MIN_YEAR)
        self.assertRaises(TypeError, self.theclass, MIN_YEAR, 1)
        # bad years
        self.theclass(MIN_YEAR, 1, 1)
        self.theclass(MAX_YEAR, 1, 1)
        self.assertRaises(ValueError, self.theclass, MIN_YEAR-1, 1, 1)
        self.assertRaises(ValueError, self.theclass, MAX_YEAR+1, 1, 1)
        # bad months
        self.theclass(2017, 1, 1)
        self.theclass(2017, 12, 1)
        self.assertRaises(ValueError, self.theclass, 2017, 0, 1)
        self.assertRaises(ValueError, self.theclass, 2017, 13, 1)
        # bad days
        self.theclass(2017, 1, 29)
        self.theclass(2017, 6, 29)
        self.theclass(2017, 6, 30, True)
        self.assertRaises(ValueError, self.theclass, 2017, 1, 0)
        self.assertRaises(ValueError, self.theclass, 2017, 1, 30)
        self.assertRaises(ValueError, self.theclass, 2017, 6, 30)
        self.assertRaises(ValueError, self.theclass, 2017, 6, 31, True)
        # bad isLeapMonth
        self.theclass(2017, 1, 1)
        self.assertRaises(ValueError, self.theclass, 2017, 1, 1, True)
        self.assertRaises(ValueError, self.theclass, 2017, 6, 30)
        # min and max
        self.theclass(MIN_YEAR, 1, 1)
        self.theclass(MAX_YEAR, 12, 1)
        self.assertRaises(ValueError, self.theclass, MIN_YEAR-1, 12, 30)
        self.assertRaises(ValueError, self.theclass, MAX_YEAR, 12, 2)

    def test_bad_constructor_arguments_typeerror(self):
        # non-expected arguments
        self.assertRaises(TypeError, self.theclass, 2017.0, 1, 1)
        self.assertRaises(TypeError, self.theclass, 2017, 1.0, 1)
        self.assertRaises(TypeError, self.theclass, 2017, 1, 1.0)
        self.assertRaises(TypeError, self.theclass, 2017, 1, 1, "non-bool type")
        # int __index__
        class IntIndex:
            def __init__(self, i):
                self.i = i
            def __index__(self):
                return self.i
        self.theclass(IntIndex(2017), 1, 1)
        self.theclass(2017, IntIndex(1), 1)
        self.theclass(2017, 1, IntIndex(1))
        # non-int __index__
        class NonIntIndex:
            def __index__(self):
                return 1.0
        arg = NonIntIndex()
        self.assertRaises(TypeError, self.theclass, arg, 1, 1)
        self.assertRaises(TypeError, self.theclass, 1, arg, 1)
        self.assertRaises(TypeError, self.theclass, 1, 1, arg)
        # int __int__
        class IntInt:
            def __init__(self, i):
                self.i = i
            def __int__(self):
                return self.i
        self.theclass(IntInt(2017), 1, 1)
        self.theclass(2017, IntInt(1), 1)
        self.theclass(2017, 1, IntInt(1))
        # non-int __int__
        class NonIntInt:
            def __int__(self):
                return 1.0
        arg = NonIntInt()
        self.assertRaises(TypeError, self.theclass, arg, 1, 1)
        self.assertRaises(TypeError, self.theclass, 1, arg, 1)
        self.assertRaises(TypeError, self.theclass, 1, 1, arg)
        # bool __bool__
        class BoolBool:
            def __bool__(self):
                return True
        self.theclass(2017, 6, 1, BoolBool())
        # non-bool __bool__
        class NonBoolBool:
            def __bool__(self):
                return 1.0
        arg = NonBoolBool()
        self.assertRaises(TypeError, self.theclass, 2017, 6, 1, arg)

    def test_hash_equality(self):
        d = self.theclass(2017, 1, 1)
        # same thing
        e = self.theclass(2017, 1, 1)
        self.assertEqual(d, e)
        self.assertEqual(hash(d), hash(e))

        dic = {d: 1}
        dic[e] = 2
        self.assertEqual(len(dic), 1)
        self.assertEqual(dic[d], 2)
        self.assertEqual(dic[e], 2)

        d = self.theclass(2017, 6, 30, True)
        # same thing
        e = self.theclass(2017, 6, 30, True)
        self.assertEqual(d, e)
        self.assertEqual(hash(d), hash(e))

        dic = {d: 1}
        dic[e] = 2
        self.assertEqual(len(dic), 1)
        self.assertEqual(dic[d], 2)
        self.assertEqual(dic[e], 2)

        # different on isLeapMonth
        self.assertNotEqual(hash(self.theclass(2017, 6, 29)),
                            hash(self.theclass(2017, 6, 29, True)))

    def test_computations(self):
        a = self.theclass(2002, 1, 30)
        b = self.theclass(1956, 1, 29)
        c = self.theclass(2001, 2, 1)

        diff = a-b
        self.assertEqual(diff.days, 16803)
        self.assertEqual(diff.seconds, 0)
        self.assertEqual(diff.microseconds, 0)

        day = timedelta(1)
        week = timedelta(7)
        a = self.theclass(2002, 3, 2)
        self.assertEqual(a + day, self.theclass(2002, 3, 3))
        self.assertEqual(day + a, self.theclass(2002, 3, 3))
        self.assertEqual(a - day, self.theclass(2002, 3, 1))
        self.assertEqual(-day + a, self.theclass(2002, 3, 1))
        self.assertEqual(a + week, self.theclass(2002, 3, 9))
        self.assertEqual(a - week, self.theclass(2002, 2, 25))
        self.assertEqual(a + 52*week, self.theclass(2003, 3, 12))
        self.assertEqual(a - 52*week, self.theclass(2001, 3, 22))
        self.assertEqual((a + week) - a, week)
        self.assertEqual((a + day) - a, day)
        self.assertEqual((a - week) - a, -week)
        self.assertEqual((a - day) - a, -day)
        self.assertEqual(a - (a + week), -week)
        self.assertEqual(a - (a + day), -day)
        self.assertEqual(a - (a - week), week)
        self.assertEqual(a - (a - day), day)
        self.assertEqual(c - (c - day), day)

        a = self.theclass(2017, 6, 2, True)
        self.assertEqual(a + day, self.theclass(2017, 6, 3, True))
        self.assertEqual(day + a, self.theclass(2017, 6, 3, True))
        self.assertEqual(a - day, self.theclass(2017, 6, 1, True))
        self.assertEqual(-day + a, self.theclass(2017, 6, 1, True))
        self.assertEqual(a + week, self.theclass(2017, 6, 9, True))
        self.assertEqual(a - week, self.theclass(2017, 6, 24))
        self.assertEqual(a + 52*week, self.theclass(2018, 6, 11))
        self.assertEqual(a - 52*week, self.theclass(2016, 6, 22))
        self.assertEqual((a + week) - a, week)
        self.assertEqual((a + day) - a, day)
        self.assertEqual((a - week) - a, -week)
        self.assertEqual((a - day) - a, -day)
        self.assertEqual(a - (a + week), -week)
        self.assertEqual(a - (a + day), -day)
        self.assertEqual(a - (a - week), week)
        self.assertEqual(a - (a - day), day)
        self.assertEqual(c - (c - day), day)

        # Add/sub ints or floats should be illegal
        for i in 1, 1.0:
            self.assertRaises(TypeError, lambda: a+i)
            self.assertRaises(TypeError, lambda: a-i)
            self.assertRaises(TypeError, lambda: i+a)
            self.assertRaises(TypeError, lambda: i-a)

        # delta - cnlunardate is senseless.
        self.assertRaises(TypeError, lambda: day - a)
        # mixing cnlunardate and (delta or cnlunardate) via * or // is senseless
        self.assertRaises(TypeError, lambda: day * a)
        self.assertRaises(TypeError, lambda: a * day)
        self.assertRaises(TypeError, lambda: day // a)
        self.assertRaises(TypeError, lambda: a // day)
        self.assertRaises(TypeError, lambda: a * a)
        self.assertRaises(TypeError, lambda: a // a)
        # cnlunardate + cnlunardate is senseless
        self.assertRaises(TypeError, lambda: a + a)

    def test_overflow(self):
        tiny = self.theclass.resolution

        for delta in [tiny, timedelta(1), timedelta(2)]:
            dt = self.theclass.min + delta
            dt -= delta  # no problem
            self.assertRaises(OverflowError, dt.__sub__, delta)
            self.assertRaises(OverflowError, dt.__add__, -delta)

            dt = self.theclass.max - delta
            dt += delta  # no problem
            self.assertRaises(OverflowError, dt.__add__, delta)
            self.assertRaises(OverflowError, dt.__sub__, -delta)

    def test_fromtimestamp(self):
        import time

        # Try an arbitrary fixed value.
        ts = time.mktime((1999, 9, 19, 0, 0, 0, 0, 0, -1))
        d = self.theclass.fromtimestamp(ts)
        self.assertEqual(d.year, 1999)
        self.assertEqual(d.month, 8)
        self.assertEqual(d.day, 10)
        self.assertEqual(d.isLeapMonth, False)

    def test_insane_fromtimestamp(self):
        # It's possible that some platform maps time_t to double,
        # and that this test will fail there.  This test should
        # exempt such platforms (provided they return reasonable
        # results!).
        for insane in -1e200, 1e200:
            self.assertRaises(OverflowError, self.theclass.fromtimestamp,
                              insane)

    def test_today(self):
        import time

        # We claim that today() is like fromtimestamp(time.time()), so
        # prove it.
        for dummy in range(3):
            today = self.theclass.today()
            ts = time.time()
            todayagain = self.theclass.fromtimestamp(ts)
            if today == todayagain:
                break
            # There are several legit reasons that could fail:
            # 1. It recently became midnight, between the today() and the
            #    time() calls.
            # 2. The platform time() has such fine resolution that we'll
            #    never get the same value twice.
            # 3. The platform time() has poor resolution, and we just
            #    happened to call today() right before a resolution quantum
            #    boundary.
            # 4. The system clock got fiddled between calls.
            # In any case, wait a little while and try again.
            time.sleep(0.1)

        # It worked or it didn't.  If it didn't, assume it's reason #2, and
        # let the test pass if they're within half a second of each other.
        if today != todayagain:
            self.assertAlmostEqual(todayagain, today,
                                   delta=timedelta(seconds=0.5))

    def test_weekday(self):
        for i in range(7):
            # 2017, 6, 2 is a Monday
            self.assertEqual(self.theclass(2017, 6, 2+i, True).weekday(), i)
            self.assertEqual(self.theclass(
                2017, 6, 2+i, True).isoweekday(), i+1)
            # 2017, 1, 3 is a Monday
            self.assertEqual(self.theclass(2017, 1, 3+i).weekday(), i)
            self.assertEqual(self.theclass(2017, 1, 3+i).isoweekday(), i+1)

    def test_isocalendar(self):
        # Check examples from
        # http://www.phys.uu.nl/~vgent/calendar/isocalendar.htm
        for i in range(7):
            d = self.theclass(2003, 11, 22+i)
            self.assertEqual(d.isocalendar(), (2003, 51, i+1))
            d = self.theclass(2003, 11, 29) + timedelta(i)
            self.assertEqual(d.isocalendar(), (2003, 52, i+1))
            d = self.theclass(2003, 12, 7+i)
            self.assertEqual(d.isocalendar(), (2004, 1, i+1))
            d = self.theclass(2003, 12, 14+i)
            self.assertEqual(d.isocalendar(), (2004, 2, i+1))
            d = self.theclass(2009, 11, 6+i)
            self.assertEqual(d.isocalendar(), (2009, 52, i+1))
            d = self.theclass(2009, 11, 13+i)
            self.assertEqual(d.isocalendar(), (2009, 53, i+1))
            d = self.theclass(2009, 11, 20+i)
            self.assertEqual(d.isocalendar(), (2010, 1, i+1))

    def test_iso_long_years(self):
        from datetime import date

        # Calculate long ISO years and compare to table from
        # http://www.phys.uu.nl/~vgent/calendar/isocalendar.htm
        ISO_LONG_YEARS_TABLE = """
              4   32   60   88
              9   37   65   93
             15   43   71   99
             20   48   76
             26   54   82

            303  331  359  387
            308  336  364  392
            314  342  370  398
            320  348  376
            325  353  381
        """
        iso_long_years = sorted(map(int, ISO_LONG_YEARS_TABLE.split()))
        L = []
        for i in range(101):
            d = self.theclass.fromsolardate(date(MIN_YEAR+i, 12, 31))
            if d.isocalendar()[1] == 53:
                L.append(i + MIN_YEAR - 1600)
            d = self.theclass.fromsolardate(date(2000+i, 12, 31))
            if d.isocalendar()[1] == 53:
                L.append(i)
        self.assertEqual(sorted(L), iso_long_years)

    def test_resolution_info(self):
        self.assertIsInstance(self.theclass.min, cnlunardate)
        self.assertIsInstance(self.theclass.max, cnlunardate)
        self.assertIsInstance(self.theclass.resolution, timedelta)
        self.assertTrue(self.theclass.max > self.theclass.min)

    def test_extreme_timedelta(self):
        big = self.theclass.max - self.theclass.min
        n = (big.days*24*3600 + big.seconds)*1000000 + big.microseconds
        justasbig = timedelta(0, 0, n)
        self.assertEqual(big, justasbig)
        self.assertEqual(self.theclass.min + big, self.theclass.max)
        self.assertEqual(self.theclass.max - big, self.theclass.min)

    def test_from_to_solardate(self):
        from datetime import date

        for y1, m1, d1, y2, m2, d2 in [ (1900, 1, 1, 1900, 1, 31),
                                        (1945, 10, 8, 1945, 11, 12),
                                        (2100, 12, 1, 2100, 12, 31)]:
            d = self.theclass(y1, m1, d1)
            solar = date(y2, m2, d2)
            fromsolar = self.theclass.fromsolardate(solar)
            self.assertEqual(d, fromsolar)
            tosolar = self.theclass.tosolardate(d)
            self.assertEqual(solar, tosolar)

    def test_timetuple(self):
        for i in range(7):
            # January 2, 1956 is a Monday (0)
            d = self.theclass(1955, 11, 20+i)
            t = d.timetuple()
            self.assertEqual(t, (1956, 1, 2+i, 0, 0, 0, i, 2+i, -1))
            # February 1, 1956 is a Wednesday (2)
            d = self.theclass(1955, 12, 20+i)
            t = d.timetuple()
            self.assertEqual(t, (1956, 2, 1+i, 0, 0, 0, (2+i) % 7, 32+i, -1))
            # March 1, 1956 is a Thursday (3), and is the 31+29+1 = 61st day
            # of the year.
            d = self.theclass(1956, 1, 19+i)
            t = d.timetuple()
            self.assertEqual(t, (1956, 3, 1+i, 0, 0, 0, (3+i) % 7, 61+i, -1))
            self.assertEqual(t.tm_year, 1956)
            self.assertEqual(t.tm_mon, 3)
            self.assertEqual(t.tm_mday, 1+i)
            self.assertEqual(t.tm_hour, 0)
            self.assertEqual(t.tm_min, 0)
            self.assertEqual(t.tm_sec, 0)
            self.assertEqual(t.tm_wday, (3+i) % 7)
            self.assertEqual(t.tm_yday, 61+i)
            self.assertEqual(t.tm_isdst, -1)

    def test_pickling(self):
        args = 2015, 11, 27
        orig = self.theclass(*args)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)
        self.assertEqual(orig.__reduce__(), orig.__reduce_ex__(2))

    def test_compat_unpickle(self):
        tests = [
            b"ccnlunardate\ncnlunardate\n(S'\\x07\\xdf\\x0b\\x1b\\x00'\ntR.",
            b"ccnlunardate\ncnlunardate\n(U\x05\x07\xdf\x0b\x1b\x00tR.",
            b"\x80\x02ccnlunardate\ncnlunardate\nU\x05\x07\xdf\x0b\x1b\x00\x85R.",
        ]
        args = 2015, 11, 27
        expected = self.theclass(*args)
        for data in tests:
            for loads in pickle_loads:
                derived = loads(data, encoding="latin1")
                self.assertEqual(derived, expected)

    def test_compare(self):
        t1 = self.theclass(2017, 6, 4)
        t2 = self.theclass(2017, 6, 4)
        self.assertEqual(t1, t2)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 >= t2)
        self.assertFalse(t1 != t2)
        self.assertFalse(t1 < t2)
        self.assertFalse(t1 > t2)

        for args in (2018, 6, 3), (2017, 6, 4, True), (2017, 7, 4), (2017, 6, 5):
            t2 = self.theclass(*args)   # this is larger than t1
            self.assertTrue(t1 < t2)
            self.assertTrue(t2 > t1)
            self.assertTrue(t1 <= t2)
            self.assertTrue(t2 >= t1)
            self.assertTrue(t1 != t2)
            self.assertTrue(t2 != t1)
            self.assertFalse(t1 == t2)
            self.assertFalse(t2 == t1)
            self.assertFalse(t1 > t2)
            self.assertFalse(t2 < t1)
            self.assertFalse(t1 >= t2)
            self.assertFalse(t2 <= t1)

        for badarg in (10, 34.5, "abc", {}, [], ()):
            self.assertEqual(t1 == badarg, False)
            self.assertEqual(t1 != badarg, True)
            self.assertEqual(badarg == t1, False)
            self.assertEqual(badarg != t1, True)

            self.assertRaises(TypeError, lambda: t1 < badarg)
            self.assertRaises(TypeError, lambda: t1 > badarg)
            self.assertRaises(TypeError, lambda: t1 >= badarg)
            self.assertRaises(TypeError, lambda: badarg <= t1)
            self.assertRaises(TypeError, lambda: badarg < t1)
            self.assertRaises(TypeError, lambda: badarg > t1)
            self.assertRaises(TypeError, lambda: badarg >= t1)

    def test_mixed_compare(self):
        our = self.theclass(2000, 4, 5)

        # Our class can be compared for equality to other classes
        self.assertEqual(our == 1, False)
        self.assertEqual(1 == our, False)
        self.assertEqual(our != 1, True)
        self.assertEqual(1 != our, True)

        # But the ordering is undefined
        self.assertRaises(TypeError, lambda: our < 1)
        self.assertRaises(TypeError, lambda: 1 < our)

        # Repeat those tests with a different class

        class SomeClass:
            pass

        their = SomeClass()
        self.assertEqual(our == their, False)
        self.assertEqual(their == our, False)
        self.assertEqual(our != their, True)
        self.assertEqual(their != our, True)
        self.assertRaises(TypeError, lambda: our < their)
        self.assertRaises(TypeError, lambda: their < our)

    def test_bool(self):
        # All cnlunardates are considered true.
        self.assertTrue(self.theclass.min)
        self.assertTrue(self.theclass.max)

    def test_replace(self):
        cls = self.theclass
        args = [2017, 6, 5, False]
        base = cls(*args)
        self.assertEqual(base, base.replace())

        i = 0
        for name, newval in (("year", 2018),
                             ("month", 7),
                             ("day", 6),
                             ("isLeapMonth", True)):
            newargs = args[:]
            newargs[i] = newval
            expected = cls(*newargs)
            got = base.replace(**{name: newval})
            self.assertEqual(expected, got)
            i += 1

        base = cls(2016, 1, 30)
        # Day is out of bounds.
        self.assertRaises(ValueError, base.replace, year=2017)
        # IsLeapMonth is wrong.
        self.assertRaises(ValueError, base.replace, isLeapMonth=True)

    def test_subclass_replace(self):
        class DateSubclass(self.theclass):
            pass

        dt = DateSubclass(2012, 1, 1)
        self.assertIs(type(dt.replace(year=2013)), DateSubclass)

    def test_subclass_cnlunardate(self):

        class C(self.theclass):
            theAnswer = 42

            def __new__(cls, *args, **kws):
                temp = kws.copy()
                extra = temp.pop("extra")
                result = self.theclass.__new__(cls, *args, **temp)
                result.extra = extra
                return result

            def newmeth(self, start):
                return start + self.year + self.month

        args = 2003, 4, 14

        dt1 = self.theclass(*args)
        dt2 = C(*args, **{"extra": 7})

        self.assertEqual(dt2.__class__, C)
        self.assertEqual(dt2.theAnswer, 42)
        self.assertEqual(dt2.extra,  7)
        self.assertEqual(dt1.toordinal(), dt2.toordinal())
        self.assertEqual(dt2.newmeth(-7), dt1.year + dt1.month - 7)

    def test_subclass_alternate_constructors(self):
        from datetime import datetime, date, time

        # Test that alternate constructors call the constructor
        class DateSubclass(self.theclass):
            def __new__(cls, *args, **kwargs):
                result = self.theclass.__new__(cls, *args, **kwargs)
                result.extra = 7
                return result

        args = (2003, 3, 13)
        d_date = date(2003, 4, 14)  # Equivalent solar date
        d_ord = 731319              # Equivalent ordinal

        base_d = DateSubclass(*args)
        self.assertIsInstance(base_d, DateSubclass)
        self.assertEqual(base_d.extra, 7)

        # Timestamp depends on time zone, so we'll calculate the equivalent here
        ts = datetime.combine(d_date, time(0)).timestamp()

        test_cases = [
            ("fromsolardate", (d_date,)),
            ("fromordinal", (d_ord,)),
            ("fromtimestamp", (ts,)),
        ]

        for constr_name, constr_args in test_cases:
            for base_obj in (DateSubclass, base_d):
                # Test both the classmethod and method
                with self.subTest(base_obj_type=type(base_obj),
                                  constr_name=constr_name):
                    constr = getattr(base_obj, constr_name)

                    dt = constr(*constr_args)

                    # Test that it creates the right subclass
                    self.assertIsInstance(dt, DateSubclass)

                    # Test that it's equal to the base object
                    self.assertEqual(dt, base_d)

                    # Test that it called the constructor
                    self.assertEqual(dt.extra, 7)

    def test_pickling_subclass_date(self):
        args = 2006, 7, 23
        orig = SubclassDate(*args)
        for pickler, unpickler, proto in pickle_choices:
            green = pickler.dumps(orig, proto)
            derived = unpickler.loads(green)
            self.assertEqual(orig, derived)
