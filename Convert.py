#!python2.7

from PIL import Image
import os
import glob
import argparse

# Arguments: from, to
# From: 2000/2003, XP, VX
# To: XP, VX
# Optional: GTBS

# For XP, GTBS simply matched database enemy graphic with charset by name; no need for the charset to be imported to
# battlers, too
#
# VX just does it the same way as VX Ace; in battlers, battler (icon) and $battler (charset). In charsets, $charset
# OR, optionally for actors, just a full copy of the charset in battlers.

parser = argparse.ArgumentParser(description='Converts charset resources from one RPG Maker format to another; '
                                             'optionally produces GTBS-format resources.')

parser.add_argument('path', help='Path to imagery to convert')
parser.add_argument('-f', help='RPG Maker format converted from; may be 2000, XP or VX', required=True)
parser.add_argument('-t', help='RPG Maker format converted to; may be XP or VX', required=True)

# GTBS mode: also generates icons and split battler and charsets for everything.
parser.add_argument('-g', '--gtbs', help='Generate battlers and battler icons for GTBS', action='store_true')

args = parser.parse_args()

valid_format_from = {'2000', 'vx', 'xp'}
valid_format_to = {'xp', 'vx'}

path = args.path
format_from = args.f.lower
format_to = args.t.lower
problem = False

p = os.path.dirname(os.path.abspath(__file__))
charset_path = os.path.join(p, "Characters")
battlers_path = os.path.join(p, "Battlers")

# Creates folder for characters if folder does not already exist
if not os.path.exists(charset_path):
    os.makedirs(charset_path)
# If generating resources for GTBS, also generates folder for battlers.
if args.gtbs:
    if not os.path.exists(battlers_path):
        os.makedirs(battlers_path)

if format_from not in valid_format_from:
    print "Invalid argument: 'from' must be 2000, XP or VX"
    problem = True

if format_to not in valid_format_to:
    print "Invalid argument: 'to' must be XP or VX"
    problem = True

if not os.path.exists(path):
    print "Invalid argument: 'path' must be a valid path"
    problem = True


def split_eight(charset, width, height):
    single_width = width/4
    single_height = height/2

    for y in range(0,2):
        for x in range(0,4):
            charsets = []
            x1 = single_width * x
            y1 = single_height * y
            x2 = x1 + single_width
            y2 = y1 + single_height
            charsets.append(charset.crop((x1,y1,x2,y2)))

    return charsets


def generate_icon(charset, single_width, single_height, t):
    # takes a single character's charset (AFTER processing to target format) and generates an icon for use with GTBS
    if t is 'XP':
        icon_width = single_width/4
    else:
        icon_width = single_width/3
    icon_height = single_height/2

    icon = charset.crop((icon_width, 0, icon_width*2, icon_height))

    return icon


def convert(t, f, image, gtbs=False):
    file, ext = os.path.splitext(image)

    im = Image.open(image)
    width, height = im.size

    if f is 'XP':
        if t is not 'XP':
            # XP charsets are always a single character with sixteen poses, but none of the target formats other than XP
            # have more than three poses in any given direction
            converted = Image.new('RGB', (width-(width/4), height))
        else:
            # Converting from XP to XP - user just wants to make GTBS graphics?
            converted = Image.new('RGB', (width, height))
    elif f is 'VX':
        if file[:1] is '$':
            # image is already only a single character, so there's no need to split it
            converted = Image.new('RGB',(width+(width/3),height))

    converted = Image.new('RGB', (width, height))

    # split image into 4x2 charsets if 2000/2003 format or VX format and not single-charset
    if f == '2000':
        charsets = split_eight(im, width, height)
    elif f == 'vx' and file[:1] is not '$':
        charsets = split_eight(im, width, height)


if not problem:
    for infile in glob.glob(os.path.join(path, "*.png")):
        convert(format_from, format_to, infile, args.gtbs)
    if format_from == '2000':
        for infile in glob.glob(os.path.join(path, "*.bmp")):
            convert(format_from, format_to, infile, args.gtbs)
    if format_from == 'xp' or format_from == 'vx':
        for infile in glob.glob(os.path.join(path, "*.jpg")):
            convert(format_from, format_to, infile, args.gtbs)


