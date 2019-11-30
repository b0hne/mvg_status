#!/usr/bin/python3
'''
displays the departures at Garching and Lehrer Stieglitz Str
'''
from tkinter import Tk, Frame, Label, YES, N, E, S, W
import datetime
from mvg_api import Station, get_id_for_station
from eventlet import Timeout

COLOR_L = "sky blue"
COLOR_R = "pale green"


# store stations for comparrission
departure_garching = ['']*4
departure_stieglitz = ['']*4


def get_garching():
    '''
    retrieves and prepares departuretimes for Garching station
    '''
    departures = None
    with Timeout(5, False):
        try:
            departures = Station(get_id_for_station("Garching"))
        except:
            return [' ']*4
    if departures is None:
        return [' ']*4
    towards_garching = []
    towards_munich = []

    for departure in departures.get_departures():
        if(departure['product'] == 'UBAHN' and len(towards_garching) + len(towards_munich) != 4):
            if departure['destination'][0] == 'G':
                if len(towards_garching) < 2:
                    towards_garching.append("\rin " + str(departure['departureTimeMinutes'])
                                            + ' min')
            elif len(towards_munich) < 2:
                towards_munich.append("\rin " + str(departure['departureTimeMinutes']) + ' min')
    for _ in range(2 - len(towards_garching)):
        towards_garching.append(' ')
    for _ in range(2 - len(towards_munich)):
        towards_munich.append(' ')
    return towards_garching + towards_munich

def get_stieglitz():
    '''
    retrieves and prepares departuretimes for LST station
    '''
    departures = None
    with Timeout(5, False):
        try:
            departures = Station(get_id_for_station("Lehrer Stieglitz Str"))
        except:
            return [' ']*4
    if departures is None:
        return [' ']*4

    stieglitz_str = ['']*4
    j = 0
    for departure in departures.get_departures():
        if j < 4:
            stieglitz_str[j] = (
                departure['label'] + " " + departure['destination']
                + "\r" + 'in' + ' ' + str(departure['departureTimeMinutes'])
                + '' + 'min')
            j += 1
    return stieglitz_str

def fill():
    '''
    creates and regularly updates interface
    '''
    # fill Garching
    departure_garching_new = get_garching()
    global departure_garching
    if departure_garching != departure_garching_new:
        departure_garching = departure_garching_new
        frame0 = Frame(root, bg=COLOR_L)
        frame0.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=N+S+W+E)

        title0 = Label(frame0, text="\nU6", font=("Courier 16 bold"), bg=COLOR_L)
        title0.pack(expand=YES, anchor=N)
        title00 = Label(frame0, text="-> Campus", font=("Courier 9 bold"), bg=COLOR_L)
        title00.pack(expand=YES, anchor=N)
        departure0_0 = Label(frame0, text=departure_garching[0], bg=COLOR_L)
        departure0_0.pack(expand=YES, anchor=N)
        departure0_1 = Label(frame0, text=departure_garching[1], bg=COLOR_L)
        departure0_1.pack(expand=YES, anchor=N)

        frame1 = Frame(root, bg=COLOR_L)
        frame1.grid(row=3, column=0, rowspan=3, columnspan=3, sticky=N+S+W+E)
        title01 = Label(frame1, text="-> München", font=("Courier 9 bold"), bg=COLOR_L)

        title01.pack(expand=YES, anchor=N)
        departure1_0 = Label(frame1, text=departure_garching[2], bg=COLOR_L)
        departure1_0.pack(expand=YES, anchor=N)
        departure1_1 = Label(frame1, text=departure_garching[3], bg=COLOR_L)
        departure1_1.pack(expand=YES, anchor=N)

    # fill Stieglitz Str
    departure_stieglitz_new = get_stieglitz()
    global departure_stieglitz
    if departure_stieglitz != departure_stieglitz_new:
        departure_stieglitz = departure_stieglitz_new
        frame2 = Frame(root, bg=COLOR_R)
        frame2.grid(row=0, column=3, rowspan=6, columnspan=3, sticky=W+E+N+S)
        title2 = Label(frame2, text=str(datetime.datetime.now().time())[:5] + "\nLehrer Stieglitz",
                       font=("Courier 16 bold"), bg=COLOR_R)
        title2.pack(expand=YES, anchor=N)
        departure2_0 = Label(frame2, text=departure_stieglitz[0], bg=COLOR_R, anchor='w')
        departure2_0.pack(expand=YES)
        departure2_1 = Label(frame2, text=departure_stieglitz[1], bg=COLOR_R, anchor='w')
        departure2_1.pack(expand=YES)
        departure2_2 = Label(frame2, text=departure_stieglitz[2], bg=COLOR_R, anchor='w')
        departure2_2.pack(expand=YES)
        departure2_3 = Label(frame2, text=departure_stieglitz[3], bg=COLOR_R, anchor='w')
        departure2_3.pack(expand=YES)
    # refresh every 15 Seconds
    frame.after(15000, fill)

# root window
root = Tk()

# switch out for rearranging on other resolution displays
# root.attributes('-fullscreen', True)
root.geometry("320x240")
root.config(cursor="none")
frame = Frame(root)
frame.grid()
root.title("departures")

# create grid
for r in range(6):
    root.rowconfigure(r, weight=1)
for c in range(6):
    root.columnconfigure(c, weight=1)

#launch
fill()
root.mainloop()
