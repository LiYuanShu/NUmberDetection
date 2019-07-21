import pymysql
strr='13005930000'
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='phone', charset='utf8')
cur = conn.cursor()
print(strr[0:3])
cur.execute('select * from placenumber where phone=' + strr[0:7])
rows = cur.fetchall()
print(rows)
if (rows == ()):
	print('查询不到结果，可能是数据库不够强大呢')
else:
	for row in rows:
		print(row)