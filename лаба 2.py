from settings import settings
input_filename = "traffic.csv"
input_file = open(input_filename, "r")
data = []
IP = ''
free = settings["free"]
k = settings["price"]
traffic, bill = 0, 0

with open(input_filename, "r") as file:
    for line in file:
        data.append(line.split(","))
IP = '217.15.20.194'
#IP = input('введите IP-адрес для тарификации: ') #217.15.20.194 по варианту
for i in range(len(data)-3):
    if data[i][3] == IP or data[i][4] == IP:
        traffic += int(data[i][12])
        traffic += int(data[i][14])
if traffic > free: 
    traffic -= free
    traffic /= 1024*1024
    bill = traffic * k
else: 
    bill = 0
print('общая стоимость:', bill)

