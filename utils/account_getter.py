from audioop import add
import pandas as pd
import requests
from tqdm import tqdm

API_KEY = "Y7ZP1HMWF1HTTB6EMAUYZDFF8RKQTVJHTU"


def getPonzi(path):
    df = pd.read_csv(path)
    return df[df.IS_PONZI == 1]['addr'].tolist()


def get_etherscan_data(address_list, output_dir, action):
    assert action in ["txlist", "txlistinternal"], "must be these 2 actions"
    length_list = []
    for address in tqdm(address_list, desc="Loading data.."):
        reqUrl = f"https://api.etherscan.io/api?module=account&action={action}&address={address}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={API_KEY}"
        headersList = {
            "Accept": "*/*",
            "User-Agent": "Ponzi"
        }
        payload = ""
        response = requests.request(
            "GET", reqUrl, data=payload,  headers=headersList)
        data = response.json()
        df = pd.DataFrame.from_dict(data)
        df2 = pd.json_normalize(df['result'])
        length_list.append(len(df2))
        df2.to_csv(f"{output_dir}{address}.csv")
    all_df = pd.DataFrame(data={
        "address": address_list,
        "length": length_list
    })
    all_df.to_csv(f"{output_dir}all_ponzi.csv")


if __name__ == '__main__':
    address_list = getPonzi("./data/others/ponzi_list.csv")
    get_etherscan_data(address_list, action="txlistinternal",
                       output_dir="./data/burst/Tx_internal/")
