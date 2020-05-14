from number_to_text import *
import datetime
from jinja2 import Template
import pdfkit
import os

input_filename = 'C:\\Users\\Лера\\Desktop\\6 семестр\\мобилки\\лаба 3\\bill.html'
with open(input_filename, 'r', encoding='utf-8') as f:
    html = f.read()

path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

internet_settings = {'price':1, 'free':1024000}

today_date = datetime.datetime.now().date()
day = today_date.day
if day < 10:
    day = f"0{day}"

month = today_date.month
if month < 10:
    month = f"0{month}"
today_date = f"Счет на оплату № 100 от {day}.{month}.{today_date.year}"
 
#счёт за интернет
input_filename_traffic = "traffic.csv"
data_internet = []
IP = ''
free = internet_settings["free"]
k = internet_settings["price"]
traffic, bill_internet = 0, 0

with open(input_filename_traffic, "r") as file:
    for line in file:
        data_internet.append(line.split(","))
IP = '217.15.20.194'
#IP = input('введите IP-адрес для тарификации: ') #217.15.20.194 по варианту
for i in range(len(data_internet)-3):
    if data_internet[i][3] == IP or data_internet[i][4] == IP:
        traffic += int(data_internet[i][12])
        traffic += int(data_internet[i][14])
if traffic > free: 
    traffic -= free
    traffic /= 1024*1024
    bill_internet = traffic * k
else: 
    bill_internet = 0
bill_internet = round(bill_internet,2)    

#счет за мобильную связь
input_filename_calls = "data.csv"
data_phone = []
duration_out, duration_in = 0, 0
sms, bill_phone, phone = 0, 0, 0
k_outcall, k_incall, k_sms = 3, 1, 1

with open(input_filename_calls, "r") as file:
    for line in file:
        data_phone.append(line.split(","))
phone = '968247916'
#phone = input('введите номер для тарификации: ') #968247916 по варианту
for i in range(len(data_phone)):
    if data_phone[i][1] == phone:
        duration_out += float(data_phone[i][3])
        sms += int(data_phone[i][4])
    if data_phone[i][2] == phone:
        duration_in += float(data_phone[i][3])
bill_phone = duration_out * k_outcall + duration_in * k_incall + sms * k_sms

bill = bill_internet + bill_phone

bill = round(bill,2) #округляем до двух знаков
bill_r = int(bill) #находим целое число 
bill_c = round(bill%1,2) * 100 #находим копейки
bill_c = int(bill_c) 

#определяем, что нужно дописать после количества рублей
if bill_r % 100 in range(10, 20):
    rubl = "рублей"
elif bill_r % 10 in [2,3,4]:
    rubl = "рубля"
elif bill_r % 10 in [0, 5, 6, 7, 8, 9]:
    rubl = "рублей"
elif bill_r % 10 == 1:
    rubl = "рубль"

#определяем, что нужно дописать после количества копеек
if bill_c % 100 in range(10, 20):
    copeck = "копеек"
elif bill_c % 10 in [2,3,4]:
    copeck = "копейки"
elif bill_c % 10 in [0, 5, 6, 7, 8, 9]:
    copeck = "копеек"
elif bill_c % 10 == 1:
    copeck = "копейка"

string = num2text(bill) #письменное представление числа
string = string[:1].upper() + string[1:] 

settings_html = {'bank':'БАНК СЕВЕРО-ЗАПАДНЫЙ БАНК ПАО СБЕРБАНК',
'gorod':'Г. САНКТ - ПЕТЕРБУРГ',
'BIK':'044030653',
'account_1':'30101810500000000653',
'account_2':'40702810855000100555',
'INN_provider':'7707049388',
'KPP_provider':'784243002',
'name_recipient':'Фёдоров Иван Романович',
'today_date': today_date,
'name_company':'Макрорегиональный филиал "Северо - Запад" ПАО "РОСТЕЛЕКОМ"',
'INN_recipient':'1101011111',
'KPP_recipient':'111111001',
'address_recipient':'г. Санкт - Петербург, Университет ИТМО, улица Ломоносова, 9',
'internet':'Домашний интернет',
'bill_internet': bill_internet,
'phone':'Мобильная связь',
'bill_phone': bill_phone,
'bill': bill,
'bill_letters': string,
'rubl': rubl,
'bill_c': bill_c,
'copeck':copeck}

options = {
    'page-size': 'A4',
    'margin-top': '2cm',
    'margin-left': '3cm',
    'margin-right': '2cm'
}

billtemplate = Template(html)
output = billtemplate.render(context=settings_html)

temp_file = 'C:\\Users\\Лера\\Desktop\\6 семестр\\мобилки\\лаба 3\\bill_2.html' #временный файл
pdf = 'C:\\Users\\Лера\\Desktop\\6 семестр\\мобилки\\лаба 3\\bill.pdf' #pdf - файл, куда сохранится счёт

with open(temp_file, 'wb') as f:
    f.write(output.encode('utf-8'))

pdfkit.from_file(temp_file, pdf, options = options, configuration = config)
os.remove(temp_file)