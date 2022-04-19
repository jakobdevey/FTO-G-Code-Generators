from numpy import array
from tkinter import *

# main window for GUI
root = Tk()
root.title('Circular G-code Generator')
root.geometry("1000x500")

# Title
title = Label(root, text="Enter Dimensions for Piece and Tool")
title.config(font=('helvetica', 18))
title.grid(row=0, column=0)

# Inputs are string variables to be converted to floats later
tool_size_hold = StringVar()
cut_depth_hold = StringVar()
new_diam_hold =  StringVar()
material = StringVar()
flute = StringVar()

# GUI boxes for entries
cut_depth_Box = Entry(root, textvariable=cut_depth_hold)
cut_depth_Box.grid(row=1, column=1)
cut_depth_Label = Label(text="How deep you would like to cut in mm (exact):")
cut_depth_Label.grid(row=1, column=0)

new_diam_Box = Entry(root, textvariable=new_diam_hold)
new_diam_Box.grid(row=3, column=1)
new_diam_Label = Label(text="The desired diameter of the hole in um (exact):")
new_diam_Label.grid(row=3, column=0)

tool_label = Label(root, text='Select the size of your tool:').grid(row=10, column=0)
tool_menu = OptionMenu(root, tool_size_hold, '0.040"','1/32"', '5/64"', '2.0mm', '1/16"', '1/8"').grid(row=10, column=1)


material_label = Label(root, text='Select the material of your piece:').grid(row=8, column=0)
material_menu = \
    OptionMenu(root, material, 'Cast Iron', 'Brass, Mild Steels, Carbon Steels', 'Alloy/ Tool Steels (Up to 30 HRC)', 'Hardened Steel, Prehardened Steel, Ti Alloy (30-38 HRC)', 'Hardened Steel, Prehardened Steel, Stainless Steel (38-45 HRC)', 'Aluminium Alloys').grid(row=8, column=1)


flute_label = Label(root, text='Select the number of flutes on your tool:').grid(row=9, column=0)
flute_menu = OptionMenu(root, flute, '2 Flute', '4 Flute').grid(row=9, column=1)


# Lists for speeds and feeds of different materials/ tools
# called later in the code depending on what tool and material you pick in the GUI
# 0's in four flute lists are placeholders for 0.040" since there is no 4-flute 0.040" tool
# Cast Iron
two_fl_speeds_iron = [14000, 21000, 12000, 9000, 6000]
two_fl_feeds_iron = [90, 168, 168, 168, 180]
four_fl_speeds_iron = [0, 21000, 11000, 8000, 5000]
four_fl_feeds_iron = [0, 600, 600, 608, 620]
#0's in four flute lists are placeholders for 0.040"

# Brass
two_fl_speeds_brass = [13000, 19000, 11000, 8000, 5000]
two_fl_feeds_brass = [80, 115, 115, 120, 120]
four_fl_speeds_brass = [0, 24000, 12000, 9000, 6000]
four_fl_feeds_brass = [0, 300, 300, 300, 360]

# up to 30 HRC
two_fl_speeds_30 = [11000, 16000, 9000, 7000, 4000 ]
two_fl_feeds_30 = [40, 50, 51, 53, 76]
four_fl_speeds_30 = [0, 16000, 9000, 7000, 4000]
four_fl_feeds_30 = [0, 280, 280, 280, 280]

# 30 to 38 HRC
two_fl_speeds_38 = [9000, 14000, 8000, 6000, 4000]
two_fl_feeds_38 = [30, 36, 36, 36, 36]
four_fl_speeds_38 = [0, 15000, 8000, 6000, 4000]
four_fl_feeds_38 = [0, 115, 115, 115, 110]

# 38 - 45 HRC
two_fl_speeds_45 = [7000, 11000, 6000, 5000, 3000]
two_fl_feeds_45 = [25, 31, 31, 31, 31]
four_fl_speeds_45 = [0, 13000, 7000, 5000, 3000]
four_fl_feeds_45 = [0, 90, 90, 90, 84]

# Aluminium
two_fl_speeds_al = [32000, 48000, 27000, 19000, 12000]
two_fl_feeds_al = [200, 240, 240, 240, 260]
four_fl_speeds_al = [0, 50000, 32000, 22000, 15000]
four_fl_feeds_al = [0, 1000, 1000, 1000, 1090]

# Flute lengths for each tool for maximum cut depth
fl_len = [3.15, 4.70, 6.30, 6.95, 12.65]    # 0.040" & 1/32", 1/16", 5/64", 2.0mm, 1/8"


