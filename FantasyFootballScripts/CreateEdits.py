import pandas
import numpy as np
import os
from datetime import datetime, timedelta

def CreateEdit(filename, filename_edit, weekN):
  weekN -= 1
  df2 = pandas.read_csv(filename)
  df2[['PASSING COMPLETION', 'PASSING ATTEMPTS']]= df2['PASSING C/A'].str.split('/', expand = True)
  opponent = []
  location = []
  for i in df2["OPP"]:
    if i.startswith('@'):
      opponent.append(i.split('@')[1])
      location.append("Away")
    else:
      opponent.append(i)
      location.append("Home")
  df2['Opponent'] = opponent
  df2['Location'] = location
  df2 = df2.drop('PASSING C/A', axis = 1)
  df2 = df2.replace('--', np.NaN)
  df2 = df2.drop('OPP', axis = 1)
  df2[df2.columns[4:20]] = df2[df2.columns[4:20]].astype(float)
  df2['rank'] = df2.groupby('PLAYER POSITION')['TOTAL'].rank(ascending=False)
  date_string = "2023-09-12 00:00:00"
  date_ = datetime.fromisoformat(date_string)
  week_date = (date_ + timedelta(days = (weekN*7))).strftime('%m-%d-%y')
  df2['DATE']= week_date
  df2.to_csv(filename_edit, index = False)





