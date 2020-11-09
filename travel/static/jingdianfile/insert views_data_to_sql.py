import pymysql

result=[]
f=open('summary1__OK.txt','r').read().split('|\n')
for item in f:
    print(item)
    result.append(eval(item))
print(result)

db=pymysql.connect(user='root',password='123456',host='127.0.0.1',port=3306,database='travel',charset='utf8')
cur=db.cursor()
sql='insert into customized_cityinfo (city_obj,view_address,view_score,view_price,view_name,view_img) values (%s,%s,%s,%s,%s,%s)'

for city in result:
    if city['view_price'] !='':
        view_price=int(city['view_price'].split('￥')[-1])
        print(view_price)
        ss=[city['view_city'], city['view_address'], city['view_score'], view_price, city['view_name'],city['view_img']]

        cur.execute(sql,ss)

    else:
        cur.execute(sql,[city['view_city'],city['view_address'],city['view_score'],0.0,city['view_name'],city['view_img']])

db.commit()




























