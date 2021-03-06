from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import Error
from settings import DATABASE_PASSWORD
from datetime import date

url = 'https://www.iata.org/en/publications/economics/fuel-monitor/'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

price_div_container = soup.find_all('div', {"class": "rich-text"})[1]

price_sentence = price_div_container.findChild('p', recursive=False)


def barrel_to_litre(barrel_price):
    per_liter = barrel_price / 158.987
    return per_liter


def total_cost_of_flight(fuel):
    fuel_expenditure = 4 * (fuel * 2508)
    return fuel_expenditure


def difference_calculator(oil_cost, kerosene_cost):
    if oil_cost > kerosene_cost:
        difference = oil_cost - kerosene_cost
        return difference
    elif kerosene_cost > oil_cost:
        difference = kerosene_cost - oil_cost
        return difference


oil_barrel_value = float(str(price_sentence).partition('$')[2][:5])

date_extracted = date.today()

oil_price_per_litre = round(barrel_to_litre(oil_barrel_value), 3)

kerosene_price_per_litre = 1.775

jet_fuel_total_cost = round(total_cost_of_flight(oil_price_per_litre), 1)

kerosene_total_cost = total_cost_of_flight(kerosene_price_per_litre)

difference = round(difference_calculator(jet_fuel_total_cost, kerosene_total_cost), 1)

print(oil_barrel_value, oil_price_per_litre, jet_fuel_total_cost, kerosene_total_cost, difference, oil_barrel_value)


# DB Connection:
def insert_variable_into_table(date, solar_kerosene_price, jet_fuel_price,
                               total_cost_jet_fuel, total_cost_solar_kerosene, difference, barrel_price):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='jet_fuel',
            user='root',
            password=f'{DATABASE_PASSWORD}'
        )

        cursor = connection.cursor()

        insert_query = """INSERT INTO fuel_prices (
        date, solar_kerosene_price, jet_fuel_price, total_cost_jet_fuel, total_cost_solar_kerosene, difference, jet_fuel_barrel_price
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        record = (date, solar_kerosene_price, jet_fuel_price,
                  total_cost_jet_fuel, total_cost_solar_kerosene, difference, barrel_price)
        cursor.execute(insert_query, record)
        connection.commit()
        print('Record inserted succesfully')

    except mysql.connector.Error as error:
        print('Failed to insert into MySQL table {}'.format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('MySQL Connection is closed.')


insert_variable_into_table(date_extracted, kerosene_price_per_litre, oil_price_per_litre, jet_fuel_total_cost,
                           kerosene_total_cost, difference, oil_barrel_value)
