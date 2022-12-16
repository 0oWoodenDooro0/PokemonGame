import json

import requests


class Pokebase:
    api_url = {
        'pokemon': 'https://pokeapi.co/api/v2/pokemon/',
        'pokemon-species': 'https://pokeapi.co/api/v2/pokemon-species/',
        'evolution-chain': 'https://pokeapi.co/api/v2/evolution-chain/',
        'growth-rate': 'https://pokeapi.co/api/v2/growth-rate/',
        'pal-park-area': 'https://pokeapi.co/api/v2/pal-park-area/',
        'region': 'https://pokeapi.co/api/v2/region/',
        'location': 'https://pokeapi.co/api/v2/location/',
        'location-area': 'https://pokeapi.co/api/v2/location-area/'
    }

    def __init__(self):
        pass

    @staticmethod
    def fetch_data(*, update: bool = False, json_cache: str, url: str):
        if update:
            json_data = None
        else:
            try:
                with open(json_cache, 'r') as file:
                    json_data = json.load(file)
                    # print('Fetched data from local cache!' )
            except(FileNotFoundError, json.JSONDecodeError) as e:
                print(f'No local cache found... {e}')
                json_data = None

        if not json_data:
            print('Fetching new json data... (Creating local cache)')
            json_data = requests.get(url).json()
            with open(json_cache, 'w') as file:
                json.dump(json_data, file)

        return json_data

    @classmethod
    def get_api(cls, api_name):
        next_url = cls.api_url[api_name]
        while True:
            json_data = requests.get(next_url).json()
            next_url = json_data['next']
            for result in json_data['results']:
                api_id = result['url'].split('/')[-2]
                cls.fetch_data(update=False,
                               json_cache=f'./{api_name}/{api_id}.json',
                               url=result['url']
                               )
            if next_url is None:
                break

    @classmethod
    def get_pokemon_api(cls):
        cls.get_api('pokemon')

    @classmethod
    def get_pokemon_species_api(cls):
        cls.get_api('pokemon-species')

    @classmethod
    def get_evolution_chain_api(cls):
        cls.get_api('evolution-chain')

    @classmethod
    def get_growth_rate_api(cls):
        cls.get_api('growth-rate')

    @classmethod
    def get_pal_park_areas_api(cls):
        cls.get_api('pal-park-area')

    @classmethod
    def get_encounters_api(cls):
        next_url = cls.api_url['pokemon']
        while True:
            json_data = requests.get(next_url).json()
            next_url = json_data['next']
            for result in json_data['results']:
                api_id = result['url'].split('/')[-2]
                cls.fetch_data(update=False,
                               json_cache=f'./encounters/{api_id}.json',
                               url=result['url'] + '/encounters'
                               )
            if next_url is None:
                break

    @classmethod
    def get_region_api(cls):
        cls.get_api('region')

    @classmethod
    def get_location_api(cls):
        cls.get_api('location')

    @classmethod
    def get_location_area_api(cls):
        cls.get_api('location-area')

    @classmethod
    def get_api_by_id(cls, api_name: str, api_id: int):
        json_data = cls.fetch_data(
            update=False,
            json_cache=f'./{api_name}/{api_id}.json',
            url=cls.api_url[api_name] + str(api_id)
        )
        return json_data


if __name__ == '__main__':
    Pokebase.get_location_area_api()
