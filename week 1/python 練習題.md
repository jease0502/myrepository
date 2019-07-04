# python 練習題
第一題題目:
輸入數字到green跟red，並寫一個判斷式，red之值是否大於green，如果是印出red大於green，不是，印出green大於red

x=eval(input())


第二題
設計一個叫做 Multiply 的函數，輸入兩個數到函式裡面進行乘，並把結果傳回主程式，並印出來


第一題
```python=
green = eval(input('你的green是多少?'))
red = eval(input('那red呢?'))
if(red > green):
    print('red大於green')
elif(green > red):
    print('green大於red')
else :
    print('green等於red')
```
第二題
```python=
x = eval(input('x=?'))
y = eval(input('y=?'))
def Multiply(x,y):
    c = x*y
    return c
print('x * y =',Multiply(x,y))
```

ftsjease0502@gmail.com