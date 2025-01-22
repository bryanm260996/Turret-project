import ttyacm
tty= ttyacm.open(1)

print('receiving bunch of data...')
msg= tty.readline()
msg=msg.strip()
items=msg.split(',')

values = [float(item) for item in items]

#for item in values:
    #print(item)
    
values_sum=sum(values)
print(f'the sum is {values_sum}')

print('Sending data..')
tty.print(values_sum)