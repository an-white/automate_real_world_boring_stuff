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


def build_json(company, sheet_id):
    load_dotenv()
    df = get_sheet(sheet_id)

    orders_df = pd.DataFrame({
        'NUMORDEN': df["PEDIDO"].str[-5:],
        'CLIENTE': df["CLIENTE"],
        'FECHAEMISION': df["FECHA_HORA"].str.slice(stop=10)
    })

    del df

    new_json = {"Records": []}

    total_items = len(orders_df)

    if total_items != 0:
        for i in range(total_items):
            record = {
                "body": """{ \"Message\" : \"{\\\"CASA\\\":0,\\\"schema\\\":\\\"""" + company +
                        """\\\",\\\"data\\\":{""" +
                        """\\\"NUMORDEN\\\":\\\"""" + str(orders_df.NUMORDEN[i]) +
                        """\\\",\\\"IDCLIENTE\\\":\\\"""" + str(orders_df.CLIENTE[i]) +
                        """\\\",\\\"FECHAEMISION\\\":\\\"""" + orders_df.FECHAEMISION[i] + """\\\"}}\"}"""
            }
            new_json["Records"].append(record)

        new_file = open(f'send_orders_{company}_{int(time.time())}.json', 'w')

        new_file.write(json.dumps(new_json))

    print(f'total orders in {company}: {total_items}')


if __name__ == '__main__':
    load_dotenv()
    companies = int(os.environ['COMPANIES'])

    for i in range(companies):
        company_i = os.environ[f'COMPANY_{i}']
        sheet_id_i = os.environ[f'SHEET_ID_COMPANY_{i}']

        build_json(company_i, sheet_id_i)
