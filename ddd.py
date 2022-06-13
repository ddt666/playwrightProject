from datetime import datetime
s = 'screenshot{}.png'.format(datetime.now().strftime("%H-%M-%S"))
print(s)