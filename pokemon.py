from __future__ import annotations

import math
import random

from pokebase import Pokebase as pb


class Pokemon:
    def __init__(
            self,
            pokemon_id: int = None,
            name: str = '',
            types: list = None,
            basic_stats: dict = None,
            individual_level: dict = None,
            effort_values: dict = None,
            level: int = 1,
            evolution_level: int = None,
            evolution_species_id: int = None,
            base_experience: int = 0,
            experience: int = 0,
            experience_chart: list = None,
            moves: dict = None
    ):
        self._pokemon_id: int = pokemon_id
        self._name: str = name
        self._types: list = types
        self._basic_stats: dict = basic_stats if basic_stats is not None else {}
        self._individual_level: dict = individual_level if individual_level is not None else {}
        self._effort_values: dict = effort_values if effort_values is not None else {}
        self._level: int = level
        self._evolution_level: int = evolution_level
        self._evolution_species_id: int = evolution_species_id
        self._stats: dict = self.get_stat()
        self._base_experience: int = base_experience
        self._experience: int = experience
        self._experience_chart: list = experience_chart if experience_chart is not None else []
        self._level_max_experience: int = self._experience_chart[self._level]['experience'] if self._level < 100 else None
        self._moves: dict = moves if moves is not None else {}

    @property
    def name(self):
        return self._name

    @staticmethod
    def get_individual_level() -> dict:
        return {
            'hp': random.randint(0, 31),
            'attack': random.randint(0, 31),
            'defense': random.randint(0, 31),
            'speed': random.randint(0, 31),
            'special-attack': random.randint(0, 31),
            'special-defense': random.randint(0, 31)
        }

    def get_stat(self) -> dict:
        return {
            'hp': self.get_hp(),
            'attack': self.get_other_ability('attack'),
            'defense': self.get_other_ability('defense'),
            'speed': self.get_other_ability('speed'),
            'special_attack': self.get_other_ability('special-attack'),
            'special_defense': self.get_other_ability('special-defense'),
        }

    def get_hp(self) -> int:
        return math.floor((self._basic_stats['hp'] * 2 + self._individual_level['hp'] + self._effort_values['hp'] / 4) * (
                self._level / 100) + self._level + 10)

    def get_other_ability(self, stat: str, character: int = 1) -> int:
        return math.floor(((self._basic_stats[stat] * 2 + self._individual_level[stat] + self._effort_values[stat] / 4) * (
                self._level / 100) + 5) * character)

    def get_experience(self, experience: int) -> None:
        self._experience += experience
        while True:
            if self._level_max_experience is None or self._experience <= self._level_max_experience:
                return
            self._experience = self._experience - self._level_max_experience
            self.level_up()

    def level_up(self) -> None:
        self._level += 1
        if self._evolution_level and self._level >= self._evolution_level:
            self.evolve_up()
        self._stats = self.get_stat()
        self._level_max_experience = self._experience_chart[self._level]['experience']

    def evolve_up(self):
        evolve_species = self.find_by_id(
            self._evolution_species_id,
            individual_level=self._individual_level,
            effort_values=self._effort_values,
            experience=self._experience,
            level=self._level
        )
        self._pokemon_id = evolve_species._pokemon_id
        self._name = evolve_species._name
        self._types = evolve_species._types
        self._basic_stats = evolve_species._basic_stats
        self._individual_level = evolve_species._individual_level
        self._effort_values = evolve_species._effort_values
        self._level = evolve_species._level
        self._evolution_level = evolve_species._evolution_level
        self._evolution_species_id = evolve_species._evolution_species_id
        self._stats = evolve_species._stats
        self._base_experience = evolve_species._base_experience
        self._experience = evolve_species._experience
        self._experience_chart = evolve_species._experience_chart
        self._level_max_experience = evolve_species._experience_chart
        self._moves = evolve_species._moves

    @classmethod
    def find_by_id(cls, pokemon_id: int, individual_level: dict = None, effort_values: dict = None, level: int = 1, experience: int = 0) -> Pokemon:
        if individual_level is None:
            individual_level = {}
        if effort_values is None:
            effort_values = {}

        pokemon_json_data = pb.get_api_by_id('pokemon', pokemon_id)
        pokemon_species_id = pokemon_json_data['species']['url']
        pokemon_species_json_data = pb.get_api_by_id('pokemon-species', pokemon_species_id.split('/')[-2])
        growth_rate_id = pokemon_species_json_data['growth_rate']['url']
        growth_rate_json_data = pb.get_api_by_id('growth-rate', growth_rate_id.split('/')[-2])
        evolution_chain_id = pokemon_species_json_data['evolution_chain']['url']
        evolution_chain_json_data = pb.get_api_by_id('evolution-chain', evolution_chain_id.split('/')[-2])

        pokemon_id = pokemon_json_data['id']

        name = pokemon_json_data['name']

        types = [x['type']['name'] for x in pokemon_json_data['types']]

        basic_stats = {}
        for stat in pokemon_json_data['stats']:
            stat_name = stat['stat']['name']
            basic_stats[stat_name] = stat['base_stat']

        if effort_values == {}:
            for stat in pokemon_json_data['stats']:
                stat_name = stat['stat']['name']
                effort_values[stat_name] = stat['effort']

        if not individual_level:
            individual_level = cls.get_individual_level()

        evolution = evolution_chain_json_data['chain']
        while True:
            if evolution['species']['url'].split('/')[-2] == pokemon_id:
                evolution_level = evolution['evolution_details'][0]['min_level']
                evolution_species_id = evolution['species']['url'].split('/')[-2]
                break
            if not evolution['evolves_to']:
                evolution_level = None
                evolution_species_id = None
                break
            evolution = evolution['evolves_to'][0]

        base_experience = pokemon_json_data['base_experience']

        experience_chart = growth_rate_json_data['levels']

        return Pokemon(
            pokemon_id=pokemon_id,
            name=name,
            types=types,
            basic_stats=basic_stats,
            individual_level=individual_level,
            effort_values=effort_values,
            level=level,
            evolution_level=evolution_level,
            evolution_species_id=evolution_species_id,
            base_experience=base_experience,
            experience=experience,
            experience_chart=experience_chart
        )

    def __str__(self) -> str:
        return f'Id: {self._pokemon_id}\n' \
               f'Name: {self._name}\n' \
               f'Type: {",".join(self._types)}\n' \
               f'Level: {self._level}\n' \
               f'Experience: {self._experience}\n' \
               f'Hp: {self._stats["hp"]}\n' \
               f'Attack: {self._stats["attack"]}\n' \
               f'Defense: {self._stats["defense"]}\n' \
               f'Speed: {self._stats["speed"]}\n' \
               f'Special-Attack: {self._stats["special_attack"]}\n' \
               f'Special-Defense: {self._stats["special_defense"]}'

