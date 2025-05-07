import pandas as pd
import numpy as np
import configparser
import os

def load_config(config_file='dgp_config.ini'):
    """Loads configuration parameters from an INI file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    dgp_params = {}
    states_list = []
    if 'dgp' in config:
        for key, value in config['dgp'].items():
            try:
                dgp_params[key] = float(value)
            except ValueError:
                if ',' in value:
                    dgp_params[key] = [v.strip() for v in value.split(',')]
                else:
                    dgp_params[key] = value
    if 'states' in config:
        states_list = [s.strip() for s in config['states'].get('list', '').split(',') if s.strip()]
    return dgp_params, states_list

def generate_base_dataframe(states, n_time_periods=52, start_date='2025-01-01'):
    """Generates the base DataFrame with State, Date, and Time index."""
    dates = pd.to_datetime([start_date] * n_time_periods) + pd.to_timedelta(np.arange(n_time_periods), unit='W')
    data_list = []
    for state in states:
        state_df = pd.DataFrame({'State': [state] * n_time_periods, 'Date': dates})
        data_list.append(state_df)
    data = pd.concat(data_list, ignore_index=True)
    data['Time'] = data.groupby('State').cumcount()
    return data

def generate_state_effects(dgp_params, states, seed=123):
    """Generates state-level variations for marketing effects."""
    np.random.seed(seed)
    state_effects = {}
    for state in states:
        state_effects[state] = {
            'tv': np.random.normal(dgp_params.get('true_tv_effect_base', 0.6), dgp_params.get('true_tv_effect_sd', 0.08)),
            'digital': np.random.normal(dgp_params.get('true_digital_effect_base', 0.9), dgp_params.get('true_digital_effect_sd', 0.12)),
            'radio': np.random.normal(dgp_params.get('true_radio_effect_base', 0.25), dgp_params.get('true_radio_effect_sd', 0.05)),
            'social': np.random.normal(dgp_params.get('true_social_effect_base', 0.7), dgp_params.get('true_social_effect_sd', 0.1)),
            'price': dgp_params.get('true_price_effect', -1.5)
        }
    return state_effects

def generate_marketing_spend(data):
    """Generates synthetic marketing spend data and applies log transformation."""
    data['TV_Spend'] = np.random.uniform(100, 1000, len(data))
    data['Digital_Spend'] = np.random.uniform(50, 500, len(data))
    data['Radio_Spend'] = np.random.uniform(20, 200, len(data))
    data['Social_Spend'] = np.random.uniform(80, 800, len(data))
    data[['TV_Spend_Log', 'Digital_Spend_Log', 'Radio_Spend_Log', 'Social_Spend_Log']] = np.log1p(data[['TV_Spend', 'Digital_Spend', 'Radio_Spend', 'Social_Spend']])
    return data

def generate_control_variables(data, dgp_params):
    """Generates synthetic control variable data."""
    data['Price'] = np.random.uniform(dgp_params.get('min_price', 10), dgp_params.get('max_price', 30), len(data))
    data['Seasonality'] = data.groupby('State')['Time'].transform(lambda t: dgp_params.get('seasonality_amplitude', 50) * np.sin(2 * np.pi * t / dgp_params.get('seasonality_period', 52)) + dgp_params.get('seasonality_baseline', 100))
    data['Economic_Index'] = np.random.normal(dgp_params.get('economic_index_mean', 100), dgp_params.get('economic_index_sd', 10), len(data))
    return data

def generate_sales(row, dgp_params, state_effects):
    """Generates synthetic sales data based on the defined DGP."""
    state = row['State']
    tv_spend = row['TV_Spend_Log']
    digital_spend = row['Digital_Spend_Log']
    radio_spend = row['Radio_Spend_Log']
    social_spend = row['Social_Spend_Log']
    price = row['Price']
    seasonality = row['Seasonality']
    economic_index = row['Economic_Index']

    sales = (dgp_params.get('true_base_intercept', 50) +
             state_effects[state]['tv'] * tv_spend +
             state_effects[state]['digital'] * digital_spend +
             state_effects[state]['radio'] * radio_spend +
             state_effects[state]['social'] * social_spend +
             dgp_params.get('true_price_effect', -1.5) * price +
             dgp_params.get('true_seasonality_effect', 0.4) * seasonality +
             dgp_params.get('true_economic_effect', 0.15) * (economic_index - dgp_params.get('economic_index_mean', 100)) +
             np.random.normal(0, dgp_params.get('true_error_sd', 8)))

    return max(0, sales)