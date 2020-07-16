a="102.3E23,VDC"

where=a.find(',')
print(where)      #where is ','

i=0
for i in range(0, where):
    print (a[i],end='')
    i=i+1
