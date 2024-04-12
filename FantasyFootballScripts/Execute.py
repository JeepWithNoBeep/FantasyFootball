import os 
import pandas
from CreateEdits import CreateEdit
from Merge import *
from FixData import CreatePreviousTotalCSV

print("finding week number")
# gets the raw Weekly file
prefixed = [filename for filename in os.listdir('.') if filename.startswith("FF_Week") and "edit" not in filename] # Gets All FF_Week files

max = 0
# gets the current week number
for i in prefixed:
	a,b = i.split('FF_Week') #FF_Week , [WeekNumber].csv
	b, c = b.split('.') ##[WeekNumber], .csv
	if not max > int(b): 
		max = int(b)
max =max + 1 #max + 1  = current week number

# Create new weekly file:
print("Webscraping for week {}".format(max))
os.system("python3 WebScrape.py {}".format(max)) 

# new file name and edited file name
file = "FF_Week" + str(max) + ".csv"
file_edit = "FF_Week" + str(max) + "_edit.csv"

# Create edited weekly files
print("Creating edited file:" + file_edit)
CreateEdit(file, file_edit, max)

#FixData
print("Getting Previous Points")
CreatePreviousTotalCSV(max)

# generate workbook
print("Creating new XLSX for files.....")
WriteXLSX()
WriteXLSX_edit()

