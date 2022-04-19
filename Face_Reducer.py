from tkinter import *
from numpy import array

# main window for GUI
root = Tk()
root.title('Face Reducer G-code Generator')
root.geometry("800x500")

# Title
title = Label(root, text= "Enter Dimensions for Your Piece and Tool")
title.config(font=('helvetica', 18))
title.grid(row=0, column=0)

# GUI inputs as string variables and will be converted later to floats
pc_diam_hold = StringVar()
tool_diam_hold = StringVar()
z_end_hold = StringVar()

# GUI boxes for entries
pc_diam_Box = Entry(root, textvariable = pc_diam_hold)
pc_diam_Box.grid(row=1, column=1)
pc_diam_Label = Label(text="Piece diameter in mm (exact):")
pc_diam_Label.grid(row=1, column=0)

z_end_box = Entry(root, textvariable = z_end_hold)
z_end_box.grid(row=2, column=1)
z_end_label = Label(text = "Amount you wish to trim the piece by in mm (exact):")
z_end_label.grid(row=2, column=0)

material = StringVar()
material_label = Label(root, text='Select the material of your piece:').grid(row=3, column=0)
material_menu = \
    OptionMenu(root, material, 'Cast Iron', 'Brass, Mild Steels, Carbon Steels', 'Alloy/ Tool Steels (Up to 30 HRC)', 'Hardened Steel, Prehardened Steel, Ti Alloy (30-38 HRC)', 'Hardened Steel, Prehardened Steel, Stainless Steel (38-45 HRC)', 'Aluminium Alloys').grid(row=3, column=1)

flute = StringVar()
flute_label = Label(root, text = 'Select the number of flutes on your end mill:').grid(row=4, column=0)
flute_menu = OptionMenu(root, flute, '2 Flute', '4 Flute').grid(row=4, column=1)

tool_size_hold = StringVar()
tool_label = Label(root, text = 'Select the size of your tool:').grid(row = 5, column = 0)
tool_menu = OptionMenu(root, tool_size_hold, '0.040"', '1/32"', '5/64"', '2.0mm', '1/16"', '1/8"').grid(row=5, column=1)

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


# Function for generating g-code .txt file
def gen_code():
    # converting GUI tool size selection from inch to mm
    # just converting tool diam to approximate diam in mm, does not need to be exact
    # this is just for the size of the cuts the tool will make
    tool_diam = 'Not Input'
    if tool_size_hold.get() == '1/32"':
        tool_diam = 0.8
    if tool_size_hold.get() == '0.040"':
        tool_diam = 1.0
    if tool_size_hold.get() == '1/16"':
        tool_diam = 1.6
    if tool_size_hold.get() == '2.0mm':
        tool_diam = 2.0
    if tool_size_hold.get() == '5/64"':
        tool_diam = 2.0
    if tool_size_hold.get() == '1/8"':
        tool_diam = 3.2

    # convert string inputs to floats to be able to use in code
    # also rounding x and z changes
    pc_diam = float(pc_diam_hold.get())
    z_end = -float(z_end_hold.get())
    x_change1 = tool_diam / 3
    x_change = round(x_change1, 3)
    z_change1 = tool_diam / 15
    z_change = round(z_change1, 3)

    # tool limits for cutting
    # facing the entire piece so x limits span the whole piece
    x_start = 0
    x_end = pc_diam + x_change
    # y limits start at front of piece and go to back
    y_start = -5
    y_end = pc_diam + 5
    # convert to string so they can be used in .txt file
    y_start_str = str(y_start)
    y_end_str = str(y_end)

    # make list of all z values
    zvals = []
    zpos = -z_change
    # for if we only need one z-step
    if zpos <= z_end:
        zpos = z_end

    if zpos == z_end:
        zvals.append(z_end)

    # for if we need multiple z steps
    else:
        while zpos >= z_end:
            zpos1 = round(zpos, 4)
            zvals.append(zpos1)
            zpos -= z_change
            if zpos <= z_end:
                zvals.append(z_end)

# convert to array to be able to call positions
    zvals = array(zvals)

    # make list of all x values
    xvals = []
    xpos = x_start
    while xpos < x_end:
        xpos1 = round(xpos, 3)
        xvals.append(xpos1)
        xpos += x_change
        if xpos >= x_end:
            xvals.append(x_end)
    xvals = array(xvals)

    # open new txt file
    file = open(r'C:\\Users\\Jaime Ortiz.SANDIA\\Documents\\NEW FACING G-CODE (RENAME).txt', 'w')

    # making g-code for cut
    # sweep through all x values for each z value
    # note that we are cutting from front to back and left to right
    # this is so the tool "climbs" the piece which results in the best cuts
    for z in range(len(zvals)):
        zstr = str(zvals[z])
        for x in range(len(xvals)):
            xstr = str(xvals[x])
            # lift tool above piece
            file.write('g1z1\n')
            # go to  x and y position
            file.write("g0y" + y_start_str + "x" + xstr + "\n")
            # lower tool to cutting depth
            file.write("g1z" + zstr + "\n")
            # make cut toward the back of the piece
            file.write("g1y" + y_end_str + "\n")

# safety z value at end of code
    file.write("g0z30\n")
    file.write("g0z30")
    file.close()

# let user know the code has worked
    popup = Label(root, text = "Your G-code was generated successfully and can be found in your documents.").grid(row=7, column = 0)
    return


Enter = Button(root, text="Generate G-code", command = gen_code, width = 20, height = 3).grid(row=7, column=1)


# function for generating speeds and feeds
def show():
    speed = 'Not Input'
    feed = 'Not Input'
    tool_size = 'Not Input'
    # different GUI selections corresponding to list positions above
    if tool_size_hold.get() == '0.040"':
        tool_size = 0
    if tool_size_hold.get() == '1/32"':
        tool_size = 1
    if tool_size_hold.get() == '1/16"':
        tool_size = 2
    # 2.0mm and 5/64" have same speeds and feeds
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

# use tool size number assigned above to call speed and feed values from lists at start of code
# have to make a section for each different material and flute
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
        speed_num = four_fl_speeds_38[tool_size]
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
        # give error if there is no selection in the GUI
        error = Label(root, text='ERROR: NOT ENOUGH INFO TO GENERATE SPEEDS AND FEEDS').grid(row=6, column=0)

# convert to string to be displayed in GUI
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

# generate g-code .txt file and put into documents
but = Button(root, text = 'Generate Speed and Feed', command=show).grid(row=6, column=1)

root.mainloop()
