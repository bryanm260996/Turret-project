import ttyacm
tty= ttyacm.open(1)

print('receiving bunch of data...')
msg= tty.readline()
msg=msg.strip()
items=msg.split(',')

values = [float(item) for item in items]

#for item in values:
#    print(item)
    
max_value = max(values)
min_value= min(values)
average_values= sum(values)/len(values)

print(f"the max value is:{max_value}, the min value is: {min_value}, the avg value is: {average_values}")