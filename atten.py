import warnings
warnings.filterwarnings("ignore")
import requests
import pandas as pd
def attendance_calculator(username,password,since='2022-07-07',till=None):
	with requests.session() as s:
		homepage=s.post("""https://portal.svkm.ac.in/usermgmt/login""", data ={"jspname":"nm", "username":username, "password" : password }, verify=False)
		url=homepage.url.rstrip('homepage')
		attendance_page=s.get(url+"viewDailyAttendanceByStudent")
		html=(attendance_page.text)
	df=pd.read_html(html)[0].replace({"Attendance":{"U":0,"P":1}})
	df["Class Date"]=pd.to_datetime(df["Class Date"],dayfirst=True)
	df.sort_values(by="Class Date",inplace=True)
	df.set_index("Class Date",inplace=True)
	df1= df[since:] if till is None else df[since:till]
	df1=df1.groupby("Subject").agg(["count","sum"])["Attendance"]
	df1["Attendance Percentage"]=df1["sum"]/df1["count"]*100
	df1.columns=["Total Classes","Attended","Percentage Attended"]
	df2 = pd.DataFrame( [[df1["Total Classes"].sum(),df1["Attended"].sum(), df1['Attended'].sum()/df1['Total Classes'].sum()*100]],index=['Aggregate'],columns=df1.columns)
	df = pd.concat( [df1, df2]) 
	print(df)
	
import sys
l=sys.argv[1:]
attendance_calculator(*l)
