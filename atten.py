import warnings
warnings.filterwarnings("ignore")
def attendance_calculator(username,password,since='2022-07-07',till=None):
	import requests
	import pandas as pd
	with requests.session() as s:
	  s.post("""https://portal.svkm.ac.in/usermgmt/login""",data={"jspname":"nm","username":username,"password":password},verify=False)
	  s.get("https://portal.svkm.ac.in/SDSOS-NM-M/homepage")
	  zz=s.get("https://portal.svkm.ac.in/SDSOS-NM-M/viewDailyAttendanceByStudent")
	  html=(zz.text)

	df=pd.read_html(html)[0].replace({"Attendance":{"U":0,"P":1}})
	df["Class Date"]=pd.to_datetime(df["Class Date"],dayfirst=True)
	df.sort_values(by="Class Date",inplace=True)
	df.set_index("Class Date",inplace=True)
	df1= df[since:] if till is None else df[since:till]
	df1=df1.groupby("Subject").agg(["count","sum"])["Attendance"]
	df1["Attendance Percentage"]=df1["sum"]/df1["count"]*100
	df1.columns=["Total Classes","Attended","Percentage Attended"]
	print(df1)
	
import sys
l=sys.argv[1:]
attendance_calculator(*l)
