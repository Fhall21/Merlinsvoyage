
from content import web_scrapper

#web_scrapper(month_num=9, year=2011)


for year in range(2015, 2014, -1):
	for month_num in range(3, 0, -1):
		web_scrapper(month_num=month_num, year=year)

#Error List:
#Month: 9, 2011, post: 5 (Du lever au coucher)
