from pathlib import Path

class Environment:
    def __init__(self):
        pass

class Geographic(Environment):
    data_name: str

    def __init__(self, name: str):
        super().__init__()
        self.data_name = name

    def __repr__(self):
        return f"{self.data_name}"

class Room(Environment):
    universe: Path
    continent: Path
    nation: Path
    state: Path
    city: Path
    street: Path
    address_i: Path
    room_i: Path

    def __init__(self, universe: str,
        continent: str,
        nation: str,
        state: str,
        city: str,
        street: str,
        address_i: str,
        room_i):
        super().__init__()
        self.universe = Path(universe)
        self.continent = Path(continent)
        self.nation = Path(nation)
        self.state = Path(state)
        self.city = Path(city)
        self.street = Path(street)
        self.address_i = Path(address_i)
        self.room_i = Path(room_i)

    def __repr__(self):
        return f"{str(self.universe / self.continent / self.nation / self.state / self.city / self.street / self.address_i / self.room_i)}"
