#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# AUTHOR : Fernando del Campo (fernando.delcampo@inria.cl)
# Copyright (c) INRIA, 2009-2015. All Rights Reserved
# Licensed under the GNU LGPL. For full terms see the file COPYING.


SUCCEEDED_IMPORTING_PIL = True

import os, sys

# http://www.pythonware.com/products/pil/
try:
	from PIL import Image
except ImportError:
	SUCCEEDED_IMPORTING_PIL = False


# Tile IDs are generated following this pattern:
# -------------------------------------
# | AL1 | AR1 | BL1 | BR1 | CL1 | CR1 |
# -------------------------------------
# | AL2 | AR2 | BL2 | BR2 | CL2 | CR2 |
# -------------------------------------
# | AL3 | AR3 | BL3 | BR3 | CL3 | CR3 |
# -------------------------------------
# | AL4 | AR4 | BL4 | BR4 | CL4 | CR4 |
# -------------------------------------


CMD_LINE_HELP = "Wallpaper for Wall-display Script\n\nUsage:\n\n" + \
	" \twallpaperWalldisplay <src_image_path> <target_dir> [options]\n\n" + \
	"Options:\n\n"+\
	"\t-im\t\tprocessing pipeline: PIL and ImageMagick (default)\n"+\
	"\t-w=N\t\twidth size screen (N in pixels) default 1920\n"+\
	"\t-h=N\t\theight size screen (N in pixels) default 1080\n"+\
	"\t-bw=N\t\tbezel width size screen (N in pixels) default 80\n"+\
	"\t-bh=N\t\tbezel height size screen (N in pixels) default 100\n"+\
	"\t-rows=N\t\tCount of rows default 4\n"+\
	"\t-cols=N\t\tCount of cols default 6\n"+\
	"\t-displace-x=N\t\tDisplace x-axes in pixels\n"+\
	"\t-displace-y=N\t\tDisplace y-axes in pixels\n"+\
	"\t-format=t\tt output tiles in PNG (png), JPEG (jpg) or TIFF (tiff)\n"


WIDTH = 1920
HEIGHT = 1080
BEZELWIDTH = 80
BEZELHEIGHT = 100
ROWS = 4
COLS = 6
NAMEROWS = [1, 2, 3, 4]
NAMECOLS = ['al', 'ar', 'bl', 'br', 'cl', 'cr']
DISPLACE_X = 0
DISPLACE_Y = 0

OUTPUT_TYPE_PNG = "png"
OUTPUT_TYPE_JPEG = "jpg"
OUTPUT_TYPE_TIFF = "tiff"
OUTPUT_TYPE = OUTPUT_TYPE_JPEG

################################################################################
# Create target directory if it does not exist yet
################################################################################
def createTargetDir():
	if not os.path.exists(TGT_DIR):
		print "Creating target directory %s" % TGT_DIR
		os.mkdir(TGT_DIR)

def buildTiles(tileName, x, y, src_sz, im):
	print "(%s, %d, %d, [%d, %d])" % (tileName, x, y, src_sz[0], src_sz[1])
	#if x+WIDTH > src_sz[0]:

	#ccl = "convert %s -crop %dx%d+%d+%d -background black -extent %dx%d -quality 95 %s" % (SRC_PATH, WIDTH, HEIGHT, x, y, WIDTH, HEIGHT, TGT_DIR+"/"+tileName)
	
	if x >= 0 and y >= 0 and x < src_sz[0] and y < src_sz[1]:
		ccl = "convert %s -crop %dx%d+%d+%d -background black -extent %dx%d -quality 95 %s" % (SRC_PATH, WIDTH, HEIGHT, x, y, WIDTH, HEIGHT, TGT_DIR+"/"+tileName)
	elif x < 0 and y >= 0 and y < src_sz[1]:
		ccl = "convert %s -crop %dx%d+%d+%d -background black -gravity East -extent %dx%d +repage -quality 95 %s" % (SRC_PATH, WIDTH, HEIGHT, x, y, WIDTH, HEIGHT, TGT_DIR+"/"+tileName)
	elif y < 0 and x >= 0 and x < src_sz[0]:
		ccl = "convert %s -crop %dx%d+%d+%d -background black -gravity North -extent %dx%d +repage -quality 95 %s" % (SRC_PATH, WIDTH, HEIGHT, x, y, WIDTH, HEIGHT, TGT_DIR+"/"+tileName)
	elif x < 0 and y < 0:
		ccl = "convert %s -crop %dx%d+%d+%d -background black -gravity NorthEast -extent %dx%d +repage -quality 95 %s" % (SRC_PATH, WIDTH, HEIGHT, x, y, WIDTH, HEIGHT, TGT_DIR+"/"+tileName)
	else:
		ccl = "echo Other case"
	os.system(ccl)
	print "Cropping: %s" % ccl


################################################################################
# Create tiles and ZUIST XML scene from source image
################################################################################
def processSrcImg():
	global DISPLACE_X, DISPLACE_Y 
	# source image
	print "Loading source image from %s" % SRC_PATH
	im = Image.open(SRC_PATH)
	src_sz = im.size
	if COLS*(WIDTH+BEZELWIDTH)-BEZELWIDTH > src_sz[0] and DISPLACE_X == 0:
		DISPLACE_X = (src_sz[0]-(COLS*(WIDTH+BEZELWIDTH)-BEZELWIDTH)) / 2

	if ROWS*(HEIGHT+BEZELHEIGHT)-BEZELHEIGHT > src_sz[1] and DISPLACE_Y == 0:
		DISPLACE_Y = (src_sz[1]-(ROWS*(HEIGHT+BEZELHEIGHT)-BEZELHEIGHT)) / 2
	


	for j in range(0, COLS):
		for i in range(0, ROWS):
			tileName = "%s%s.%s" % (NAMECOLS[j], NAMEROWS[i], OUTPUT_TYPE)
			buildTiles(tileName, j*(WIDTH+BEZELWIDTH)+DISPLACE_X, i*(HEIGHT+BEZELHEIGHT)+DISPLACE_Y, src_sz, im)



################################################################################
# main
################################################################################
if len(sys.argv) > 2:
	SRC_PATH = os.path.realpath(sys.argv[1])
	TGT_DIR = os.path.realpath(sys.argv[2])
	if len(sys.argv) > 3:
		for arg in sys.argv[3:]:
			if arg.startswith("-w="):
				WIDTH = int(arg[len("-w="):])
			elif arg.startswith("-h"):
				HEIGHT = int(arg[len("-h="):])
			elif arg.startswith("-bw="):
				BEZELWIDTH = int(arg[len("-bw="):])
			elif arg.startswith("-bh"):
				BEZELHEIGHT = int(arg[len("-bh="):])
			elif arg.startswith("-format"):
				OUTPUT_TYPE = arg[len("-format="):]
			elif arg.startswith("-displace-x"):
				DISPLACE_X = int(arg[len("-displace-x="):])
			elif arg.startswith("-displace-y"):
				DISPLACE_Y = int(arg[len("-displace-y="):])

	if not SUCCEEDED_IMPORTING_PIL:
		print "PIL not available"
		sys.exit(0)

	createTargetDir()
	processSrcImg()

