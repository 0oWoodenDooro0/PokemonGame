from pokemon import Pokemon


class Player:
    def __init__(self, username: str):
        self._username = username
        self._pokemon = []
        self._pokeballs = 15
        self._greatballs = 0
        self._ultraballs = 0
        self._money = 1000

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def pokemon(self):
        return self._pokemon

    @property
    def pokeballs(self):
        return self._pokeballs

    @pokeballs.setter
    def pokeballs(self, pokeballs: int):
        self._pokeballs = pokeballs

    @property
    def greatballs(self):
        return self._greatballs

    @greatballs.setter
    def greatballs(self, greatballs: int):
        self._greatballs = greatballs

    @property
    def ultraballs(self):
        return self._ultraballs

    @ultraballs.setter
    def ultraballs(self, ultraballs: int):
        self._ultraballs = ultraballs

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money: int):
        self._money = money

    def add_pokemon(self, pokemon: Pokemon) -> None:
        self._pokemon.append(pokemon)

    def get_pokemon(self) -> list:
        return self._pokemon

    def use_pokeball(self) -> bool:
        if self._pokeballs > 0:
            self._pokeballs -= 1
            return True
        return False

    def use_greatball(self) -> bool:
        if self._greatballs > 0:
            self._greatballs -= 1
            return True
        return False

    def use_ultraball(self) -> bool:
        if self._ultraballs > 0:
            self._ultraballs -= 1
            return True
        return False

    def use_money(self, price: int) -> bool:
        if self._money > price:
            self._money -= price
            return True
        return False

    def __str__(self):
        return f'Name: {self._username}\n' \
               f'Number of Pokemon: {len(self._pokemon)}\n' \
               f'Pokeball: {self._pokeballs}\n' \
               f'Greatball: {self._greatballs}\n' \
               f'Ultraball: {self._ultraballs}\n' \
               f'Money: {self._money}'
