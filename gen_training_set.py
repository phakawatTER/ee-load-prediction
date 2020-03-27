import pandas as pd
from matplotlib import pyplot as plt
import os
DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
TIMES = []
ENV_NAME = "ee-env"
dataframe = pd.DataFrame(columns=['time', 'load'])
current_dir = os.path.dirname(__file__)  # current path of script file
# list directory of each day dataset
directory = [dir for dir in os.listdir() if not os.path.isfile(dir)
             and dir != ENV_NAME]


def get_day(day):
    if day in DAYS:
        return day
    else:
        for d in DAYS:
            if d in day:
                return d


def get_month(month):
    if month in MONTHS:
        return month
    else:
        for d in MONTHS:
            if d in month:
                return d
        print(month)


for d in directory:
    files = os.listdir(d)
    try:
        for file in files:
            try:
                try:
                    dd, mm, _, _ = file.split("_")
                except:
                    dd,mm,_ =file.split("_")
                dd = get_day(dd.lower())  # lowercase day
                mm = get_month(mm.lower())  # lowercase month
                dd = DAYS.index(dd)
                mm = MONTHS.index(mm)
                dt = "{} {} ".format(dd, mm)
                file_path = os.path.join(d, file)
                csv = pd.read_csv(file_path)
                csv.rename(columns={"Category": "time",
                                    "Krabi": "load"}, inplace=True)
                for i, t in enumerate(csv["time"]):
                    try:
                        new_time = dt+t
                        csv.set_value(i, "time", new_time)
                    except:
                        pass
                dataframe = dataframe.append(csv, ignore_index=True)
            except:
                pass
    except:
        pass
clusters = {}
def format_date(x):
    if len(str(x)) == 1:
        x= "0"+str(x)
    return x
def format_time(time):
    hour,minute = time.split(":")
    second = "00"
    if len(hour) == 1:
        hour = "0"+hour
    return  ":".join([hour,minute,second])

for i, time in enumerate(dataframe["time"]):

    try:
        day, month, time = time.split(" ")
        hour, minute = time.split(":")
        cluster = "{}-{}".format(day, month)
        tt = format_time(time)
        dd = format_date(int(day)+1)
        mm = format_date(int(month)+1)
        
        norm_time = (int(day)+int(month)+int(hour)+int(minute))/(6+11+23+59)
        date = f"2016-{mm}-{dd} {tt}"
        dataframe.set_value(i, "date",date )
        dataframe.set_value(i, "time",norm_time )
        dataframe.set_value(i, "day", day)
        dataframe.set_value(i, "month", month)
        dataframe.set_value(i, "hour", int(hour))
        dataframe.set_value(i, "minute", int(minute))
        if cluster not in clusters:
            clusters[cluster] = {"time": [], "load": []}
        clusters[cluster]["time"].append(dataframe["time"][i])
        clusters[cluster]["load"].append(dataframe["load"][i])
    except Exception as err:
        print(err)
        pass
    
    
dataframe.drop(columns=["time"],axis=1)

dataframe= dataframe.sort_values(by="date",ascending=True)
# dataframe=dataframe.reindex(columns=["norm_time","load"])
dataframe=dataframe.reindex(columns=["day","month","hour","minute","load"])
# dataframe=dataframe.reindex(columns=["date","load"])
dataframe=dataframe.dropna()# drop nan row
dataframe.to_csv("training_set.csv", index=False)

# color_list = ["ro", "go", "bo", "yo"]
# for i, c in enumerate(clusters):
#     cluster = clusters[c]
#     time = cluster["time"]
#     load = cluster["load"]
#     plt.plot(time, load, color_list[i % len(color_list)-1])
# plt.show()