# function for generating speeds and feeds based on tool size and piece material
def show():
    speed = 'Not Input'
    feed = 'Not Input'
    tool_size = 'Not Input'
    # different indexes corresponding to list positions above
    if tool_size_hold.get() == '0.040"':
        tool_size = 0
    if tool_size_hold.get() == '1/32"':
        tool_size = 1
    if tool_size_hold.get() == '1/16"':
        tool_size = 2
    if tool_size_hold.get() == '2.0mm':
        tool_size = 3
    if tool_size_hold.get() == '5/64"':
        tool_size = 3
    if tool_size_hold.get() == '1/8"':
        tool_size = 4

    # empty labels to 'white out' previous labels
    white = Label(root, text='                                                                                                                                                                                                  ').grid(row=12, column=0)
    white2 = Label(root, text='                                                                                                                                         ').grid(row=13, column=0)

# Get results based on user selections from dropdown menus
    speed_num = 'Not Input'
    feed_num = 'Not Input'

    if material.get() == 'Brass, Mild Steels, Carbon Steels' and flute.get() == '2 Flute':
        speed_num = two_fl_speeds_brass[tool_size]
        feed_num = two_fl_feeds_brass[tool_size]
    elif material.get() == 'Brass, Mild Steels, Carbon Steels' and flute.get() == '4 Flute':
        speed_num = four_fl_speeds_brass[tool_size]
        feed_num = four_fl_feeds_brass[tool_size]
    elif material.get() == 'Cast Iron' and flute.get() == '2 Flute':
        speed_num = two_fl_speeds_iron[tool_size]
        feed_num = two_fl_feeds_iron[tool_size]
    elif material.get() == 'Cast Iron' and flute.get() == '4 Flute':
        speed_num = four_fl_speeds_iron[tool_size]
        feed_num = four_fl_feeds_iron[tool_size]
    elif material.get() == 'Alloy/ Tool Steels (Up to 30 HRC)' and flute.get() == '2 Flute':
        speed_num = two_fl_speeds_30[tool_size]
        feed_num = two_fl_feeds_30[tool_size]
    elif material.get() == 'Alloy/ Tool Steels (Up to 30 HRC)' and flute.get() == '4 Flute':
        speed_num = four_fl_speeds_30[tool_size]
        feed_num = four_fl_feeds_30[tool_size]
    elif material.get() == 'Hardened Steel, Prehardened Steel, Ti Alloy (30-38 HRC)' and flute.get() == '2 Flute':
        speed_num = two_fl_speeds_38[tool_size]
        feed_num = two_fl_feeds_38[tool_size]
    elif material.get() == 'Hardened Steel, Prehardened Steel, Ti Alloy (30-38 HRC)' and flute.get() == '4 Flute':
        speed_num= four_fl_speeds_38[tool_size]
        feed_num = four_fl_feeds_38[tool_size]
    elif material.get() == 'Hardened Steel, Prehardened Steel, Stainless Steel (38-45 HRC)' and flute.get() == '2 Flute':
        speed_num = two_fl_speeds_45[tool_size]
        feed_num = two_fl_feeds_45[tool_size]
    elif material.get() == 'Hardened Steel, Prehardened Steel, Stainless Steel (38-45 HRC)' and flute.get() == '4 Flute':
        speed_num = four_fl_speeds_45[tool_size]
        feed_num = four_fl_feeds_45[tool_size]
    elif material.get() == 'Aluminium Alloys' and flute.get() == '2 Flute':
        speed_num = two_fl_speeds_al[tool_size]
        feed_num = two_fl_feeds_al[tool_size]
    elif material.get() == 'Aluminium Alloys' and flute.get() == '4 Flute':
        speed_num = four_fl_speeds_al[tool_size]
        feed_num = four_fl_feeds_al[tool_size]
    else:
        # give error if user has not made selections and tries to generate speed and feed
        error = Label(root, text = 'ERROR: NOT ENOUGH INFO TO GENERATE SPEEDS AND FEEDS').grid(row=12, column=0)

        # convert to string to display to user
    speed = str(speed_num)
    feed = str(feed_num)

    # our spindle only goes up to 30000 RPM
    # give error if required spindle speed exceeds 30000
    if speed_num > 30000:
        pop = Label(root, text='Required spindle speed exceeds the capabilities of our spindle. Please use a different end mill / tool.').grid(row=6, column=0)
    else:
        # Display speed and feed to user
        snf = Label(root, text='Set spindle speed to ' + speed + ' RPM and feed rate to ' + feed + ' mm/min.').grid(row=6, column=0)


    return

#   Button to execute function above
but = Button(root, text='Generate Speed and Feed', command=show).grid(row=12, column=1)


