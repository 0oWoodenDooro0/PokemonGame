import pickle
import random

from player import Player
from pokebase import Pokebase as pb
from pokemon import Pokemon as pm


class Game:

    def __init__(self):
        self._encounter_rate: list = self.get_encounter_rate()
        self.player = None
        self.random_pokemon = None
        self.random_pokemon_rate = None
        self.random_pokemon_base_score = None
        self.shop_list = {
            'poke-ball': 200,
            'great-ball': 600,
            'ultra-ball': 800
        }
        self.ball_list = {
            1: 'poke-ball',
            2: 'great-ball',
            3: 'ultra-ball'
        }

    def start(self):
        player_name = input('input your name:\n>')
        self.player = self.recover_player_data(player_name)
        self.save_player_data(self.player)
        self.help()
        while True:
            action = input('>')
            if action == 'w':
                self.wild()
            elif action == 's':
                self.shop()
            elif action == 'p':
                self.pokemon()
            elif action == 'i':
                self.player_information()
            elif action == 'h':
                self.help()
            elif action == 'e':
                self.save_player_data(self.player)
                exit()

    @staticmethod
    def save_player_data(player: Player) -> None:
        player_name = player.username
        player_data = pickle.dumps(player)

        with open(f'./player_data/{player_name}.pkl', 'wb') as file:
            file.write(player_data)

    @staticmethod
    def recover_player_data(player_name: str) -> Player:
        try:
            with open(f'./player_data/{player_name}.pkl', 'rb') as file:
                player_data = file.read()

            player = pickle.loads(player_data)
        except FileNotFoundError:
            player = Player(player_name)

        return player

    @staticmethod
    def get_encounter_rate() -> list:
        encounter_rate_list = []
        for pal_park_area_id in range(5):
            pal_park_area_json_data = pb.get_api_by_id('pal-park-area', pal_park_area_id + 1)

            encounter_rate_list += [{
                'pokemon_id': encounter_rate['pokemon_species']['url'].split('/')[-2],
                'rate': encounter_rate['rate'], 'base_score': encounter_rate['base_score']
            } for encounter_rate in pal_park_area_json_data['pokemon_encounters']]
        encounter_rate_list.sort(key=lambda x: int(x['pokemon_id']))

        return encounter_rate_list

    def catch(self, pokeball_rate):
        if self.random_pokemon_rate * pokeball_rate <= random.randint(0, 255):
            print(f'????????????{self.random_pokemon.name}')
            self.player.add_pokemon(self.random_pokemon)
            self.player.money += self.random_pokemon_base_score
        else:
            print(f'{self.random_pokemon.name}?????????')

    def wild(self) -> None:
        random_pokemon_encounter = random.choices(self._encounter_rate, [encounter['rate'] for encounter in self._encounter_rate])
        self.random_pokemon = pm.find_by_id(random_pokemon_encounter[0]['pokemon_id'])
        self.random_pokemon_rate = random_pokemon_encounter[0]['rate']
        self.random_pokemon_base_score = random_pokemon_encounter[0]['base_score']
        print(f'?????????????????????{self.random_pokemon.name}')
        print(f'??????{self.player.pokeballs}???poke-ball, {self.player.greatballs}???greatball, {self.player.ultraballs}???ultraball')
        print(f'??????pb ???poke-ball, ??????gb ???ultra-ball, ??????ub ???ultra-ball')
        while True:
            ball = input('>')
            if ball == 'pb' and self.player.use_pokeball():
                print('?????????poke-ball')
                self.catch(1)
                return
            if ball == 'gb' and self.player.use_greatball():
                print('?????????great-ball')
                self.catch(1.5)
                return
            if ball == 'ub' and self.player.use_ultraball():
                print('?????????ultra-ball')
                self.catch(2)
                return
            if ball == 'back':
                return
            print('????????????????????????')

    def pokemon(self):
        pokemons = self.player.get_pokemon()
        while True:
            for index, pokemon in enumerate(pokemons):
                if index == 6:
                    break
                print(f'{index + 1} {pokemon.name}')
            index = input('>')
            if index == 'back':
                return
            try:
                if int(index) - 1 >= 6:
                    raise IndexError
                print(pokemons[int(index) - 1])
                return
            except(IndexError, ValueError):
                print('???????????????????????????')

    def player_information(self):
        print(self.player)

    def buy(self, index: int, quantity: int = 1) -> bool:
        if 0 < index <= len(self.shop_list):
            item = list(self.shop_list.keys())[index - 1]
            price = self.shop_list.get(item)

            if self.player.use_money(price * quantity):
                if index == 1:
                    self.player.pokeballs += quantity
                elif index == 2:
                    self.player.greatballs += quantity
                elif index == 3:
                    self.player.ultraballs += quantity
                print(f'??????{price * quantity}????????????{quantity}???{self.ball_list[index]},??????{self.player.money}??????')
                return True
            else:
                print("??????????????????")
                return False
        else:
            print("??????????????????,????????????")
            return False

    def shop(self):
        while True:
            print(f'Money: {self.player.money}')
            for index, (item, price) in enumerate(self.shop_list.items()):
                print(f'{index + 1} {item} {price}')
            user_input = input(">")
            if user_input == 'back':
                return
            parts = user_input.split()
            try:
                if len(parts) == 1:
                    quantity = 1
                else:
                    quantity = int(parts[1])
                index = int(parts[0])
                if self.buy(index, quantity):
                    break
            except ValueError:
                print("????????????,????????????")

    @staticmethod
    def help():
        print('??????w ??????????????????pokemon, ??????s ????????????, ??????i ??????????????????, ??????p ??????pokemon, ??????h ????????????, ??????e ??????')
