import time
from time import struct_time
from typing import Tuple, Union, Callable

from overload import overload


class TimePeriod(object):
    def __init__(self, period: int, time=None):

        if 0 > period or period > 4:
            raise ValueError("Time period must be between 0 and 4")
        if time is not None:
            if type(time) != Time:
                raise TypeError("Argument 'time' must be a Time instance")
        self.period = period
        self._time = time
        
    def __eq__(self, other) -> bool:
        return self.period == other.period

    def __ne__(self, other) -> bool:
        return self.period != other.period

    def __lt__(self, other) -> bool:
        return self.period < other.period

    def __gt__(self, other) -> bool:
        return self.period > other.period

    def __repr__(self) -> str:
        if self.period == 0:
            return f"TimePeriod(<Night>)"
        if self.period == 1:
            return f"TimePeriod(<Morning>)"
        if self.period == 2:
            return f"TimePeriod(<Noon>)"
        if self.period == 3:
            return f"TimePeriod(<Afternoon>)"

    def __str__(self) -> str:
        if self.period == 0:
            return f"Night"
        if self.period == 1:
            return f"Morning"
        if self.period == 2:
            return f"Noon"
        if self.period == 3:
            return f"Afternoon"

    def __int__(self) -> int:
        return self.period

    def get_start_time(self):
        days = 0
        if self._time is not None:
            g = self._time.gmtime()
            minute = g.tm_min
            second = g.tm_sec
            hour = g.tm_hour
            days = self._time.seconds / 60 / 60 / 24
            days -= hour / 24
            days -= minute / 60 / 24
            days -= second / 60 / 60 / 24
            days = int(days)
        if self.period == 0:
            return Time(days, 0, 0, 0)
        if self.period == 1:
            return Time(days, 6, 0, 0)
        if self.period == 2:
            return Time(days, 12, 0, 0)
        if self.period == 3:
            return Time(days, 18, 0, 0)

    def get_end_time(self):
        days = 0
        if self._time is not None:
            g = self._time.gmtime()
            minute = g.tm_min
            second = g.tm_sec
            hour = g.tm_hour
            days = self._time.seconds / 60 / 60 / 24
            days -= hour / 24
            days -= minute / 60 / 24
            days -= second / 60 / 60 / 24
            days = int(days)
        if self.period == 0:
            return Time(days, 5, 59, 59)
        if self.period == 1:
            return Time(days, 11, 59, 59)
        if self.period == 2:
            return Time(days, 17, 59, 59)
        if self.period == 3:
            return Time(days, 23, 59, 59)
    
    def get_timespan(self):
        return TimeSpan(self.get_start_time(), self.get_end_time())

    def get_period(self):
        return self.period

    @classmethod
    def system_timeperiod(cls):
        return Time.system_time().get_timeperiod()


class TimeLength(object):
    def __init__(self, time: float):
        self._timeLength = time
        
    def sleep(self):
        time.sleep(self._timeLength)
        
    def schedule(self, priority: int, func: Callable, *args, **kwargs):
        import sched
        s = sched.scheduler(time.time, time.sleep)
        s.enter(self._timeLength, priority, func, args, kwargs)
        return s

    def get_seconds(self):
        return self._timeLength

    def get_minutes(self):
        return self._timeLength / 60

    def get_hours(self):
        return self._timeLength / 60 / 60

    def get_days(self):
        return self._timeLength / 60 / 60 / 24

    def get_weeks(self):
        return self.get_days() / 7

    def __str__(self):
        g = time.gmtime(self._timeLength)
        minute = g.tm_min
        second = g.tm_sec
        hour = self._timeLength / 60 / 60
        hour -= minute / 60
        hour -= second / 60 / 60
        hour = int(hour)
        minute = str(minute)
        second = str(second)
        if len(minute) == 1:
            minute = "0" + minute
        if len(second) == 1:
            second = "0" + second
        return f"{hour}:{minute}:{second}"

    def __repr__(self):
        return f"TimeLength(<{self.__str__()}>)"

    def __int__(self):
        return int(self._timeLength)

    def __float__(self):
        return float(self._timeLength)


