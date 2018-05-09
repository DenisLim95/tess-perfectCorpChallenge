from PIL import Image
from pytesseract import image_to_string
import sys
import glob, os


def Usage():
	print("Usage:")
	print("For all files: 'script_denis.py all [0/1/2]'\n")
	print("For specific file: 'script_denis.py [filename] [0/1/2]'\n")
	print("Third argument: \n")
	print("		= 1 if wanting to pre-process with extract.py\n")
	print("		= 2 if wanting to pre-process with ImageMagic TextCleaner\n")
	print("		= 0 if wanting no pre-process\n")
	return -1

def Run_Extract(filename, ext):
	new_file_name = filename + '_Ext.png'
	os.system("python extract.py %s.%s %s" %(filename, ext, new_file_name))
	return new_file_name

def Run_TextCleaner(filename, ext):
	new_file_name = filename + '_TxtCL.png'
	# need to fix this
	os.system("./textcleaner %s.%s %s" %(filename, ext, new_file_name))
	return new_file_name


def ProcessOne(run_extract):


	imgname_t = sys.argv[1]
	ext_index = imgname_t.find('.')

	if ext_index == -1 or ext_index == 0:
		print("Invalid file name...")
		return -1

	imgname = imgname_t[0:ext_index]
	print("imgname: %s" % (imgname))
	imgext = imgname_t[ext_index+1:]
	print("imgext: %s" %imgext)
	print("runextract: %s" % (run_extract))

	if int(run_extract) == 1:
		imgname_t = Run_Extract(imgname, imgext)
	elif int(run_extract) == 2:
		imgname_t = Run_TextCleaner(imgname, imgext)

	print("pre-processed img created: %s" % imgname_t)
	img = Image.open(imgname_t)
	text = image_to_string(img)

	

	if int(run_extract) == 1:
		# Create text Output
		here = os.path.dirname(os.path.realpath(__file__))
		subdir = "results"
		filename = imgname + "_extract_OUT.txt"
		filepath = os.path.join(here, subdir, filename)

		# create your subdirectory
		if not os.path.exists(here+"/"+ subdir):
			os.mkdir(os.path.join(here, subdir))
		file = open(filepath, 'w')


	elif int(run_extract) == 2:
		# Create text Output
		here = os.path.dirname(os.path.realpath(__file__))
		subdir = "results"
		filename = imgname + "_textCleaner_OUT.txt"
		filepath = os.path.join(here, subdir, filename)

		# create your subdirectory
		if not os.path.exists(here+"/"+ subdir):
			os.mkdir(os.path.join(here, subdir))
		file = open(filepath, 'w')

	else:
		# Create text Output
		here = os.path.dirname(os.path.realpath(__file__))
		subdir = "results"
		filename = imgname + "_OUT.txt"
		filepath = os.path.join(here, subdir, filename)

		# create your subdirectory
		if not os.path.exists(here+"/" + subdir):
			os.mkdir(os.path.join(here, subdir))
		file = open(filepath, 'w')

	file.write(text)
	file.close()
	
	# Print
	print("Tesseract output: \n")
	print(text)

def ProcessAll(run_extract):

	image_list = []
	for filename in glob.glob('*.jpg'):
		image_list.append(filename)

	for filename in glob.glob('*.jpeg'):
		image_list.append(filename)
	
	for filename in glob.glob('*.png'):
		image_list.append(filename)


	# Import all images
	for filename in image_list:

		imgname_t = filename
		ext_index = imgname_t.find('.')

		if ext_index == -1 or ext_index == 0:
			print("Invalid file name...")
			return -1

		imgname = imgname_t[0:ext_index]
		print("IMGNAME: %s" %(imgname))
		imgext = imgname_t[ext_index+1:]

		if int(run_extract) == 1:
			imgname_t = Run_Extract(imgname, imgext) 
		elif int(run_extract) == 2:
			imgname_t = Run_TextCleaner(imgname, imgext)

		img = Image.open(imgname_t)
		text = image_to_string(img)

		if int(run_extract) == 1:
		# Create text Output
			here = os.path.dirname(os.path.realpath(__file__))
			subdir = "results"
			filename = imgname + "_extract_OUT.txt"
			filepath = os.path.join(here, subdir, filename)

			# create your subdirectory
			if not os.path.exists(here+"/"+ subdir):
				os.mkdir(os.path.join(here, subdir))
			file = open(filepath, 'w')

		elif int(run_extract) == 2:
			# Create text Output
			here = os.path.dirname(os.path.realpath(__file__))
			subdir = "results"
			filename = imgname + "_textCleaner_OUT.txt"
			filepath = os.path.join(here, subdir, filename)

			# create your subdirectory
			if not os.path.exists(here+"/"+ subdir):
				os.mkdir(os.path.join(here, subdir))
			file = open(filepath, 'w')

		else:
			# Create text Output
			here = os.path.dirname(os.path.realpath(__file__))
			subdir = "results"
			filename = imgname + "_OUT.txt"
			filepath = os.path.join(here, subdir, filename)

			# create your subdirectory
			if not os.path.exists(here+"/" + subdir):
				os.mkdir(os.path.join(here, subdir))
			file = open(filepath, 'w')

		file.write(text)
		file.close()

		# Print
		print("Tesseract Output for image '%s'\n" %(filename))
		print(text)
		

def CleanUp():
	# Ext / TxtCL.png'
	newImages_list = []

	for newname in glob.glob('*Ext.png'):
		newImages_list.append(newname)

	for newname in glob.glob('*TxtCL.png'):
		newImages_list.append(newname)

	# Create new folder for new files created.
	newpath = 'pre-processed-imgs'
	if not os.path.exists(newpath):
		os.makedirs(newpath)


	# Move new files to new folder
	for file in newImages_list:
		os.rename(file, newpath + '/' + file)

def main():

	if len(sys.argv) != 3:
		Usage()
	elif int(sys.argv[2]) < 0 or int(sys.argv[2]) > 2:
		Usage()
	else:
		run_extract = sys.argv[2]
		if sys.argv[1] == 'all':
			print("Processing all image files...")
			ProcessAll(run_extract)
		else:
			print("Processing one file...")
			ProcessOne(run_extract)


	# finally, move created files to new folder
	if int(run_extract):
		CleanUp()


if __name__ == "__main__":
	main()



