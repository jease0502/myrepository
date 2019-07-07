# google sheet 使用紀錄

## 前因

由於社團內的帳本實在太亂了，於是我便天馬行空地把google表單跟sheet結合再一起，然後做一些簡單的函示應用

## 建立表單

在GOOGLE SHEET中提供一個很簡單的表單串連方式。步驟如下

1. 開啟SHEET
2. 點選插入
3. 選擇表單

就三個步驟，編輯表單內容就不這裡寫了

## 涵式

在使用excel涵式時，前面都要多一個```=```才會進入涵是模式，這次使用到的韓式分別是```sum```、```IMPORTRANGE```、```IF (COUNTIF)```

### sum()

按照字面上的意思就是加總，使用方式是:
```
sum(值_1, [值_2, ...])
```
示範:
```
sum(H:H)
```
上面這行的意思是把所有在H行的數值進行加總

```
SUM(1,2,3,4,5)
```
上面這行則是將括號裡面的數值加總在一起也就是15

### IMPORTRANGE

它的用途在於將其他表單中的格子傳送到另外一個表單進行使用，使用方法:

```
=IMPORTRANGE("網址","區域")
```

成果展示

![](https://i.imgur.com/1WT1vXC.png)
￼

![](https://i.imgur.com/mGt4Yre.png)


### IF (COUNTIF)

這個涵式常用於在判斷三個變數時使用，他像是程式碼中的巢狀結構，也可以說是```if、else if (elif)、else```的綜合體，使用方法:

可以先拆開成if和countif來看

#### IF
```
IF(logical_expression, value_if_true, value_if_false)
```
在使用IF指令時切記他所回傳的答案是```TRUE```OR```FALSE```，所以在上述的語法中可看到，```logical_expression```適用來設定條件的，如果是對的就回傳在```value_if_true```這邊所給的回覆，如果是錯的則是回傳``` value_if_false```內的回覆，預設``` value_if_false```是空的，可寫可不寫。

示範
```
IF(A2 = "foo","A2 is foo")
```
如果A2=foo這個字串，則他會回傳A2 is foo這行文字


#### COUNTIF
```
COUNTIF(range, criterion)
```

在使用這個程式碼時，通常配合if來進行使用，以來輔助if在選取範圍時的無力，並且他所接收的值為0和1，也就是```TRUE```OR```FALSE```，故需要搭配if來進行使用。而他的語法也很直白，先給定一個範圍，再給出如果是正確的要回傳甚麼。

示範:

```
COUNTIF(A1:A10,">20")
```
從A1到A10，如果接收到的指令是TRUE則回傳>20回去