class TimeSpan(object):
    def __init__(self, time_start, time_end):
        if type(time_start) == int:
            self._start: Time = Time(time_start)
        elif type(time_start) == float:
            self._start: Time = Time(time_start)
        elif type(time_start) == Time:
            self._start: Time = time_start

        if type(time_end) == int:
            self._end: Time = Time(time_end)
        elif type(time_end) == float:
            self._end: Time = Time(time_end)
        elif type(time_end) == Time:
            self._end: Time = time_end
        
    def get_start_time(self):
        return self._start
    
    def get_end_time(self):
        return self._end
    
    def get_timelength(self):
        return TimeLength(self._end.seconds-self._start.seconds)

    def __str__(self):
        return f"{self._start.__str__()} - {self._end.__str__()}"

    def __repr__(self):
        return f"TimeSpan(<{self._start.__str__()}>, <{self._end.__str__()}>)"


class WeekDay(object):
    def __init__(self, wday):
        self._wDay = wday

    def __str__(self):
        if self._wDay == 0:
            return f"Monday"
        if self._wDay == 1:
            return f"Thuesday"
        if self._wDay == 2:
            return f"Wednesday"
        if self._wDay == 3:
            return f"Thursday"
        if self._wDay == 4:
            return f"Friday"
        if self._wDay == 5:
            return f"Saturday"
        if self._wDay == 6:
            return f"Sunday"


class Time(object):
    @overload
    def __init__(self, seconds: float):
        if type(seconds) == int:
            self.seconds = seconds
        elif type(seconds) == float:
            self.seconds = seconds
        
        import time
        self._time = time
            
    @__init__.add
    def __init__(self, timetuple: Union[Tuple, struct_time]):
        import time
        self._time = time
        
        if type(timetuple) == struct_time:
            self.seconds = time.mktime(timetuple)
        elif type(timetuple) == tuple:
            self.seconds = time.mktime(timetuple)
        else:
            try:
                self.seconds = time.mktime(timetuple)
            except TypeError:
                raise TypeError(f"invalid type for argument #0: '{type(timetuple)}' must be float, tuple or structtime")

    @__init__.add
    def __init__(self, days: Union[int, float], hours: Union[int, float], minutes: Union[int, float], seconds: Union[int, float]):
        sec = seconds
        sec += minutes * 60
        sec += hours * 60 * 60
        sec += days * 60 * 60 * 24
        self.seconds = sec
        
        import time
        self._time = time

    @__init__.add
    def __init__(self, day: int, month: int, year: int, hour: int, minute: int, second: int):
        import time
        self._time = time
        
        self.seconds = time.mktime(struct_time((year, month, day, hour, minute, second, -1, -1, -1)))

    def schedule(self, priority, func, *args, **kwargs):
        import sched
        s = sched.scheduler(time.time, time.sleep)
        s.enterabs(self.seconds, priority, func, args, kwargs)
        return s

    def asctime(self):
        return self._time.asctime(self.gmtime())

    def gmtime(self):
        return self._time.gmtime(self.seconds)

    def sleep(self):
        return self._time.sleep(self.seconds)

    def mktime(self):
        return self._time.mktime(self.gmtime())

    def get_hour(self):
        """
        Get number of hours from gmtime

        :return:
        """

        return self.gmtime()[3]

    def get_minute(self):
        """
        Get number of minutes from gmtime

        :return:
        """

        return self.gmtime()[4]

    def get_second(self):
        """
        Get number of seconds from gmtime

        :return:
        """

        return self.gmtime()[5]

    def get_yday(self):
        """
        Get number of days of the year from gmtime

        :return:
        """

        return self.gmtime()[7]

    def get_year(self):
        """
        Get number of years from gmtime

        :return:
        """

        return self.gmtime()[0]

    def get_month(self):
        """
        Get number of months from gmtime

        :return:
        """

        return self.gmtime()[1]

    def get_wday(self):
        """
        Get weekday number of gmtime

        :return:
        """

        return self.gmtime()[6]

    def get_timeperiod(self):
        """
        Returns a time period of the time object

        :return:
        """

        hour = self.get_hour()
        if 0 <= hour < 6:
            return TimePeriod(0, self)
        elif 6 <= hour < 12:
            return TimePeriod(1, self)
        elif 12 <= hour < 18:
            return TimePeriod(2, self)
        elif 18 <= hour < 24:
            return TimePeriod(3, self)

    def get_weekday(self):
        return WeekDay(self.get_wday())

    def is_am(self):
        hour = self.get_hour()
        return 0 <= hour < 12

    def is_pm(self):
        hour = self.get_hour()
        return 12 <= hour < 24

    @classmethod
    def system_time(cls):
        """
        Returns the current system time

        :return:
        """

        return Time(time.time())

    def __repr__(self):
        """
        Returns a string representation of the formatted time

        :return:
        """

        return f"Time(<{self.__str__()}>)"

    def __str__(self):
        """
        Returns a formatted string of the time object

        :return:
        """

        return self.strftime("%d/%m/%Y %H:%M:%S GMT")

    def __int__(self):
        """
        Returns milliseconds of the time object

        :return:
        """

        return int(self.seconds * 1000)

    def strftime(self, format_):
        """
        Returns a formatted string of the time object

        :param format_:
        :return:
        """

        return self._time.strftime(format_, self.gmtime())


