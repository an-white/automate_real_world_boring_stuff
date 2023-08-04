import json
import os
import time

from dotenv import load_dotenv


def build_json(company, company_id):
    # orders file must have the next structure

    """ orders_compony.md
    NUMORDEN1 IDCLIENTE1 FECHAEMISION1
    NUMORDEN2 IDCLIENTE2 FECHAEMISION2
    """

    # this structure is the easy way to build all the orders in the JSON
    try:
        orders_file = open(f'orders_{company}.md', 'r')
    except FileNotFoundError:
        return print(f'file not found for company: {company}')

    list_orders = orders_file.readlines()

    new_json = {"Records": []}

    total_items = len(list_orders)

    if total_items != 0:
        for line in list_orders:
            num_order, id_customer, order_date = line.split(' ')
            record = {
                "body": """{ \"Message\" : \"{\\\"CASA\\\":""" +
                        str(company_id) +
                        """,\\\"schema\\\":\\\"""" + company +
                        """\\\",\\\"data\\\":{""" +
                        """\\\"NUMORDEN\\\":\\\"""" + num_order +
                        """\\\",\\\"IDCLIENTE\\\":\\\"""" + id_customer.strip() +
                        """\\\",\\\"FECHAEMISION\\\":\\\"""" + order_date.strip() + """\\\"}}\"}"""
            }
            new_json["Records"].append(record)

        new_file = open(f'send_orders_{company}_{int(time.time())}.json', 'w')

        new_file.write(json.dumps(new_json))

    print(f'total orders in {company}: {total_items}')


if __name__ == '__main__':
    load_dotenv()
    companies = int(os.environ['COMPANIES'])

    for company_i_id in range(companies):
        company_i = os.environ[f'COMPANY_{company_i_id}']

        build_json(company_i, company_i_id)
