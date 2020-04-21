import sys
import matplotlib
import matplotlib.pyplot as plot
import matplotlib.dates as dates
import datetime
import matplotlib.patches as patchs

def lineplot(x_data, y_data, x_label="", y_label="", title=""):

    fig, ax = plot.subplots()

    
    ax.plot(x_data, y_data, lw = 1, color = '#5A009D', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.savefig('traffic_diagram.pdf')

def draw_graphic(data, IP):
    lrg = 23
    medium = 17
    small= 13

    params = {
        "figure.titlesize": medium,
        "figure.figsize": (16,10),
        "axes.labelsize": medium,
        "axes.titlesize":medium,
        "legend.fontsize":medium,
        "xtick.labelsize":small,
        "ytick.labelsize":medium
    }

    plot.rcParams.update(params)
    coef = 0.0009765625
    # x = [datetime.datetime.strptime(s[0],"%Y-%m-%d %H:%M:%S") for s in data[1:len(data)-3]]
    x = []
    y = []
    datamas = {}
    
    for i in range(1, len(data)-3):
        if data[i][3] == IP or data[i][4] == IP:
            delta = int(data[i][12])
            time = data[i][0]
            if time in datamas:
                prev_t = datamas[time]
                datamas[time] = prev_t + delta
            else:
                datamas[time] = delta
            
    print(data[15904][0])        
    datamas_ks = list(datamas.keys())
    datamas_ks.sort()

    # print(len(datamas))
    # print(datamas)

    prev_i = 0
    prev_prev_i = 0
    traffic = 0
    for i in datamas_ks:
        traffic += datamas[i]
        
        prev_prev_i = prev_i
        prev_i = i 
        print(f"{i}:{traffic}")
        x.append(datetime.datetime.strptime(i,"%Y-%m-%d %H:%M:%S"))
        y.append(traffic)
    
    lineplot(x,y,"Timestamp (sec)","Trafic (bytes)","Diagram of trafic in time")
    
    datenums = dates.date2num(x)

    plot.figure(figsize=(16,10), dpi= 80, facecolor='w', edgecolor='k')
    plot.xticks(rotation = 14)
    ax = plot.gca()
    ax.set(xlabel = "Time", ylabel = "Traffic (Kb)")
    fmt = dates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_major_locator(dates.MinuteLocator(interval=10))
    plot.scatter(datenums, y, s=5,c='tab:green', label="Traffic, Kb")
    plot.title("Traffic over time", fontsize = 22)
    plot.legend(fontsize=13)
    plot.savefig("traffic_scatter.pdf", bbox_inches="tight")

data = []

with open("traffic.csv", "r") as file:
    for line in file:
        data.append(line.split(","))

IP = "217.15.20.194"
k = 2
traffic = 0
trafic_range = []

for i in range(len(data)-3):
    line = data[i]
    sa = line[3]
    da = line[4]
    ibyt = line[12]
    if sa == IP or da == IP:
        traffic += int(ibyt)

draw_graphic(data, IP)

traffic /= 1024*1024

print(round(traffic * k, 2))

# for i in range(len(mas[0])):
#     if mas[0][i] == "sa":
#         print(f"sa: {i}", end = " ")
#     elif mas[0][i] == "da":
#         print(f"da: {i}", end = " ")
#     elif mas[0][i] == "ibyt":
#         print(f"ibyt: {i}", end = " ")
#     elif mas[0][i] == "obyt":
#         print(f"obyt: {i}", end = " ")
#     elif mas[0][i] == "ts":
#         print(f"ts: {i}", end = " ")
#     elif mas[0][i] == "te":
#         print(f"te: {i}", end = " ")
# print()

