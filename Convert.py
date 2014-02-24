from PIL import Image
import os, glob
import optparse

# Arguments: from, to
# From: 2000/2003, XP, VX
# To: XP, VX

# Only 2000/2003

parser = optparse.OptionParser()

parser.add_option('-f', '--from', help='Format converted from; may be 2000, XP or VX', dest='f', action='store_true')
parser.add_option('-t', '--to', help='Format converted to; may be XP or VX', dest='t', action='store_true')
parser.add_option('-g', '--gtbs', help='Generate battlers and battler icons for GTBS', dest='gtbs', default=False) # generates icons and splits battler sets for everything.

mandatory = ['f', 't']

for m in mandatories:
    if not opts.__dict__[m]:
		print "A mandatory option is missing!\n"
		parser.print_help()
		exit(-1)

def split_eight(charset):
	single_width = width/4
	single_height = height/2
	icon_width
	
	for y in range(0,2):
		for x in range(0,4):
			charsets = []
			x1 = single_width * x
			y1 = single_height * y
			x2 = x1 + single_width
			y2 = y1 + single_height
			charsets.append(charset.crop((x1,y1,x2,y2)))
	
	return charsets

def generate_icon(charset, single_width, single_height):
	# takes a single character's charset (AFTER processing to target format) and generates an icon for use with GTBS
	if opts.t is 'XP':
		icon_width = single_width/4
	else:
		icon_width = single_width/3
	icon_height = single_height/2
	
	icon = charset.crop((icon_width,0,icon_width*2,icon_height))
	
	return icon
			
def 2000_to_VX():
	for infile in glob.glob("*.bmp"):
		file, ext = os.path.splitext(infile)
		p = os.path.dirname(os.path.abspath(__file__))
		if not os.path.exists(p + "\\Battlers"): os.makedirs(p + "\\Battlers")
		if not os.path.exists(p + "\\Characters"): os.makedirs(p + "\\Characters")
		
		im = Image.open(infile)
		width, height = im.size
		converted = Image.new('RGB',(width,height))
		
		if opts.f is 'XP':
			converted = Image.new('RGB',(width-(width/4),height))
		elif opts.f is 'VX':
			if file[:1] is '$':
				# image is already only a single character, so there's no need to split it
				converted = Image.new('RGB',(width+(width/3),height))
			else:
				converted = Image.new('RGB',(width,height))
		elif opts.f is '2000':
			converted = Image.new('RGB',(width,height))
		
		if opts.f is '2000':
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
			
			converted.resize((576,512)).save("Characters\\[" + f + "] " + file + ".png", 'PNG')
			converted.resize((576,512)).save("Battlers\\[" + f + "] " + file + ".png", 'PNG')
			
			single_X = 72#*2
			single_Y = 128#*2
			icon_width = single_X/3
			icon_height = single_Y/4
			
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
		elif opts.f is 'XP':
			# four columns where everything else needs three
			# remove first column
			col_x = width/4
			col_y = height
			
			converted.paste(im.crop(col_x,0,width,col_y),(0,0,col_x*3,col_y))
		elif opts.f is 'VX':
			# three columns where XP wants four, in each character's specific set
			if file[:1] is '$':
				# charset is already a single character
				# copy second column to fourth
				col_x = width/3
				col_y = height
			else:
				# charset is a set of eight
		# # Resize converted image
		# converted = converted.resize((576,512))
		
		# Save converted image in PNG format
		
		if opts.f is '2000':
		
		# Split whole charset into separate characters
		
	
# def 2000_to_VX():
	# for infile in glob.glob("*.bmp"):
		# file, ext = os.path.splitext(infile)
		# p = os.path.dirname(os.path.abspath(__file__))
		# if not os.path.exists(p + "\\Battlers"): os.makedirs(p + "\\Battlers")
		# if not os.path.exists(p + "\\Characters"): os.makedirs(p + "\\Characters")
		# im = Image.open(infile)
		# converted = Image.new('RGB',(288,256))
		
		# # move up-facing poses to the correct position
		# converted.paste(im.crop((0,0,288,32)), (0,96,288,128))
		# converted.paste(im.crop((0,128,288,160)), (0,224,288,256))
		
		# # move right-facing poses to the correct position
		# converted.paste(im.crop((0,32,288,64)), (0,64,288,96))
		# converted.paste(im.crop((0,160,288,192)), (0,192,288,224))
		
		# # move down-facing poses to the correct position
		# converted.paste(im.crop((0,64,288,96)), (0,0,288,32))
		# converted.paste(im.crop((0,192,288,224)), (0,128,288,160))
		
		# # move left-facing poses to the correct position
		# converted.paste(im.crop((0,96,288,128)), (0,32,288,64))
		# converted.paste(im.crop((0,224,288,256)), (0,160,288,192))
		
		# # # Resize converted image
		# # converted = converted.resize((576,512))
		
		# # Save converted image in PNG format
		# converted.resize((576,512)).save("Characters\\[VX] " + file + ".png", 'PNG')
		# converted.resize((576,512)).save("Battlers\\[VX] " + file + ".png", 'PNG')
		
		# single_X = 72#*2
		# single_Y = 128#*2
		# icon_width = single_X/3
		# icon_height = single_Y/4
		
		# # Split whole charset into separate characters
		
		# for y in range(0,2):
			# for x in range(0,4):
				# x1 = single_X * x
				# y1 = single_Y * y
				# x2 = x1 + single_X
				# y2 = y1 + single_Y
				# single = converted.crop((x1,y1,x2,y2))
				# single.resize((144,256)).save("Battlers\\$[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
				# single.resize((144,256)).save("Characters\\$[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')
				# pose_X1 = icon_width
				# pose_Y1 = 0
				# pose_X2 = icon_width*2
				# pose_Y2 = icon_height
				# icon = single.crop((pose_X1,pose_Y1,pose_X2,pose_Y2))
				# icon.resize((icon_width*2,icon_height*2)).save("Battlers/[VX] " + file + " " + str(x) + "-" + str(y) + ".png", 'PNG')