from machine import RTC

rtc = RTC()
# for 22nd of June 2017 at 10:30am (TZ 0)
rtc.init((2017, 6, 22, 10, 30, 0, 0, 0))
print(rtc.now())
