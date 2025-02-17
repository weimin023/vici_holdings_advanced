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
第四個**rolling one-second time window**以第四筆訂單為起始點，演示了有訂單剛好在window boundary的情況。\
由於window已定義為**左閉右開**，最後一筆剛好在boundary的訂單屬於下一個區間。\
![image](https://github.com/weimin023/vici_holdings_advanced/blob/main/vici4.drawio.png)

### 解法:
1. **sliding window**的問題會想到以**queue**來解。
2. timestamp轉換為ns。計算訂單時間差需要考慮timestamp跨日問題，假設有兩筆訂單:
   ```
   "000011 23:59:59.500000000 [ORDER] OrderID:BAB|Side:Sell|Price:3.69|Lots:1",
   "000012 00:00:00.200000000 [ORDER] OrderID:BAC|Side:Buy|Price:3.68|Lots:1",
   ```
   如果轉為ns後直接計算時間差會變為負值，故要用一個變數紀錄是否跨日。
4. 主程式由三個function組成，使用unittest framework。
   - `detect_throttle_violations`:主要函式，接受line of log，並紀錄violation orders。
   - `parse_timestamp`:檢查timestamp format是否違規。
   - `time_to_nanoseconds`:將string type timestamp轉為ns。
### 測試
  - case 1: 空輸入
  - case 2: 有一筆violation
  - case 3: timestamp有跨日
  - case 4: 輸入log格式不正確
### 執行
```
python3 Q1.py
```
會測試共計6種test cases。對於log中的非法輸入將會在terminal raise exception。\
每個test case的invalid order將會被存在變數**violations_log**中，可自行印出。

## Q2: Mean Value
1. 使用 Kahan 求和補償算法(Kahan Summation Algorithm)來計算輸入數列的均值，以減少浮點數加法的累積誤差。
2. 使用template function，允許輸入 std::vector<T>，T可以是任一數值類型。
### 測試
1. 透過`pyblind`將C++函式導出，並在python環境調用。
2. 將`numpy`算出的mean作為ground truth，與C++實作的函式結果直接比較。誤差小於1e9則可驗證C++函式答案正確。
### 執行
1. 先build C++ mean function
```
mkdir build
cd build
cmake ..
make -j20
```
2. 執行python test script
```
python3 Q2.py
```
測試涵蓋了:
1. 幾種variable type的極值(int32, uint32, int64, uint64)出現overflow時會不會爆掉。
2. 資料量很大的情況
3. 同時有正負值的情況
