import requests
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from torch import le


def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)


def download_parallel(args):
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap_unordered(download_url, args)
    for result in results:
        print('url:', result[0], 'time (s):', result[1])


if __name__ == "__main__":
    urls = ['https://etherscan.io/exportData?type=address&a=0xfd2487cc0e5dce97f08be1bc8ef1dce8d5988b4d',
            'https://etherscan.io/exportData?type=address&a=0xfd2487cc0e5dce97f08be1bc8ef1dce8d5988b4d',
            'https://etherscan.io/exportData?type=address&a=0xfd2487cc0e5dce97f08be1bc8ef1dce8d5988b4d',
            'https://etherscan.io/exportData?type=address&a=0xfd2487cc0e5dce97f08be1bc8ef1dce8d5988b4d']

    fns = ["./data/ponzi_or_not/ponzi_data_{}.csv".format(i+1)
           for i in range(len(urls))]
    inputs = zip(urls, fns)
    target_dir = "./data/ponzi_or_not"
    download_parallel(urls)
