# vici_holdings_advanced

## Q1: Throttle Limit
對於題目中這句話的意思沒有十分肯定 "The throttle limit is defined as a maximum of 4 orders within **any rolling one-second time window**."\
我的理解如下圖:
![image](https://github.com/weimin023/vici_holdings_advanced/blob/main/vici.drawio.png)

從開始讀取log input後開始計算1s區間，每個區間為**左閉右開**。
### 舉例:
第一個**rolling one-second time window**內有6筆訂單，故後面兩筆為violations。
第二個**rolling one-second time window**以第二筆訂單為起始點
