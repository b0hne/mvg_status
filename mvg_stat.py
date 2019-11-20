#!/usr/bin/python3
from mvg_api import *
from tkinter import *

COLOR_L = "sky blue"
COLOR_R = "pale green"

# retreave departures for Garching
def get_Garching():
    gz = Station(get_id_for_station("Garching"))
    gzf_dp = []
    gzm_dp = []

    for departure in gz.get_departures():
        print(departure['destination'])
        if(departure['product'] == 'UBAHN' and (len(gzf_dp) + len(gzm_dp)!= 4)):
            if(departure['destination'][0] == 'G'):
                if(len(gzf_dp)<2):
                    gzf_dp.append("\rin " + str(departure['departureTimeMinutes']) + ' min')
            elif(len(gzm_dp)<2):
                gzm_dp.append("\rin " + str(departure['departureTimeMinutes']) + ' min')
    for i in range(2 - len(gzf_dp)):
        gzf_dp.append('')
    for i in range(2 - len(gzm_dp)):
        gzm_dp.append('')
    return gzf_dp + gzm_dp

# retreave departures for Garching
def get_Stieglitz():
    ls = Station(get_id_for_station("Lehrer Stieglitz Str"))
    ls_dp = ['']*4
    j = 0
    for departure in ls.get_departures():
        if(j < 4):
            ls_dp[j] = (departure['label'] + " " + departure['destination']
                + "\r" + 'in' + ' ' + str(departure['departureTimeMinutes']) + '' + 'min')
            j += 1
    return ls_dp

root = Tk()
# switch out for rearranging on smaller displays
root.geometry("320x240")
root.config(cursor="none")
# root.attributes('-fullscreen', True)
frame = Frame(root)
frame.grid()
root.title("departures")

# create grid
for r in range(6):
    root.rowconfigure(r, weight=1)
for c in range(6):
    root.columnconfigure(c, weight=1)

# store stations for comparrission
dpg = ['']*4
dps = ['']*4


def fill():
    dpg_new = get_Garching()
    global dpg
    if(dpg != dpg_new):
        dpg = dpg_new
        frame0 = Frame(root, bg=COLOR_L)
        frame0.grid(row = 0, column = 0, rowspan = 3, columnspan = 3, sticky = N+S+W+E)

        title0 = Label(frame0, text="\nU6", font=("Courier 16 bold"), bg=COLOR_L)
        title0.pack(expand=YES, anchor=N)
        title00 = Label(frame0, text="-> Campus", font=("Courier 9 bold"), bg=COLOR_L)
        title00.pack(expand=YES, anchor=N)
        departure0_0 = Label(frame0, text=dpg[0], bg=COLOR_L)
        departure0_0.pack(expand=YES, anchor=N)
        departure0_1 = Label(frame0, text=dpg[1], bg=COLOR_L)
        departure0_1.pack(expand=YES, anchor=N)

        frame1 = Frame(root, bg=COLOR_L)
        frame1.grid(row = 3, column = 0, rowspan = 3, columnspan = 3, sticky = N+S+W+E)
        title01 = Label(frame1, text="-> München", font=("Courier 9 bold"), bg=COLOR_L)

        title01.pack(expand=YES, anchor=N)
        departure1_0 = Label(frame1, text=dpg[2], bg=COLOR_L)
        departure1_0.pack(expand=YES, anchor=N)
        departure1_1 = Label(frame1, text=dpg[3], bg=COLOR_L)
        departure1_1.pack(expand=YES, anchor=N)

    # fill Stieglitz Str
    dps_new = get_Stieglitz()
    global dps
    if(dps != dps_new):
        dps = dps_new
        frame2 = Frame(root, bg=COLOR_R)
        frame2.grid(row = 0, column = 3, rowspan = 6, columnspan = 3, sticky = W+E+N+S)
        title2 = Label(frame2, text=str(datetime.datetime.now().time())[:5] + "\nLehrer Stieglitz" ,font=("Courier 16 bold"), bg=COLOR_R)
        title2.pack(expand=YES, anchor=N)
        departure2_0 = Label(frame2, text=dps[0], bg=COLOR_R, anchor='w')
        departure2_0.pack(expand=YES)
        departure2_1 = Label(frame2, text=dps[1], bg=COLOR_R, anchor='w')
        departure2_1.pack(expand=YES)
        departure2_2 = Label(frame2, text=dps[2], bg=COLOR_R, anchor='w')
        departure2_2.pack(expand=YES)
        departure2_3 = Label(frame2, text=dps[3], bg=COLOR_R, anchor='w')
        departure2_3.pack(expand=YES)
    # refresh every 15 Seconds
    frame.after(15000,fill)

fill()
root.mainloop()
