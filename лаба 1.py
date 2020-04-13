input_filename = "data.csv"
input_file = open(input_filename, "r")
data = []
duration_out, duration_in = 0, 0
sms, bill, phone = 0, 0, 0
k_outcall, k_incall, k_sms = 3, 1, 1

with open(input_filename, "r") as file:
    for line in file:
        data.append(line.split(","))
phone = input('введите номер для тарификации: ') #968247916 по варианту
for i in range(len(data)):
    if data[i][1] == phone:
        duration_out += float(data[i][3])
        sms += int(data[i][4])
    if data[i][2] == phone:
        duration_in += float(data[i][3])
bill = duration_out * k_outcall + duration_in * k_incall + sms * k_sms    
print('общая стоимость за услуги связи:', bill)
