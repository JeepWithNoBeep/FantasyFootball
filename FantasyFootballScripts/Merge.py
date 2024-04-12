import os
import pandas as pd
import glob

def WriteXLSX():
	path = './'
	all_files = glob.glob(os.path.join(path, "*.csv"))
	
	# Write FantasyFootballWeekly.xlsx
	print("Writing FantasyFootballWeekly.xlsx")
	writer = pd.ExcelWriter('FantasyFootballWeekly.xlsx', engine='xlsxwriter')
	for f in all_files:
		if 'edit' not in f and 'Previous' not in f:
    			df = pd.read_csv(f)
    			df.to_excel(writer, sheet_name=os.path.basename(f))
	writer.close()
def WriteXLSX_edit():	
	path = './'
	all_files = glob.glob(os.path.join(path, "*.csv"))
	# Write FantasyFootballWeekly_edit.xlsx
	print("Writing FantasyFootballWeekly_edit.xlsx")
	writer = pd.ExcelWriter('FantasyFootballWeekly_edit.xlsx', engine='xlsxwriter')
	for f in all_files:
		if 'edit' in f:
    			df = pd.read_csv(f)
    			df.to_excel(writer, sheet_name=os.path.basename(f))

	writer.close()


	