# function for generating G-code .txt file
def gen_code():
    # get parameters from user inputs
    cut_depth = float(cut_depth_hold.get())
    new_diam = float(new_diam_hold.get())/1000
    tool_diam = 'Not Input'
    tool_len = 'Not Input'
    # converting tool diameter from in to mm
    # must be exact since the tool diameter affects the amount of material left to cut
    if tool_size_hold.get() == '0.040"':
        tool_diam = 1.016
        tool_len = fl_len[0]
    if tool_size_hold.get() == '1/32"' :
        tool_diam = 0.7938
        tool_len = fl_len[0]
    if tool_size_hold.get() == '1/16"':
        tool_diam = 1.5875
        tool_len = fl_len[1]
    if tool_size_hold.get() == '2.0mm':
        tool_diam = 2.000
        tool_len = fl_len[3]
    if tool_size_hold.get() == '5/64"':
        tool_diam = 1.9844
        tool_len = fl_len[2]
    if tool_size_hold.get() == '1/8"':
        tool_diam = 3.1750
        tool_len = fl_len[4]

    old_diam = tool_diam

    # set rest of parameters for setup
    # list of x vals
    xvals = []
    xend = round((new_diam - old_diam)/2, 4) # difference between tool diameter and desired diameter
    xmove = round(tool_diam/100, 4) # very small increments to minimize tool bending
    # xmove = 1.0 # you can set the increments to a fixed number if you want here

    # list from 0 to x end in increments of xmove
    x_pos = 0
    while x_pos <= xend:
        xvals.append(x_pos)
        x_pos += xmove
        if x_pos >= xend:
            xvals.append(xend)

    # array for indexing
    xvals = array(xvals)

    # z cut increment
    z_change = round(tool_diam/8, 4)
    # z_change = 1
    z_end = -cut_depth

    # make list of all z values
    # from 0 to z end in increments of z_change
    zvals = []
    zpos = -z_change
    while zpos > z_end:
        zvals.append(zpos)
        zpos -= z_change
        if zpos <= z_end:
            zvals.append(z_end)

    zvals = array(zvals)

    # give warning to user if selected tool is too short
    if cut_depth > tool_len:
        warning = Label(root,text="The selected tool is not long enough to make the desired cut. Please use another tool or make a shallower cut.").grid(row=14, column=0)

    # open new txt file
    elif cut_depth <= tool_len:
        file = open(r'C:\\Users\\Jaime Ortiz.SANDIA\\Documents\\NEW CIRCLE G-CODE (RENAME).txt', 'w')
        # raise tool to a safe height
        file.write('g0z20' + '\n')
        # move tool exactly above center of connector
        file.write('g0x0y0' + '\n')
        #lower tool to 1mm above connector
        file.write('g0z1' + '\n')

        # make hole the size of the tool through the center of the connector
        for z in range(len(zvals)):
            zstr = str(round(zvals[z],4))
            # feedrate 50 mm/min
            # pecking down center of  connector
            file.write('F50.0 z' + zstr + '\n')
            if z%3 == 0:    #pull out every third stepl
                file.write('g1 z0' + '\n')
                file.write('g1z' + zstr + '\n')

        # circular portion of g-code
        # run all x values for each z value
        for z in range(len(zvals)):
            # raise tool to safe height
            file.write('g1z1' + '\n')
            # bring tool to center of connector
            file.write('g1x0y0' + '\n')
            # convert z value to string
            zstr = str(round(zvals[z], 4))
            # lower tool to cutting depth
            file.write('g1z' + zstr + '\n')
            for x in range(len(xvals)):
                # positive x string
                xstr = str(xvals[x])
                # negative x string
                nxstr = str(-xvals[x])
                #bring tool to right side of circle
                file.write("g1x" + xstr + 'y0' + "\n")
                # make circular cut from right to left side of circle
                file.write("g3x" + nxstr + 'y0' + 'i' + nxstr + 'j0' + "\n")
                # finish cut by making circular cut from left to right side
                file.write("g3x" + xstr + 'y0' + 'i' + xstr + 'j0' + "\n")

        # safety height at end of code
        file.write("g0z30\n")
        file.write("g0z30")
        file.close()
        # notify user that their file is ready
        popup = Label(root, text="Your G-code was generated successfully and can be found in your documents.").grid(row=13, column=0)
        # to erase previous error message
        white3 = Label(root, text="                                                                                                                    
                                                                                                                                            ").grid(row=14, column=0)


    return

# button to execute function above
Enter = Button(root, text="Generate G-code", command=gen_code, width=20, height=3).grid(row=13, column=1)

root.mainloop()
