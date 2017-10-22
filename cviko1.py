import re
import string

from collections import Counter


file = open('c:\\Users\\User\\Desktop\\scorelib.txt', encoding="utf8")


r = re.compile('Composer: .*')
yearReg = re.compile('Publication Year: .*')
counter = Counter()
yearCounter = Counter()
ctr = 0
for line in file:
    m = r.match(line)
    year = yearReg.match(line)
    if m:
        ctr = ctr + 1
        line1 = line.split(':')
        line1 = line1[1].strip()
        counter[line1] += 1

    if year:
        line2 = line.split(':')
        line2 = line2[1].strip()
        yearCounter[line2] += 1

print('Composers :', ctr)
for composer, count in counter.items():
    print(composer + ':' + str(count))

for year, count in yearCounter.items():
    print(year + ':' + str(count))
