import os
import sys
import glob

stats = [0,0]

def Check_Empty(name):
	return (os.stat(name).st_size == 0)

def Print_Stats():
	ntrue = stats[1]
	nfalse = stats[0]
	total = ntrue + nfalse


	percent_text_det = (ntrue / total) * 100

	print("\nOut of %s images, tesseract detected text for %s images. %f%% text detection.\n" %(total,ntrue,percent_text_det))

def main():

	if len(sys.argv) != 2:
		print("Error: Please specify file name or 'all'")
		return -1
	else:

		if sys.argv[1] == 'all':

			

			file_list = []
			for filename in glob.glob('results/*.txt'):
				file_list.append(filename)

			# Check all text files
			for filename in file_list:
				stats[Check_Empty(filename)]+= 1

			Print_Stats()
			
		else:
			fname = sys.argv[1]
			print(Check_Empty(fname))
			

if __name__ == "__main__":
	main()



