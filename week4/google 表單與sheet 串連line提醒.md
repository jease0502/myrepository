# google 表單與sheet 串連line提醒

## 簡介

當表單每次有人填寫時，我們很少有辦法作到即時回覆或是常常忘記去看與整理，有了這個，你便可以隨時隨地的接到通知，當有人填寫好表單的時候，就會知道有人填寫好了，有沒有覺的這種隨時隨地都被提醒要工作的感覺很棒呢？:smiling_imp: :broken_heart: 


## line notify

首先要先去聲請[```line notify ```](https://notify-bot.line.me/zh_TW/)，進去之後會進入都入頁面，然後點選自己的名子
![](https://i.imgur.com/rjrwX3j.png)

然後選擇個人頁面

![](https://i.imgur.com/a8103TM.png)

進去之後點選下方的發行權杖

![](https://i.imgur.com/AVrxWFV.png)

接下來選擇你要傳送訊息的群組，填入權杖名稱，權杖名稱也就是你到時候要顯示在訊息上最上方的名稱。接下來按下發行。

![](https://i.imgur.com/RQmg3jO.png)

按下的時候，它會給你一組序號，記住這組帳號只會出現過一次，如果你沒有記得，你就GG了...

![](https://i.imgur.com/cn0lCvl.png)

當然你也可以把它給解除在重新用一次～


## Google表單與sheet串連

在我們擁有了這組號碼之後，我們就可以開始寫sheet 的巨集了，首先打開你的sheet，然後工具，選擇指令碼編輯器。

![](https://i.imgur.com/PPQiwIY.png)

接下來，將以下的程式碼填入，首先我們剛在申請 line notify的時候有拿到一組亂碼，我們要把它填入<b>token</b>的位置。message則是將你要傳達的訊息給打在裡面，如果要去讀取他表格內容可以用``` e.values[1]```去將我們要呼叫的表格位置填入在values裡面，記得他是從0開始進行表格命名的。

而```sendLineNotify```這個函式是不需要進行調整的，這個函式是用來與line api 進行串連的，所以基本上我們是不會去更改到他的。

```javascript=
function myFunction(e) { 
var token = "填入剛剛拿到的號碼"; 
var spreadSheet = SpreadsheetApp.getActive(); 

var message = "\n日期: " + e.values[1] + "\n摘要： " + e.values[3] ; 
sendLineNotify(message, token); 
} 

function sendLineNotify(message, token){ 
var options = 
{ 
"method" : "post", 
"payload" : {"message" : message}, 
"headers" : {"Authorization" : "Bearer " + token} 
}; 
UrlFetchApp.fetch("https://notify-api.line.me/api/notify", options); 
}


```

當我們更改好程式之後，要去設定我們的提醒時間這時候需要按下一個很像時鐘的按鈕。

![](https://i.imgur.com/2P9csPE.png)

然後你會跳到另外一個頁面當中，這時你會發現它空空如也正等待著你去填充它，這時候我們要去按下新增觸發條件，而填寫方式如下圖。

![](https://i.imgur.com/bii2tZV.png)

首先錯誤通知設定就看個人吧，你想馬上收到就設定成即時通知吧～選取活動範圍這邊，當然也有其他的選擇可以去使用，而本次的目的是為了讓表單更新時，我們便會即時收到的通知，所以我在設定的時候，選擇了當提交表單時，它會立刻發出訊通知。

然後按下儲存後，它會先去過問你要不要給它權限，這邊就按下允許就可以了。接下來你就可以去測試你的程式是否成功了～

p.s 記得把line Notify 加到你要發送的群組裡面喔～

## 成果

![](https://i.imgur.com/Es5p2CN.png)
