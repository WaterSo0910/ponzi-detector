# Burst detector

## Goal

- give a safe zone and dangerous zone for user (split by burst)
- make everybody know more deeply what is ponzi scheme

## Steps

1. Merge Tx_internal, Tx_external by contract
2. Order them by timestamp
3. Build a time-series dataset
   - init contract balance is 0
   - add External Tx value
   - substract Internal Tx value
4. Visualizaion (use visdom)
5. Modeling (use LSTM)
   - predict when would `burst` happened

## Problem

- What is our time series unit?

## Reference
[How to deal with irregular time series data](https://www.notion.so/Corrupt-sparse-irregular-and-ugly-Deep-learning-on-time-series-887b823df439417bb8428a3474d939b3)