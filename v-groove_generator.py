from math import sqrt
from tkinter import *

#main window for GUI
root = Tk()
root.title('V-Groove G-code Generator')
root.geometry("1000x500")

#Title
title = Label(root, text = "Enter Parameters for your Piece")
title.config(font=('helvetica', 18))
title.grid(row=0, column=0)

# GUI Inputs are string variables that will be converted to floats later
fib_diam_hold = StringVar()
groove_depth_hold = StringVar()
piece_wid_hold = StringVar()
piece_len_hold = StringVar()
groove_space_hold = StringVar()
num_grooves_hold = StringVar()
endL_hold = StringVar()

#GUI boxes for entries
# fiber diameter
fib_diam_Box = Entry(root, textvariable = fib_diam_hold)
fib_diam_Box.grid(row=3, column=1)
fib_diam_Label = Label(text="Enter the fiber diameter in um (exact):")
fib_diam_Label.grid(row=3, column=0)

# groove depth from top of piece
groove_depth_box = Entry(root, textvariable = groove_depth_hold)
groove_depth_box.grid(row=4, column = 1)
groove_depth_label = Label(text = "Enter the depth of the grooves from the top of the piece in um (exact) (if unknown or want the program to generate it for you, enter '0'):")
groove_depth_label.grid(row=4, column=0)

# groove spacing
groove_space_box = Entry(root, textvariable = groove_space_hold)
groove_space_box.grid(row=5, column=1)
groove_space_label = Label(text = "Enter the spacing between groove vertices in um (exact):")
groove_space_label.grid(row=5, column=0)

# number of grooves
num_grooves_box = Entry(root, textvariable = num_grooves_hold)
num_grooves_box.grid(row=6, column=1)
num_grooves_label = Label(text = "Enter the number of grooves (integer):")
num_grooves_label.grid(row=6, column=0)

# width of piece (side to side)
piece_wid_box = Entry(root, textvariable = piece_wid_hold)
piece_wid_box.grid(row=7, column=1)
piece_wid_label = Label(text = "Enter the width of the piece (side to side) in mm (exact):")
piece_wid_label.grid(row=7, column=0)

# length of piece (front to back)
piece_len_box = Entry(root, textvariable = piece_len_hold)
piece_len_box.grid(row=8, column=1)
piece_len_label = Label(text = "Enter the length of the piece (front to back) in mm (approx to 0.1 mm):")
piece_len_label.grid(row=8, column=0)

# Empty space to the left of the grooves
endL_box = Entry(root, textvariable = endL_hold)
endL_box.grid(row=9, column=1)
endL_label = Label(text = "Enter the amount of space before the grooves on the left side of the piece in mm (exact). **Enter '0' if you want centered grooves**:")
endL_label.grid(row=9, column=0)

material = StringVar()
material_label = Label(root, text='Select the material of your piece:').grid(row=10, column=0)
material_menu = \
    OptionMenu(root, material, 'Cast Iron', 'Brass, Mild Steels, Carbon Steels', 'Alloy/ Tool Steels (Up to 30 HRC)', 'Hardened Steel, Prehardened Steel, Ti Alloy (30-38 HRC)', 'Hardened Steel, Prehardened Steel, Stainless Steel (38-45 HRC)', 'Aluminium Alloys').grid(row=10, column=1)

flute = StringVar()
flute_label = Label(root, text='Select the number of flutes on your tool:').grid(row=11, column=0)
flute_menu = OptionMenu(root, flute, '2 Flute', '4 Flute').grid(row=11, column=1)

tool_size_hold = StringVar()
tool_label = Label(root, text='Select the size of your tool:').grid(row=12, column=0)
tool_menu = OptionMenu(root, tool_size_hold, '0.040"', '1/32"', '5/64"', '2.0mm', '1/16"', '1/8"').grid(row=12, column=1)

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
    white = Label(root, text='                                                                                                                                                                                                  ').grid(row=13, column=0)
    white2 = Label(root, text='                                                                                                                                         ').grid(row=14, column=0)

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
        error = Label(root, text = 'ERROR: NOT ENOUGH INFO TO GENERATE SPEEDS AND FEEDS').grid(row=13, column=0)

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
but = Button(root, text='Generate Speed and Feed', command=show).grid(row=13, column=1)

