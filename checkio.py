import re
st = 'aaaaa'
#st = 'abcabcabab'
#st = 'abababc'

print(re.findall(r'(.+)\1\1\1\1', st))
print(re.findall(r'(.+)\1\1\1', st))
print(re.findall(r'(.+)\1\1', st))
print(re.findall(r'(.+)\1', st))

# res = ''
# res1 = ''
# sch = 0
# for i in range(len(st)):
#     if i==0:
#         continue
#     for j in range(len(st)-i):
#         if len(st[j:j+i])==len(st[j+i:j+2*i]):
#             if st[j:j+i]==st[j+i:j+2*i]:
#                 if res=='':
#                     res+= st[j:j+i] + st[j+i:j+2*i]
#                     sch = 2
#                 elif res[:i]==st[j+i:j+2*i]:
#                     res+=st[j+i:j+2*i]
#                     sch+=1
#                 else:
#                     res = ''
#                     sch = 0
#             print(st[j:j + i], st[j + i:j + 2 * i], res, sch)
#         else:
#             res = ''
#             sch = 0
#
#
#     res = ''
#     sch = 0

