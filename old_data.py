from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from settings import DATABASE_PASSWORD
from datetime import date, datetime
import pandas as pd

# Handling DF
data = pd.read_csv('historical_fuel_data.csv')
df = pd.DataFrame(data)

old_data = df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')


def barrel_to_litre(barrel_price):
    per_liter = barrel_price / 158.987
    return per_liter


def total_cost_of_flight(fuel):
    fuel_expenditure = 4 * (fuel * 2508)
    return fuel_expenditure


def difference_calculator(oil_cost, kerosene_cost):
    if oil_cost.any() > kerosene_cost:
        difference = oil_cost.any() - kerosene_cost
        return difference
    elif kerosene_cost > oil_cost.any():
        difference = kerosene_cost - oil_cost.any()
        return difference


oil_barrel_value = df['jet_fuel_price_per_barrel']

kerosene_price_per_litre = 1.775

oil_price_per_litre = round(barrel_to_litre(oil_barrel_value), 3)

date_extracted = old_data

jet_fuel_total_cost = round(total_cost_of_flight(oil_price_per_litre), 1)

kerosene_total_cost = total_cost_of_flight(kerosene_price_per_litre)

difference = round(difference_calculator(jet_fuel_total_cost, kerosene_total_cost), 1)

print(df)

# try:
#     connection = mysql.connector.connect(
#         host='localhost',
#         database='jet_fuel',
#         user='root',
#         password=f'{DATABASE_PASSWORD}'
#     )
#
#     cursor = connection.cursor()
#
#     insert_query = """INSERT INTO fuel_prices (
#     date, solar_kerosene_price, jet_fuel_price, total_cost_jet_fuel, total_cost_solar_kerosene, difference
#     )
#     VALUES (%s, %s, %s, %s, %s, %s)"""
#     for i, row in enumerate(df.itertuples(), 1):
#         print(row)
#         cursor.execute(
#             """INSERT INTO fuel_prices (
#                     date, solar_kerosene_price, jet_fuel_price,
#                     total_cost_jet_fuel, total_cost_solar_kerosene, difference
#                     )
#                 VALUES (%s, %s, %s, %s, %s, %s)""",
#             (
#                 date_extracted,
#                 kerosene_price_per_litre,
#                 oil_price_per_litre,
#                 jet_fuel_total_cost,
#                 kerosene_total_cost,
#                 difference
#             )
#         )
#     connection.commit()
#     print('Record inserted succesfully')
#
# except mysql.connector.Error as error:
#     print('Failed to insert into MySQL table {}'.format(error))
#
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print('MySQL Connection is closed.')
