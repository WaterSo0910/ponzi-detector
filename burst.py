import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
CONTRACT_ADDR = "0x7011f3edc7fa43c81440f9f43a6458174113b162"
OUTPUT_DIR = "./image/burst/"


def get_tx(contract_address, internal: bool):
    if internal == False:
        path = f"./data/burst/Tx_external/{contract_address}.csv"
    else:
        path = f"./data/burst/Tx_internal/{contract_address}.csv"

    df = pd.read_csv(path)
    df = df.filter(
        ['timeStamp', 'hash', 'from', 'to', 'value', 'isError'])
    df.value = df.value.astype(float)
    df = df[((~df["to"].isna()) & (~df["from"].isna())) & (df["to"] == CONTRACT_ADDR) | (
        df["from"] == CONTRACT_ADDR) & (df.isError == 0)]
    return df


def merge_tx(df_int, df_ext):
    df_merge = pd.concat([df_int, df_ext], axis=0)
    df_merge.loc[df_merge["from"] ==
                 CONTRACT_ADDR, ["value"]] = -1*df_merge.loc[df_merge["from"] ==
                                                             CONTRACT_ADDR, ["value"]]
    df_merge = df_merge.sort_values(by=["timeStamp"])
    return df_merge


def get_burst_stats(df_merge):
    df_burst = df_merge.filter(["timeStamp", "value"]).groupby(
        'timeStamp').sum().reset_index()
    df_burst["cum_value"] = df_burst['value'].cumsum(axis=0)
    return df_burst


def visualize_burst(df_burst):
    fig, ax = plt.subplots(figsize=(16, 4))
    sns.lineplot(ax=ax, data=df_burst, x="timeStamp", y="cum_value")
    fig.savefig(f"{OUTPUT_DIR}burst.png")


def get_user_profit_stats(df_merge):
    df_pay = df_merge.groupby("from").sum().reset_index().rename(
        columns={"from": "address", "value": "pay"})
    df_paid = df_merge.groupby("to").sum().reset_index().rename(
        columns={"to": "address", "value": "paid"})

    df_addr = pd.concat([df_pay, df_paid], axis=0).drop(
        columns=["timeStamp", "isError"])

    df_addr = df_addr.groupby("address").sum().reset_index().fillna(0)

    df_addr["p/e"] = (-1*df_addr["paid"])/df_addr["pay"]
    df_addr["profit"] = -1*(df_addr["pay"]+df_addr["paid"])
    return df_addr


def visualize_user_profit_stats(df_addr):
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.histplot(ax=ax, data=df_addr, x="p/e", binwidth=0.1)
    fig.savefig(f"{OUTPUT_DIR}pe_hist.png")
    # df_addr[np.isinf(df_addr["p/e"])]
    df_pyramid = df_addr.groupby('p/e').count().reset_index()
    df_pyramid = df_pyramid.rename(columns={
        "address": "count",
        "pay": "count1"
    })
    df_pyramid = df_pyramid.filter(["p/e", "count", "count1"])
    df_pyramid["p/e"] = round(df_pyramid["p/e"], 1)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns_plot = sns.barplot(ax=ax, data=df_pyramid, x='count',
                           y='p/e', orient='horizontal', ci=None)
    fig = sns_plot.get_figure()
    fig.savefig(f"{OUTPUT_DIR}pe_count.png")
    df_pyramid["count1"] = df_pyramid["count1"]*-1

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_plot = sns.barplot(ax=ax, x='count', y='p/e', data=df_pyramid,
                           lw=0, orient='horizontal', ci=None)
    bar_plot = sns.barplot(ax=ax, x='count1', y='p/e', data=df_pyramid,
                           lw=0, orient='horizontal', ci=None)
    plt.savefig(f"{OUTPUT_DIR}pe_pyramid.png")


if __name__ == '__main__':
    # Get internal and external Tx
    df_ext = get_tx(contract_address=CONTRACT_ADDR, internal=False)
    df_int = get_tx(contract_address=CONTRACT_ADDR, internal=True)
    df_merge = merge_tx(df_int, df_ext)
    # Time-series burst
    df_burst = get_burst_stats(df_merge)
    visualize_burst(df_burst)
    # User profits stats
    df_addr = get_user_profit_stats(df_merge)
    visualize_user_profit_stats(df_addr)
