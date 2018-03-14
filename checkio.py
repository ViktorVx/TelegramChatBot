import re
st = 'aa'

l1 = 1
res = 1
for i in range(1,len(st)):
    if st[i]==st[i-1]:
        l1+=1
    else:
        if l1>res:
            res = l1
            l1 = 0

print(res)
