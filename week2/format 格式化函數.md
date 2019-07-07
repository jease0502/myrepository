---
tags: python
---

# format 格式化函數

他是一個很詭異的東西～它可以利用{}來代替％，它增強了字串格式化的功能。format 函數可以接受很多個參數，位置也不須按照順序。

```python=
" {} {} " . format ( " hello " , " world " )
 #不設置指定位置，按默認順序' hello world ' 
>>>  hello world
" {0} {1} " . format ( " hello " , " world " ) #設置指定位置' hello world ' 
>>> hello world '
" {1} {0} {1} " . format ( " hello " ," world " )    
#設置指定位置'
>>>  world hello world '
```

當然也可以設置參數啦～

第一種是最簡單的參數設定
```python=
print ( " 網站名：{name},地址{url} " . format ( name = " jeasenetwork" , url = " www.jease.com " ) ) 
#通過字典設置參數
```
第二種是採用列表的方式來進行
```python=
my_list = [ ' jeasenetwork' , 'www.jease.com ' ] 
print ( " 網站名：{0[0]},地址{0[1]} " . format ( my_list ) ) # "0"是必須的
```
第三種是用字典的方式來進行
```python=
a={'name':'jea'}
print ("網站:{name}").format(**a)   #python3
print " 網站:{name}".format(**a)    #python2
```


接下來是把數字給格式化
```python=
print ("{:格式}" . format (數字））
```
下面將列出所有打法～

輸入|格式|輸出|描述
--|--|--|--|
3.1415926|	{:.2f}	|3.14|保留小數點後兩位
3.1415926	|{:+.2f}	|+3.14	|帶符號保留小數點後兩位
-1	|{:+.2f}|	-1.00	|帶符號保留小數點後兩位
2.71828	|{:.0f}	|3	|不帶小數
5	|{:0>2d}	|05	|數字補零(填充左邊, 寬度為2)
5	|{:x<4d}	|5xxx|	數字補x (填充右邊, 寬度為4)
10	|{:x<4d}	|10xx	|數字補x (填充右邊, 寬度為4)
1000000|	{:,}	|1,000,000	|以逗號分隔的數字格式
0.25	|{:.2%}	|25.00%|	百分比格式
1000000000|	{:.2e}	|1.00e+09	|指數記法
13	|{:10d}	 |       13	|右對齊(默認, 寬度為10)
13|	{:<10d}	|13	|左對齊(寬度為10)
13	|{:^10d}	|    13	|中間對齊(寬度為10)