# def convert_2000_to_vx():
#     for infile in glob.glob("*.bmp"):
#         file, ext = os.path.splitext(infile)
#         p = os.path.dirname(os.path.abspath(__file__))
#         if not os.path.exists(p + "\\Battlers"): os.makedirs(p + "\\Battlers")
#         if not os.path.exists(p + "\\Characters"): os.makedirs(p + "\\Characters")
#
#         im = Image.open(infile)
#         width, height = im.size
#         converted = Image.new('RGB',(width,height))
#
#         if args.f is 'XP':
#             converted = Image.new('RGB',(width-(width/4),height))
#         elif args.f is 'VX':
#             if file[:1] is '$':
#                 # image is already only a single character, so there's no need to split it
#                 converted = Image.new('RGB',(width+(width/3),height))
#             else:
#                 converted = Image.new('RGB',(width,height))
#         elif args.f is '2000':
#             converted = Image.new('RGB',(width,height))
#
#         if args.f is '2000':
#             # move up-facing poses to the correct position
#             converted.paste(im.crop((0,0,288,32)), (0,96,288,128))
#             converted.paste(im.crop((0,128,288,160)), (0,224,288,256))
#
#             # move right-facing poses to the correct position
#             converted.paste(im.crop((0,32,288,64)), (0,64,288,96))
#             converted.paste(im.crop((0,160,288,192)), (0,192,288,224))
#
#             # move down-facing poses to the correct position
#             converted.paste(im.crop((0,64,288,96)), (0,0,288,32))
#             converted.paste(im.crop((0,192,288,224)), (0,128,288,160))
#
#             # move left-facing poses to the correct position
#             converted.paste(im.crop((0,96,288,128)), (0,32,288,64))
#             converted.paste(im.crop((0,224,288,256)), (0,160,288,192))
#
#             converted.resize((576,512)).save("Characters\\[" + f + "] " + file + ".png", 'PNG')
#             converted.resize((576,512)).save("Battlers\\[" + f + "] " + file + ".png", 'PNG')
#
#             single_X = 72#*2
#             single_Y = 128#*2
#             icon_width = single_X/3
#             icon_height = single_Y/4
#
#             for y in range(0,2):
#                 for x in range(0,4):
#                     x1 = single_X * x
#                     y1 = single_Y * y
#                     x2 = x1 + single_X
#                     y2 = y1 + single_Y
#                     single = converted.crop((x1,y1,x2,y2))
#                     single.resize((144,256)).save("Battlers\\$[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
#                     single.resize((144,256)).save("Characters\\$[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
#                     pose_X1 = icon_width
#                     pose_Y1 = 0
#                     pose_X2 = icon_width*2
#                     pose_Y2 = icon_height
#                     icon = single.crop((pose_X1,pose_Y1,pose_X2,pose_Y2))
#                     icon.resize((icon_width*2,icon_height*2)).save("Battlers/[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
#         elif args.f is 'XP':
#             # four columns where everything else needs three
#             # remove first column
#             col_x = width/4
#             col_y = height
#
#             converted.paste(im.crop(col_x,0,width,col_y),(0,0,col_x*3,col_y))
#         elif args.f is 'VX':
#             # three columns where XP wants four, in each character's specific set
#             if file[:1] is '$':
#                 # charset is already a single character
#                 # copy second column to fourth
#                 col_x = width/3
#                 col_y = height
#             else:
#                 # charset is a set of eight
#         # # Resize converted image
#         converted = converted.resize((576,512))
#
#         # # Save converted image in PNG format
#
#         # if args.f is '2000':
#
#         # # Split whole charset into separate characters


def convert_2000_to_VX():
    for infile in glob.glob("*.bmp"):
        file, ext = os.path.splitext(infile)
        p = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(p + "\\Battlers"): os.makedirs(p + "\\Battlers")
        if not os.path.exists(p + "\\Characters"): os.makedirs(p + "\\Characters")
        im = Image.open(infile)
        converted = Image.new('RGB',(288,256))

        # move up-facing poses to the correct position
        converted.paste(im.crop((0,0,288,32)), (0,96,288,128))
        converted.paste(im.crop((0,128,288,160)), (0,224,288,256))

        # move right-facing poses to the correct position
        converted.paste(im.crop((0,32,288,64)), (0,64,288,96))
        converted.paste(im.crop((0,160,288,192)), (0,192,288,224))

        # move down-facing poses to the correct position
        converted.paste(im.crop((0,64,288,96)), (0,0,288,32))
        converted.paste(im.crop((0,192,288,224)), (0,128,288,160))

        # move left-facing poses to the correct position
        converted.paste(im.crop((0,96,288,128)), (0,32,288,64))
        converted.paste(im.crop((0,224,288,256)), (0,160,288,192))

        # # Resize converted image
        # converted = converted.resize((576,512))

        # Save converted image in PNG format
        converted.resize((576,512)).save("Characters\\[VX] " + file + ".png", 'PNG')
        converted.resize((576,512)).save("Battlers\\[VX] " + file + ".png", 'PNG')

        single_X = 72#*2
        single_Y = 128#*2
        icon_width = single_X/3
        icon_height = single_Y/4

        # Split whole charset into separate characters

        for y in range(0,2):
            for x in range(0,4):
                x1 = single_X * x
                y1 = single_Y * y
                x2 = x1 + single_X
                y2 = y1 + single_Y
                single = converted.crop((x1,y1,x2,y2))
                single.resize((144,256)).save("Battlers\\$[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
                single.resize((144,256)).save("Characters\\$[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
                pose_X1 = icon_width
                pose_Y1 = 0
                pose_X2 = icon_width*2
                pose_Y2 = icon_height
                icon = single.crop((pose_X1,pose_Y1,pose_X2,pose_Y2))
                icon.resize((icon_width*2,icon_height*2)).save("Battlers/[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')