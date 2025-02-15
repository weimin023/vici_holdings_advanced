# vici_holdings_advanced

## Q1: Throttle Limit
對於題目中這句話的意思沒有十分肯定 "The throttle limit is defined as a maximum of 4 orders within **any rolling one-second time window**."\
我的理解如下圖:
![image](https://github.com/weimin023/vici_holdings_advanced/blob/main/vici.drawio.png)

從開始讀取log input後開始計算1s區間，每個區間為**左閉右開**。
### 舉例:
第一個**rolling one-second time window**內有6筆訂單，故後面兩筆為violations。

第二個**rolling one-second time window**以第二筆訂單為起始點。中間兩筆訂單在前一個window就視為invalid了，故不考慮。
因為已有四筆valid訂單，最後一筆新訂單為**invalid**。
![image](https://github.com/weimin023/vici_holdings_advanced/blob/main/vici2.drawio.png)
第三個**rolling one-second time window**以第三筆訂單為起始點。思路延續上一個window，最後一筆新訂單為**valid**。\
![image](https://github.com/weimin023/vici_holdings_advanced/blob/main/vici3.drawio.png)
第四個**rolling one-second time window**以第四筆訂單為起始點。演示了有訂單剛好在window boundary的情況。\
由於window已定義為**左閉右開**，最後一筆剛好在boundary的訂單屬於下一個區間。\
![image](https://github.com/weimin023/vici_holdings_advanced/blob/main/vici4.drawio.png)
