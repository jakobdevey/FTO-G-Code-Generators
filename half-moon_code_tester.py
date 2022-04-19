from numpy import array
from math import sqrt, sin, acos
from tkinter import *

# main window for GUI
root = Tk()
root.title('Half-moon G-code Generator')
root.geometry("1000x500")

# Title
title = Label(root, text="Enter Dimensions for Piece and Tool")
title.config(font=('helvetica', 18))
title.grid(row=0, column=0)

# GUI Inputs are string variables that will be converted to floats later
pc_diam_hold = StringVar()
pc_len_hold = StringVar()
tool_diam_hold = StringVar()
sl_wid_hold = StringVar()
sl_height_hold = StringVar()

# GUI boxes for parameters
pc_diam_Box = Entry(root, textvariable=pc_diam_hold)
pc_diam_Box.grid(row=3, column=1)
pc_diam_Label = Label(text="Piece diameter in mm (exact):")
pc_diam_Label.grid(row=3, column=0)

pc_len_box = Entry(root, textvariable=pc_len_hold)
pc_len_box.grid(row=4, column=1)
pc_len_label = Label(text="Piece length in mm (approximate to 0.1mm):")
pc_len_label.grid(row=4, column=0)

sl_wid_box = Entry(root, textvariable=sl_wid_hold)
sl_wid_box.grid(row=6, column=1)
sl_wid_label = Label(text="Desired slit width in mm (exact):")
sl_wid_label.grid(row=6, column=0)

sl_height_box = Entry(root, textvariable=sl_height_hold)
sl_height_box.grid(row=7, column=1)
sl_height_label = Label(text="Desired slit height in um (exact):")
sl_height_label.grid(row=7, column=0)

material = StringVar()
material_label = Label(root, text='Select the material of your piece:').grid(row=8, column=0)
material_menu = \
    OptionMenu(root, material, 'Cast Iron', 'Brass, Mild Steels, Carbon Steels', 'Alloy/ Tool Steels (Up to 30 HRC)', 'Hardened Steel, Prehardened Steel, Ti Alloy (30-38 HRC)', 'Hardened Steel, Prehardened Steel, Stainless Steel (38-45 HRC)', 'Aluminium Alloys').grid(row=8, column=1)

flute = StringVar()
flute_label = Label(root, text='Select the number of flutes on your tool:').grid(row=9, column=0)
flute_menu = OptionMenu(root, flute, '2 Flute', '4 Flute').grid(row=9, column=1)

tool_size_hold = StringVar()
tool_label = Label(root, text='Select the size of your tool:').grid(row=10, column=0)
tool_menu = OptionMenu(root, tool_size_hold, '0.040"', '1/32"', '1/16"', '5/64"', '2.0mm', '1/8"').grid(row=10, column=1)

# Lists for speeds and feeds of different materials/ tools
# called later in the code depending on what tool and material you pick in the GUI
# 0's in four flute lists are placeholders for 0.040" since there is no 4-flute 0.040" tool
# Cast Iron
two_fl_speeds_iron = [14000, 21000, 12000, 9000, 6000]
two_fl_feeds_iron = [90, 168, 168, 168, 180]
four_fl_speeds_iron = [0, 21000, 11000, 8000, 5000]
four_fl_feeds_iron = [0, 600, 600, 608, 620]

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
    # different selections corresponding to list positions above
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

# Get results based on selections from dropdown menus
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

#   Button to execute speed and feed function
but = Button(root, text='Generate Speed and Feed', command=show).grid(row=12, column=1)


# function for generating G-code .txt file
def gen_code():
    # get parameters from user entries
    pc_diam = float(pc_diam_hold.get())
    pc_len = float(pc_len_hold.get())
    sl_wid = float(sl_wid_hold.get())
    sl_height = float(sl_height_hold.get()) / 1000
    tool_diam = 'Not Input'
    tool_len = 'Not Input'
    # converting tool diameter from in to mm
    # does not need to be exact since this is only for determining the size of cuts
    if tool_size_hold.get() == '1/32"' :
        tool_diam = 0.8
        tool_len = fl_len[0]
    if tool_size_hold.get() == '0.040"':
        tool_diam = 1.0
        tool_len = fl_len[0]
    if tool_size_hold.get() == '1/16"':
        tool_diam = 1.6
        tool_len = fl_len[1]
    if tool_size_hold.get() == '2.0mm':
        tool_diam = 2.0
        tool_len = fl_len[3]
    if tool_size_hold.get() == '5/64"':
        tool_diam = 2.0
        tool_len = fl_len[2]
    if tool_size_hold.get() == '1/8"':
        tool_diam = 3.2
        tool_len = fl_len[4]

    # set rest of parameters for setup
    pc_rad = pc_diam / 2
    x_change = tool_diam / 4
    z_change = tool_diam / 4
    slh2 = sl_height / 2

    # tool limits for cutting
    # cutting front to back and left to right for cleanest cuts
    # start at front of piece
    y_start = -5
    y_end = pc_len + 5
    # convert to string to be written into .txt file
    y_start_str = str(y_start)
    y_end_str = str(y_end)
    # x start is one step in from the left of the piece
    x_start = -(pc_diam / 2) + x_change
    # x end is at the right end of the slit
    x_end = sl_wid / 2
    # z limit is half of the slit since this is only one half of the array
    z_end = -(pc_diam / 2) - slh2

    # make list of all z values
    # from z start to z end in increments of z change
    zvals = []
    zpos = -z_change
    while zpos > z_end:
        # round to 4 for machine limitations
        zpos1 = round(zpos, 4)
        zvals.append(zpos1)
        zpos -= z_change
        if zpos <= z_end: # so that the cut will go to the exact depth input by user
            zvals.append(z_end)

