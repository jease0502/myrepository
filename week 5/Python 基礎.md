# Python 基礎
###### tags: `python` `hackersir`



[TOC]

---

# Python 簡介

----

2019 7 月程式語言流行排行榜

![](https://i.imgur.com/tOpHPc1.png =700x500)


---

## 應用

----

![](https://i.imgur.com/CrAJNZs.png =700x500)


---


## 特點

----

+ 程式碼簡潔明瞭
+ 可以應用於不同領域(物理、生物、...)

---

## 體驗

----

在開始交程式前，先來看點漂亮的星星吧～

----

將下面程式碼複製到Colab執行

```python=
for a in range(0,20):
  print((20-a)*' ','*'*(2*a+1))
```

----

接下來你就會看到美麗的星星樹了～

![](https://i.imgur.com/IlMbUrQ.png)



---


# 程式教學

---

## 變數

----

變數就像是箱子

他有很多種類的箱子

每個箱子它都只能夠裝下特定種類的物品。

----

在python裡面有整數、浮點數、字串等種類的箱子

至於每個箱子能裝什麼我們下面會說。

----

我們通常會去幫變數取一個名字

讓我們比較好去使喚它

而這些名字有著一定的規則限制著他們

---


## 寫法設定

----

### 縮排

----

在python中縮排非常重要

你一不小心沒有縮排或是縮排錯了

你的程式就不能執行了

而python 中常用的兩種縮排

分別是`tab`或是4格空白

**不要混著用會出事**


----


### 多條語句

----

如果想將全部程式碼都寫在一起時

可以用 <font color="green">**分號**`;` </font>來將每段程式碼隔開

這樣子的用法便叫做多條語句

----

#### 實做

----

```python=
a = 1; b = 2; c = 3
```


----

### 多行語句

----

當你的程式碼很長的時候

你又不想要都擠在一行

可以用反斜線`\`來區隔

但是當遇到有括號把他們包在一起的情況

就不需要分號了

----

#### 實做

----

```python=
a = '1' +\
    '2' +\
    '3'

b = [1, 2, 3,
    4, 5, 6]
```


----

### 註解

----

當我們需要在程式旁邊打上一些附註

以面別人看不懂你的程式碼時

就需要用到註解的功能

----

註解分成兩種
+ 單行註解
    + 井字號`#`
+ 多行註解
    + 三個單引號`'''`或三個雙引號`"""`


----

實做

----

```python=
a = 1

#我的第一單行註解

'''
山支大哥好帥
'''

"""
宣儀好正～
"""
```

---

## 型態

----

在前面我們有提到在python裡面有

整數、浮點數、字串等種類的箱子

而整數、浮點數、字串又被稱作<font color="red"><b>型態</b></font>


----

當然python裡面有很多種型態

----


+ Python內建的型態
    + 數字
        + int (整數)
        + float (浮點數)（小數）
        + complex(複數)
    + str (字串)
    + List(列表)
    + Tuple(元组)
    + Dictionary(字典)
    + bool (布林值)
        + 只有`True`跟`False`

----

在開始講解型態前

先介紹一個函式

```type(變數)```

利用這個變數可以查看當前變數型態

----

### 數字

----

在數學中，有分整數、小數、複數

在程式裡面也是一樣的

----

在python裡面複數 `a + bj`可以用下面方法來表示

```python
complex(a,b)
```

----

#### 實做：

----

```python=
#int
a = 100
print(a)

#float
b = 123.456
print(b)
```

----

```python=
#complex
c = 2+4j
d = complex(5,6)
print(c)
print(d)
```

----

### str(字串)

----

各種文字都是字串

宣告字串可以用單引號(`'`)或雙引號(`"`)

這兩種打法都是一樣的功能

<font color=red>注意：</font>**字串的內容一旦定義好後，就不能被修改**

----


字串的基本語法如下

```python
變數名稱 = "文字"
變數名稱 = '文字'
```

----

在字串方面，每一個單字都佔有著一個位置

所以我們可以把一個一個單字挑出來召喚

而在召喚時又有幾種方法

----

#### 順序取值

----

在講解前先科普一下知識

----

在程式中，我們在計算變數位置時都是從0開始的

舉例來說，有一個人的名字叫做"苞娜"

<font color=gree>苞</font>所存放的空間（記憶體）位於這個變數之中<font color=red>0</font>的位置當中

<font color=gree>娜</font>也就是在<font color=red>1</font>的位置

----

而0、1這兩個數字便是索引

像是每一本書都會有著他的索引，以來幫助讀者更輕鬆的去查找資料

這些索引，所應對到的頁數，便是讀者所需要的內容（變數）

----

python 字串有兩種取值順序(排序順序）
+ 從左到右順序（索引）從0開始
+ 從右到左順序（索引）從-1開始

| 字串 | a | s | d | f |
| --- | --- | --- | --- | --- |
| 從頭到尾  | 0 | 1 | 2 | 3 |
| 從尾到頭  | -4 | -3 | -2 | -1 |

----

那我們又該如何去實現呢？

----

在python中要去取第幾個字元可以用這個方法

```python
變數[上索引:下索引+1]
```
在程式裡面在指定範圍時，常是不包括<font color=red>最後位置數</font>

所以在下索引的地方必須加1來讓你包刮到你想印出的字串

----

#### 舉例

----

```python=
>>> 變數 = '我是字串'
>>> 變數[0:] #從0位置開始
'我是字串'
>>> 變數[0:4] #從0到位置3
'我是字串'
>>> 變數[0:3] #從0到位置2
'我是字'
>>> 變數[-1] #最後一個字
'串'
>>> 變數[-4:-1] #從-4到-2
'我是字'
>>> 變數[-4:] #從位置-4開始
'我是字串'
```

----

python的字串可以用

+ `+` 來連接
+ `*` 來將原字串倍數增加（只能是整數）

----

#### 實做

----

```python=
s = 'asdfghjkl'
a = "qwe"

print('型態:', type(s))
print('型態:', type(a))
print(s[3])
print(s[-3])
print(s[0:5])
print(s[-4:-1])
print(s+a)
print(a*3)
```

----

### list(列表)

----

我們可以把列表當作集裝箱

在一開始我們把變數當成箱子

而列表的功用就是可以把他們都裝起來

----

列表的基本語法
```
變數=[東西1,東西2]
```

----

當我們把東西丟進去之後

又該如何取出？

----

他的用法跟剛才的字串一樣

列表一樣有兩種取法順序

- 從左到右從0開始
- 從右到左從-1開始

----

用法：
```
便是[上界：下界]
```

列表一樣可以用
+ `+` 來連接
+ `*` 來重複操作

----

實做

----

```python=
>>> x=123
>>> y='hackersir'
>>> list1=[x,y,"e"]
>>> list2=[y,x,"e"]
>>> list3=list1+list2
>>> list3
[123, 'hackersir', 'e', 'hackersir', 123, 'e']
```

----

現在來介紹一些列表一些用法

----

+ 添加列表
    + `list.append(要加的元素)`
        + 加在句尾
        + 一次只能加一個單位
    + `list.extend(要加的串列)`
        + 從最後面開始加
        + 一次可以加入全部元素
    + `list.insert(要插入的位置(index), 插入的元素)`

----

實做

----

```python=
>>> x=123
>>> y='hackersir'
>>> list1=[x,y,"e"]
>>> list2=[y,x,"e"]

>>> list1.append(list2)
>>> list1
[123, 'hackersir', 'e', ['hackersir', 123, 'e']]

>>> list1=[x,y,"e"]
>>> list1.extend(list2)
>>> list1
[123, 'hackersir', 'e', 'hackersir', 123, 'e']

>>> list4=["0","1","2"]
>>> list4
['0', '1', '2']
>>> list4.insert(0,"111")
>>> list4
['111', '0', '1', '2']
```

----

+ 刪除列表元素
    + `del`
        + `del list[index]`
            + 刪掉某一項
        + `del list`
            + 整個刪掉
    + `list.pop(index)`
        + 如果index不填的話會刪掉最後一項
    + `list.remove(要刪的元素)`

----

實做

----

```python=
>>> list1=["h","a","c","k","e","r","s","i","r"]

>>> del list1[0]
>>> list1
['a', 'c', 'k', 'e', 'r', 's', 'i', 'r']

>>> del list1
>>> list1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'list1' is not defined


>>> list1.pop()
'r'
>>> list1
['h', 'a', 'c', 'k', 'e', 'r', 's', 'i']

>>> list1.remove("c")
>>> list1
['h', 'a', 'k', 'e', 'r', 's', 'i', 'r']
```

----

+ 排序
    + `list.sort(key=None, reverse=False)`
        + `reverse = True`
            + 由大排到小
        + `reverse = False`
            + 由小排到大
        + `key`
            + 用來進行比較的元素

----

實做

----

```python=
>>> list2=[1,20,512,41,589,510,41,7]
>>> list2.sort(key=None,reverse=False)
>>> list2
[1, 7, 20, 41, 41, 510, 512, 589]
```

----

+ 反轉
    + `list.reverse()`
        + `()`裡不用填東西
+ 用元素找index
    + `list.index(要找的元素)`
+ 計算元素出現幾次
    + `list.count(你要計算的元素)`

----

實做

----

```python=
>>> list2=[1, 7, 20, 41, 41, 510, 512, 589]
>>> list2.reverse()
>>> list2
[589, 512, 510, 41, 41, 20, 7, 1]
>>> list2.index(7)
6
>>> list2.count(41)
2
```

----

### Tuple

----

元組其實就跟列表一樣

唯一的差別就是

元組在**宣告完後就不能改**了

----

元組基本語法

```python
變數 = (東西1, 東西2, ...)
```

----

元組中只包含一個元素時，需要在元素後面加逗號(`,`)

```python
tup = (50,)
```

----

元組不能刪裡面的元素

要刪只能整個刪除

但可以宣告一個新的元組，內容是兩個舊的原組加起來

----

元組操作跟剛剛的列表一樣

列表一樣有兩種取法順序

- 從左到右從0開始
- 從右到左從-1開始

----

如果要從元組裡面拿東西的話可以用

```python
變量[上界:下界]
```

原組一樣可以用
+ `+` 來連接
+ `*` 來重複操作
操作後產生一個新的元組

----

實做

----

```python=
>>> tup=(1,5,50)
>>> tup
(1, 5, 50)
>>> tup1=(2,)
>>> tup+tup1
(1, 5, 50, 2)
>>> tup*2
(1, 5, 50, 1, 5, 50)
```

---

### dic

----

python中的字典跟註釋一樣

每一個註釋只會有一個意思

----

字典基本語法

```python
變數 = {key1:value1, key2:value2, ...}
```

一個key只能出現一次

如果重複，最後一個key的value會代替前面的值

value可以重複沒關係

**key可以是字串、數字、元組，但不能是列表**

----

取字典裡面資料的方法

```python
dict[key]
```

**只能用key去取value**

所以要修改value時，只能用key去搜尋

----

刪除字典元素

+ `del`
    + `del dict[key]`
        + 刪掉某一組(key:value)
    + `del dict`
        + 整個刪掉

----

實做

----

```python=
>>> dic={'apple':1,'banana':2,'apple':3}
>>> dic
{'apple': 3, 'banana': 2}
>>> dic['apple']
3
>>> del dic['apple']
>>> dic
{'banana': 2}
>>> del dic
>>> dic
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'dic' is not defined

```

----

+ `dict.pop(key)`
    + 刪掉某一組(key:value)，回傳value
+ `dict.clear()`
    + 清空字典，字典還在，但是是空的
+ `dict.popitem()`
    + 隨機刪掉字典裡的一組key跟value，並回傳刪掉的key跟value

----

實做

----

```python=
>>> dic={'apple':1,'banana':2,'beef':3}
>>> dic.pop('apple')
1
>>> dic
{'banana': 2, 'beef': 3}
>>> dic.clear()
>>> dic
{}
>>> dic.popitem()
('beef', 3)
>>> dic
{'apple': 1, 'banana': 2}
```

---

### bool

----

在生活中有著對與錯，成立與不成立

程式中當然也有

布林就是所謂的對與錯，`True`跟`False`

----

實做：
```python=
f = True
print(f)
print('型態:', type(f)) #型態: <class 'bool'>

g = False
print(g)
print('型態:', type(g)) #型態: <class 'bool'>
```

---

## print

----

在程式當中，我們該如何去將資料顯示出來呢？

接下來就要開始講如何讓電腦吐出資料來

----

在python 中，當我們要去將資料吐出來

可以用```print``` 這個函式

在python兩個版本中使用方法是<font color=red>不同的</font>

----

基本的使用方法

Python3
```python
print('你好，世界')
```

Python2
```python
print '你好，世界'
```

----

print中階用法

```python
print(變數1, 變數2, ..., sep=分隔字元, end=結束字元)
```

+ 如果要輸出多個變數，在變數中間要加上`,`將他們分開
+ 在變數跟變數之間會有分隔字元把它分開，預設是用空白`" "`把他們分開
+ 在輸出完成之後，會加上一個字元，預設是換行`\n`



----

而分隔字元跟字元都是可以更改的

```python=
>>> 變數='變數'
>>> 變數2='變數2'
>>> print(變數,變數2,sep=' 拉拉拉 ',end=' 我是句尾 ')
變數 拉拉拉 變數2 我是句尾
```

----

當我們想要固定以一個穩定的模式去輸出
就可以使用 <font color=red>**print參數格式化**</font>


----

print參數格式化語法

```python
print(變數 % (參數列))
```

----

| 參數 | 說明 |
| --- | --- |
| `%d` | 整數 |
| `%f` | 浮點數 |
| `%s` | 字串 |
| `%c` | 字元 |
| `%u` | 無號整數 |
| `%o` | 八進位 |
| `%p` | 印記憶體 |

----

| 參數 | 說明 |
| --- | --- |
| `%e` | 科學記號(英文是小寫的) |
| `%E` | 科學記號(英文是大寫的) |
| `%x` | 十六進位(英文是小寫的) |
| `%X` | 十六進位(英文是大寫的) |
| `%g` | 就是 `%f` + `%e` |
| `%G` | 就是 `%f` + `%E` |

----

#### 實做

----

```python=
print(666, '小黑你好', '我很好')
print('右腳經濟', '左腳政治', '拉進來打出去', sep="", end="\n\n\n")

a = '我是字串'
b = 666
print("%s %d" % (a, b))
```

----

### 特殊字串

----

在python裡面有一些字串有著特殊的意義

我們需要用到**反斜線**`\`

來與一些字進行搭配

產生一些新的意思

----

那特殊字元又有哪些呢？

- 響鈴`\a`
- 退一格`b`
- 印出雙引號`\"`
- 印出單引號`\'`
- 印出反斜線‵\\`
- 空4格`\t`
- 換行`\n`



----

實做
```python=
s = '你是什麼樣的朋友呢？"我不是你朋友!!!"'
print(s)

#或是用反斜線
a = '你是什麼樣的朋友呢？ \'我不是你朋友!!!\''
print(a)
```

---


## input

----

在python中，如果我們需要將資料輸入到變數裡面

可以用input來讓使用者可以自行輸入資料

----

input基本語法

```python
變數名稱 = input('要顯示讓人家知道要輸入什麼')
```

----

實做：

```python=
x = input('輸入:')

print(x)
print(type(x))
```

---


## 型態轉換

----

剛剛有提到整數、浮點數、字串

都是型態的一種

那當我們想要去轉換型態時

要該怎麼做呢？

----

語法如下
```python
目標變數 = 目標型態（原本變數）
```

----

實做

```python=
# 先宣告一個整數
a=100
print(a)
print(type(a)) #查看型態

# 將整數轉為浮點數
b = float(a) 
print(b)
print(type(b))

# 宣告一個浮點數
c=123.56
print(c)
print(type(c))

# 將浮點數轉為整數
e=int(c)
print(e)
print(type(e))

# 將整數轉為字串
f=str(a)
print(f)
print(type(f))

# 將浮點數轉為字串
g=str(c)
print(g)
print(type(g))

# 將字串轉為整數
h = '123'
i=int(h)
print(i)
print(type(i))
```

---

## 運算式


----

運算式是什麼？

就是數學式子...

----

1+1 是一個運算式

2*2 還是一個運算式

`+` 、 `*`是運算子

運算子就是用來決定要做哪一種運算

`1`就是運算元

----

#### 算數運算子

----

| 運算子 | 意義 |
| --- | --- |
| `+` | 相加 |
| `-` | 相減 |
| `*` | 相乘 |
| `/` | 相除 |
| `%` | 取餘數 |
| `//` | 取商數 |
| `**` | 次方 |


----

除了數字之外

字串也是可以做運算

----

實做

```python=
a = 1+2
b = 3-1
c = 3*2
d = 5/3
e = 10%3
f = 7//2
g = 2**3

h = 'hello'
i = 'hackersir'

print(a, b, c, d, e, f, g, sep=' ^_^ ')

print(h+i)
print(h*10)
```

---


## 判斷式

----

### 關係運算子

----

在數學中，有著等於、小於、大於、不等於

等等的關係，這些便是<font color=red>**關係運算子**</font>

----

| 運算子 | 意義 |
| --- | --- |
| `==` | 等於 |
| `!=` | 不等於 |
| `>` | 大於 |
| `<` | 小於 |
| `>=` | 大於或等於 |
| `<=` | 小於或等於 |

----

實做

```python=
a = 1 == 2
b = 1 == 1

c = 1 != 2
d = 1 != 1

e = 1 > 2
f = 2 > 3

g = 1 < 2
h = 3 < 2

print(a, b, c, d, e, f, g, h)
```

```python
False True True False False False True False
```

----

### 邏輯運算子

----

排列組合中有提到not、and、or

而這些便是邏輯運算子

----

| 運算子 | 意義 |
| --- | --- |
| `not` | 相反 |
| `and` | 兩者為真才為真 |
| `or` | 其中一者為真即為真 |

----

實做
```python=
>>> a = 1 == 1
>>> print(a)
True
>>> print(not(a))
False
>>> 
>>> b = 1 == 2
>>> print(b)
False
>>> print(a and b)
False
>>> print(a and a)
True
>>> 
>>> print(a or b)
True
>>> print(b or b)
False
>>> print(a or a)
True

```

----


### 敘述判斷式

----

判斷式基本語法

```python
if (條件式一):
    條件式一成立，要做的事

elif (條件式二):
    條件式二成立，要做的事

else:
    上述條件式都不成立，要做的事
```

----

#### if

----

上述語法可以用流程圖來演示：

```flow
st=>start: Start
e=>end: End
op=>operation: 條件運算式
op2=>operation: 主體敘述
cond=>condition: 是或否？

st->op->cond->op2->e
cond(yes)->op2
cond(no)->e
```

----

#### 實做

----

```python=
a=16
b=4
if a>b:
    print("a>b")
>>> a>b
```

----

#### if else 

----

```flow
st=>start: Start
e=>end: End
op=>operation: 條件運算式
op2=>operation: 主體敘述1
op3=>operation: 主體敘述2
cond=>condition: 是或否？

st->op->cond->op2->e
cond(yes)->op2
cond(no)->op3->e
```

----

實做

----

```python=
a=20
b=10
if a>b:
    print("a>b")
else:
    print("a<b")
```

----

#### if elif else

----

```flow
st=>start: Start
e=>end: End
op=>operation: 條件運算式
op2=>operation: 主體敘述1
op3=>operation: 主體敘述2
op4=>operation: 主體敘述3
cond=>condition: 是或否？
cond1=>condition: 是或否？

st->op->cond->op2->e
cond(yes)->op2
cond(no)->op3->cond1->e
cond1(yes)->e
cond1(no)->op4->e
```

----

實做

----

```python=
a=30
b=20
c=10
if a<b:
    print("a<b")
elif a<c:
    print("a<c)
else :
    print("a>b,a>c")
>>>a>b,a>c
```

---


## 迴圈

----

+ python迴圈分兩種
    + while
    + for

----

#### while

----

```python=
初始值設定
while 條件運算式：
    迴圈主體敘述
    更新運算式
```


----

```flow
st=>start: Start
e=>end: End
op=>operation: 條件運算式
op2=>operation: 主體敘述1
op3=>operation: 主體敘述2
cond=>condition: 是或否？

st->op->cond->op2->e
cond(yes)->op2
cond(no)->op3->e
```

----

實做

----

```python=
i=0
while i<=3:
	print(i)
	i+=1
>>>0
>>>1
>>>2
>>>3
```

----

#### for

----

上述while迴圈的敘述也可以使用```for in range```來表示。其語法如下:
```python=
for i in range(start,end,step):
    迴圈主體敘述
```

----

```flow
st=>start: Start
e=>end: End
op=>operation: i-start
op2=>operation: 迴圈主體敘述
op3=>operation: 主體敘述2
cond=>condition: i<=end-1
op4=>operation: i+=step

st->op->cond->op2->op4->op
cond(yes)->op2
cond(no)->e
```

----

注意：
- for迴圈敘述後面要加上冒號


----

實做

----

```python=
for i in range(10,1,-1):
    print(i,end=" ")
>>>10 9 8 7 6 5 4 3 2
```
---


## 函式

----

在寫程式時，常常一不小心就會亂掉

那我們又該如何避免呢？

這是就可以用函數來把程式整理出來

----

基本語法
```python
def 函式名稱(要傳進去的東西):
    要做的事
    return 要吐出來的東西
```

----

+ 如果return後面沒接東西代表return None
+ 函式內的變數跟函式外的變數並不相同，就算名子一樣，也互相不會有影響

----

實做

```python=
def job(a):
    a+=100
    return a

b=100
c=job(b)
print(c)
>>>200
```