NIGHT = TimePeriod(0)
MORNING = TimePeriod(1)
NOON = TimePeriod(2)
AFTERNOON = TimePeriod(3)


if __name__ == '__main__':
    def time_tests():
        print("\n\n--= Time(...) Tests =--")

        time_ = Time(5, 3, 5, 3)
        print(time_.gmtime())
        print(time_.get_timeperiod())

        time_ = Time(5, 7, 6, 42)
        print(time_.get_timeperiod())

        time_ = Time(5, 14, 38, 32)
        print(time_.get_timeperiod())

        time_ = Time(5, 19, 54, 23)
        print(time_.get_timeperiod())

        time_ = Time(4, 3, 2004, 21, 25, 0)
        print(time_)

        time_ = Time.system_time()
        print(time_.get_timeperiod())
        print(time_.get_weekday())
        print(time_)

    def timelength_tests():
        print("\n\n--= TimeLength(...) Tests =--")

        time_l = TimeLength(123456)
        print(repr(time_l))
        print(str(time_l))
        print(int(time_l))
        print(float(time_l))

        def print_test(name):
            print("Hello %s" % name)

        time_l = TimeLength(3)
        time_l.schedule(10, print_test, "World").run()

    def timespan_tests():
        print("\n\n--= TimeSpan(...) Tests =--")

        time_ = Time.system_time()
        time_p = time_.get_timeperiod()
        time_s = time_p.get_timespan()
        print(time_)
        print(time_p)
        print(time_s)
        print(repr(time_s))

        time_ = Time(18000, 12, 0, 0)
        time_p = time_.get_timeperiod()
        time_s = time_p.get_timespan()
        print()
        print(time_)
        print(time_p)
        print(time_s)
        print(repr(time_s))

        time_ = Time(18000, 17, 59, 59)
        time_p = time_.get_timeperiod()
        time_s = time_p.get_timespan()
        print()
        print(time_)
        print(time_p)
        print(time_s)
        print(repr(time_s))

        time1 = Time(17000, 13, 59, 32)
        time2 = Time(18300, 17, 32, 19)
        time_s = TimeSpan(time1, time2)
        time_l = time_s.get_timelength()
        print()
        print(time_s)
        print(time_l)
        print(time_l.get_seconds())

    time_tests()
    timelength_tests()
    timespan_tests()

    import system
    time__ = Time.system_time()

    tts = system.TTS("en")
    tts.pspeak(f"It's {time__.get_weekday()} {str(time__)[:-4]}")
