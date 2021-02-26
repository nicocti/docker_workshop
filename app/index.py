import os
import time
import argparse
from typing import Iterable, List

import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def get_domains(
    keywords: List[str], api: str = "https://api.domainsdb.info/v1/domains/search"
) -> Iterable[dict]:
    for keyword in keywords:
        params = {"domain": keyword}
        response = requests.request("GET", api, params=params)
        response.raise_for_status()
        for domain in response.json()["domains"]:
            yield {
                "_source": domain,
                "_index": "domains"
            }


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("domains", nargs="*")
    args = parser.parse_args()

    es: Elasticsearch = Elasticsearch(
        hosts=os.getenv("ES_HOST", "localhost"),
        port=os.getenv("ES_PORT", "9200"),
        ca_certs="/etc/ssl/certs/ca-certificates.crt",
    )

    while not es.ping():
        time.sleep(10)

    bulk(es, get_domains(keywords=args.domains))
