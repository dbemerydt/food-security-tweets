import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
from matplotlib import rcParams
rcParams['font.size'] = '12'
import pickle
from metadata import *
import subprocess
import datetime
all_keywords = food_keywords+event_keywords

for event in events[1:]:
    event_folder = event["name"].lower().replace(" ","-")
    f = open(event_folder+"/tweet-counts.p","rb")
    counts = pickle.loads(f.read())
    f.close()
    start_datetime = datetime.datetime(event["start"].year,event["start"].month,event["start"].day)-datetime.timedelta(days=7)
    times = [start_datetime+i*datetime.timedelta(hours=1) for i in range(len(counts[0]))]
    base_resolution = datetime.timedelta(hours=1)
    resolutions = [datetime.timedelta(hours=1),datetime.timedelta(hours=3),datetime.timedelta(hours=12),datetime.timedelta(days=1),]
    resolution_names = ["1 Hour","3 Hours","12 Hours","1 Day"]
    # for i in range(len(all_keywords)):
    #     fig = plt.figure(figsize=(15,6))
    #     ax = fig.add_axes([.2,.2,.7,.7])
    #     # plt.plot(times,counts[i])
    #     ax.plot(times,counts[i],zorder=20,label=all_keywords[i])
    #     ax.plot([event["start"],event["start"]],ax.get_ylim(),color=".7",linestyle='dashed',zorder=10)
    #     ax.plot([event["end"]+datetime.timedelta(days=1),event["end"]+datetime.timedelta(days=1)],ax.get_ylim(),color=".7",linestyle='dashed',zorder=10)
    #     # ax.title(all_keywords[i],zorder=20)
    #     plt.legend()
    #     ax.set_ylabel("Num. Tweets")
    #     ax.set_xlabel("Time")
    #     plt.savefig(event_folder+"/"+all_keywords[i].replace(" ","-")+"-hourly.png",dpi=600,bbox_inches="tight")
    #     plt.close(fig)
    # subprocess.call("open "+event_folder+"/"+all_keywords[i].replace(" ","-")+".png",shell=True)
    
    for i in range(len(all_keywords)):
        values = counts[i]
        print(len(times))
        for r_i in range(len(resolutions)):
            resolution = resolutions[r_i]
            bigger_times = [start_datetime+i*resolution for i in range(int((times[-1]-times[0])/resolution+1))]
            # print(len(bigger_times))
            new_values = [0 for i in range(len(bigger_times))]
            for j,t in enumerate(bigger_times):
                inner = t
                while inner<t+resolution:
                    new_values[j] += values[times.index(inner)]
                    inner += base_resolution
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_axes([.2,.2,.7,.7])
            # plt.plot(times,counts[i])
            ax.plot(bigger_times,new_values,zorder=20,label=all_keywords[i])
            # ax.plot(times,counts[i],zorder=20,label=all_keywords[i])
            ax.plot([event["start"],event["start"]],ax.get_ylim(),color=".7",linestyle='dashed',zorder=10)
            ax.plot([event["end"]+datetime.timedelta(days=1),event["end"]+datetime.timedelta(days=1)],ax.get_ylim(),color=".7",linestyle='dashed',zorder=10)
            ax.set_title(resolution_names[r_i],zorder=20)
            plt.legend()
            ax.set_ylabel("Num. Tweets")
            ax.set_xlabel("Time")
            plt.savefig(event_folder+"/"+all_keywords[i].replace(" ","-")+"-"+resolution_names[r_i].lower().replace(" ","-")+".png",dpi=600,bbox_inches="tight")
            plt.close(fig)

