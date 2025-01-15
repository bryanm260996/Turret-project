import ttyacm
tty= ttyacm.open(1)

print('receiving data...')
msg=tty.readline()
print(f"got: {msg}")

print('Sending data..')
tty.print('hello, I am pico!')

