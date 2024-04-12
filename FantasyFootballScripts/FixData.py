import pandas as pd

def CreatePreviousTotalCSV(weekNumber):
	if weekNumber > 1:
		fileName = "PreviousPoints_Week" + str(weekNumber) + ".csv"
		previous_points = []
		name = []
		date = []
		df = pd.read_csv ('FF_Week' + str(weekNumber - 1) + '_edit.csv', header = 0)
		for i in df["PLAYER NAME"]:
			name.append(i)
		for i in df["TOTAL"]:
			previous_points.append(i)
		for i in df["DATE"]:
			date.append(i)
		df2 = pd.DataFrame()
		df2['PLAYER NAME'] = name
		df2['PREVIOUS TOTAL'] = previous_points
		df2['DATE']= date
		df2.to_csv(fileName, index = False)
	else:
		print("Week 1, No previous data")