# convert to array to be able to index
    zvals = array(zvals)

    # make list of all x values
    # from x start to x end in increments of x change
    xvals = []
    xpos = x_start
    while xpos < x_end:
        xpos1 = round(xpos, 4)
        xvals.append(xpos1)
        xpos += x_change
        if xpos >= x_end: # to cut to exact position needed
            xvals.append(x_end)

    # array for indexing
    xvals = array(xvals)

    # give error if selected tool is not long enough to make the cut
    theta = acos((sl_wid/2)/pc_rad)
    h = (sin(theta) * pc_rad) + (sl_wid/2)

    # white label to "erase" previous messages
    white = Label(root, text = "                                                                                                                                                                                                                                          ").grid(row=14, column=0)#to white out previous error message

    if tool_len < h:
        error = Label(root, text="ERROR! The tool you have selected is too short to make this cut. Please change your parameters or select a new tool.").grid(row=14, column=0)

    # generate g-code if all lis good
    else:
        # open new txt file
        file = open(r'C:\\Users\\Jaime Ortiz.SANDIA\\Documents\\NEW HALF-MOON G-CODE (RENAME).txt', 'w')

        # g-code for first part of cut (top part)
        # sweep through all x values for each z value
        for z in range(len(zvals)):
            zstr = str(zvals[z])
            for x in range(len(xvals)):
                xstr = str(xvals[x])
                # raise tool above piece
                file.write('g1z1\n')
                # move tool to x and y position
                file.write("g0y" + y_start_str + "x" + xstr + "\n")
                # lower tool to cutting depth
                file.write("g1z" + zstr + "\n")
                # make cut from front to back of piece
                file.write("g1y" + y_end_str + "\n")

        # g-code for second part of cut (left side)
        # make list of coords for x
        xvalsB = []
        xposB = x_start
        # want to cut to left end of slit, therefore use negative x_end
        while xposB < -x_end:
            xposB1 = round(xposB, 4)
            xvalsB.append(xposB1)
            xposB += x_change
            if xposB >= -x_end: # go to exact end
                xvalsB.append(-x_end)

        xvalsB = array(xvalsB)

        # make list of limits for z
        zlims = []
        for i in range(len(xvalsB)):
            # calculating the cut depths from horizontal center of piece for each x value using pythagorean theorem
            zlim = sqrt(pc_rad ** 2 - xvalsB[i] ** 2) + pc_rad  # have to add pc radius to account for the top half of the piece
            zlim = round(zlim, 4)
            zlims.append(-zlim)

        zlims = array(zlims)

        # writing code for second part of cut (side sweeps)
        # sweep through all z values for each x value
        for i in range(len(zlims)):
            zposB = z_end # start at old z end position
            xposC = xvalsB[i]
            xstr2 = str(xposC) # convert to string for .txt file
            while zposB > zlims[i]:
                zposB -= z_change
                zposB = round(zposB, 4)
                zstr2 = str(zposB)
                # raise tool above piece
                file.write("g1z0\n")
                # go to x and y position
                file.write("g0y" + y_start_str + "x" + xstr2 + "\n")
                # lower tool to cutting depth
                file.write("g1z" + zstr2 + "\n")
                # make cut to back of piece
                file.write("g1y" + y_end_str + "\n")

        # safety height at end of code
        file.write("g0z30\n")
        file.write("g0z30")
        file.close()

        # let user know the code worked
        popup = Label(root, text="Your G-code was generated successfully and can be found in your documents.").grid(row=13, column=0)
    return

# button to execute function above
Enter = Button(root, text="Generate G-code", command=gen_code, width=20, height=3).grid(row=13, column=1)

root.mainloop()
