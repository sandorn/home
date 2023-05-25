from enum import Enum, unique


@unique
class Weekday(Enum):
    Sun = 'aaa'  # Sun的value被设定为0
    Mon = 'bbb'
    Tue = 'ccc'


for name, member in Weekday.__members__.items():
    print(name, '=>', member, ',', member.value)

print(Weekday.Mon.value)
print(Weekday.Sun.value)
