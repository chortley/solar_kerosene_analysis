from settings import DATABASE_PASSWORD
import pandas as pd
from sqlalchemy import create_engine

data = pd.read_csv('historical_fuel_data.csv')
df = pd.DataFrame(data)


def barrel_to_litre(barrel_price):
    per_liter = barrel_price / 158.987
    return per_liter


def total_cost_of_flight(fuel):
    fuel_expenditure = 4 * (fuel * 2508)
    return fuel_expenditure


def difference_calculator(oil_cost, kerosene_cost):
    if oil_cost.any() > kerosene_cost:
        difference = oil_cost - kerosene_cost
        return difference
    elif kerosene_cost > oil_cost.any():
        difference = kerosene_cost - oil_cost
        return difference


oil_barrel_value = df['jet_fuel_barrel_price']

kerosene_price_per_litre = 1.775

oil_price_per_litre = round(barrel_to_litre(oil_barrel_value), 3)

date_extracted = df['date']

jet_fuel_total_cost = round(total_cost_of_flight(oil_price_per_litre), 1)

kerosene_total_cost = total_cost_of_flight(kerosene_price_per_litre)

difference = difference_calculator(jet_fuel_total_cost, kerosene_total_cost)

df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

df.date.dt.strftime('%d.%m.%Y')

df.insert(1, 'solar_kerosene_price', kerosene_price_per_litre)
df.insert(2, 'jet_fuel_price', oil_price_per_litre)
df.insert(3, 'total_cost_jet_fuel', jet_fuel_total_cost)
df.insert(4, 'total_cost_solar_kerosene', kerosene_total_cost)
df.insert(5, 'difference', difference)
pd.set_option('display.max_columns', None)

engine = create_engine(f'mysql+mysqlconnector://root:{DATABASE_PASSWORD}@localhost:3306/jet_fuel', echo=False)
df.to_sql(name='fuel_prices', con=engine, if_exists='append', index=False)
