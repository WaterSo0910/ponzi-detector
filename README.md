# ponzi-detector

## Goal

detect ponzi scheme on ethereum contracts

## Motivation

用戶可以將交易發送到以太坊網絡:

    - 創建新合約
    - 調用合約的功能
    - 將以太幣轉移給合約或其他用戶

所有交易都記錄在一個公共的數據結構——區塊鏈，在收到外部交易後，合約可以觸發一些內部交易，這些交易並未明確記錄在區塊鏈上，但仍會影響用戶和其他合約的餘額。由於交易可以轉移資金，因此確保正確執行交易至關重要。

## Analysis

- When to burst
  - Tx data of contracts
  
- Ponzi or not
  - stats
  - bytecode
    - settings of train/validate
    - preprocess logic
      - composition features
      - how to handle imbalanced data
    - methods
      - Random Forest
      - xgboost
      
      - NLP NN
    - Result
      - Importance of features  
      - Validation score

## Ponzi definition

![ponzi](https://ars.els-cdn.com/content/image/1-s2.0-S0167739X18301407-gr2_lrg.jpg)