# function for generating G-code .txt file
def gen_code():
    # get parameters from user entries
    fib_diam = float(fib_diam_hold.get())/1000
    groove_depth = float(groove_depth_hold.get())/1000
    piece_wid = float(piece_wid_hold.get())
    piece_len = float(piece_len_hold.get())
    groove_space = float(groove_space_hold.get())/1000
    num_grooves = int(num_grooves_hold.get())
    endL = float(endL_hold.get())

    # groove depth calculated to be fiber diameter + space underneath the fiber at the bottom of the groove
    groove_depth_str = 'Not Input Yet'
    if groove_depth == 0:   # automatically set groove depth based on fiber diameter if user wants to
        # exact groove depth calculated
        x = sqrt(2*((fib_diam/2)**2)) + fib_diam/2
        # multiply by 1.07 to give a little room for error
        x *= 1.07
        groove_depth = round(x, 4)
        groove_depth_str = str(round(groove_depth*1000, 4))
    else:  # otherwise use user's groove_depth
        groove_depth_str = str(groove_depth)

    # cutting right to left for best quality cuts
    # cutting into the piece
    # start cut at right side of piece
    x_start = piece_len + 5
    x_start_str = str(x_start)
    # finish cut at left side
    x_end = -7
    x_end_str = str(x_end)

    yz_move = -sqrt((groove_space**2)/2) # distance y and z that the tool moves after each cut (same distance since piece is at a 45 degree angle)
    # groove depth is also distance from edge of first/last groove to middle of first/last groove
    groove_wid = 2*groove_depth + (num_grooves-1)*groove_space   # total length of all grooves

    # for centering grooves on piece if user wants
    if endL == 0:
        endL1 = (piece_wid-groove_wid)/2  # space on each side to center grooves
        endL = round(endL1, 4)

# this is just for the first step to get the piece to the first cut position
    endLy = endLz = -sqrt((endL**2)/2)   # z and y coords to go past the empty space at the start. Same distance since piece is at 45 degree angle.
    endLy_str = str(round(endLy, 4))
    first_move_z = -sqrt(2*(groove_depth**2)) + endLz  # first cut needs to be deeper in z axis
    first_move_z_str = str(round(first_move_z, 4))


    # start new .txt file
    file = open(r'C:\\Users\\Jaime Ortiz.SANDIA\\Documents\\NEW G-CODE (RENAME).txt', 'w')
    #raise tool to safe height
    file.write('g1z1\n')
    # go to x and y coordinates
    file.write('g0x' + x_start_str + 'y' + endLy_str + '\n')
    # lower tool to cutting depth
    file.write('g1z' + first_move_z_str + '\n')
    # make cut from right to left
    file.write('g1x' + x_end_str + '\n')

    # making a cut for each groove
    for i in range(1, num_grooves):
        # measuring distance from the end of the piece, not from the previous groove
        ymove_raw = endLy + yz_move*i   # covers all y coordinates
        ymove = round(ymove_raw, 4)
        # convert to string for txt file
        ymove_str = str(ymove)
        # measuring distance from the end of the piece, not from the previous groove
        zmove_raw = first_move_z + yz_move*i    # covers all z coordinates
        zmove = round(zmove_raw, 4)
        # convert to string for txt file
        zmove_str = str(zmove)

        # raise tool to safe height
        file.write('g1z1\n')
        # move tool to x and y position
        file.write('g0x' + x_start_str + 'y' + ymove_str + '\n')
        # lower tool to cutting height
        file.write('g1z' + zmove_str + '\n')
        # make cut from right to left
        file.write('g1x' + x_end_str + '\n')

    # raise tool to safety height at end of code
    file.write('g0z30\n')
    file.write('g0z30')
    file.close()

    # let user know the code file is ready
    popup = Label(root, text = "Your G-code was generated successfully and can be found in your documents.").grid(row=14, column = 0)
    # let user know the calculated groove depth in case they want to double check it
    popup = Label(root, text="Calculated Groove Depth:" + groove_depth_str + "um").grid(row=15, column=0)
    return

# button to generate code
Enter = Button(root, text="Generate G-code", command = gen_code, width = 24, height = 3).grid(row=14, column=1)


root.mainloop()