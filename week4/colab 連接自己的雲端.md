# colab 連接自己的雲端
###### tags: colab

## 簡介

在我們要利用colab去training 的時候，總是需要將資料給帶入近來，那我們又該寫我們的檔案路徑呢？這邊將紀錄一個直接跟雲端串連的方法。

## 實做

1. 首先在colab中輸入這行程式碼
```
from google.colab import drive
drive.mount('/content/drive')
```

2. 接下來它會出現這行程式碼
![](https://i.imgur.com/0O4UXfw.png)

3. 用力點下他的連結，你會看到它叫你連結帳號，然後你點選你要的帳號,然後按下允許

![](https://i.imgur.com/z7TXUCB.png)

4. 接下來你會得到一組密碼，也就是token，把它複製下來，貼到在colab中的那個框框裡面，然後執行下就好

5. 找到一個叫做My Drive的資料夾，這邊底下的資料夾便是你存放資料的地方

![](https://i.imgur.com/YMNKPeq.png)

6. 如果要複製路徑的話，直接對著目標檔案右鍵，即可複製地址