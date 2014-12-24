#! python2.7

# Feldherren's shiny handy script for converting RM2000 format charsets to VX Ace format.
# It even converts them so they're easily usable with GTBS!
# Just drop this in the directory containing RM2000 format charsets and run it. It'll do all the work.

# Note: requires python 2.7 and the Python Imaging Library (PIL)

from PIL import Image
import os, glob

def convert(infile):
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

for infile in glob.glob("*.bmp"):
	convert(infile)
for infile in glob.glob("*.png"):
	convert(infile)