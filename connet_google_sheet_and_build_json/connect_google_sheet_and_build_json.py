import json
import os
import time

import pandas as pd
from dotenv import load_dotenv

"""
get data from a google sheet doc, use this info to build a json
"""


def get_sheet(sheet_id):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv'
    return pd.read_csv(url)


def build_json():
    load_dotenv()
    sheet_id = os.environ['SHEET_ID']
    df = get_sheet(sheet_id)

    orders_df = pd.DataFrame({
        'NUMORDEN': df["PEDIDO"].str[-5:],
        'CLIENTE': df["CLIENTE"],
        'FECHAEMISION': df["FECHA_HORA"].str.slice(stop=10)
    })

    del df

    new_json = {"Records": []}

    for i in range(len(orders_df)):
        record = {
            "body": """{ \"Message\" : \"{\\\"CASA\\\":0,\\\"schema\\\":\\\"dbafv\\\",\\\"data\\\":{""" +
                    """\\\"NUMORDEN\\\":\\\"""" + str(orders_df.NUMORDEN[i]) +
                    """\\\",\\\"IDCLIENTE\\\":\\\"""" + str(orders_df.CLIENTE[i]) +
                    """\\\",\\\"FECHAEMISION\\\":\\\"""" + orders_df.FECHAEMISION[i] + """\\\"}}\"}"""
        }
        new_json["Records"].append(record)

    new_file = open(f'send_order_{int(time.time())}.json', 'w')

    new_file.write(json.dumps(new_json))

    print(f'total orders: {len(orders_df)}')


if __name__ == '__main__':
    build_json()
