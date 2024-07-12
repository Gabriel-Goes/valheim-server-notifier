# Autor Gabriel Góes Rocha de Lima
# Data: 2024-06-25
# Descrição: Configurações de regex para os eventos de log
# valheim-server-notifier/odin/event/types.py
# Inspired from https://www.reddit.com/r/valheim/comments/n7vv9b/comment/gxihljp

# ------------------------- IMPORTS------------------------------------------ #
from . import Event


# ------------------------- TYPES------------------------------------------ #
class Death(Event):
    viking: str

    def __init__(self, viking: str) -> None:
        self.viking = viking

    def __str__(self) -> str:
        return f'**Camarada {self.viking} deitou!**'


class Join(Event):
    viking: str
    zdoid: str

    def __init__(self, viking: str, zdoid: str) -> None:
        self.viking = viking
        self.zdoid = zdoid

    def __str__(self) -> str:
        return f'*Camarada {self.viking}|{self.zdoid} se uniu a batalha!*'


class DestroyZDO(Event):
    zdoid: str

    def __init__(self, zdoid: str) -> None:
        print("ZDOID CALL")
        self.zdoid = zdoid

    def __str__(self) -> str:
        from notifier.mapper import player_zdoid_map
        player_name = player_zdoid_map.get(self.zdoid, f'ZDO {self.zdoid}')
        return f'O Camarada {player_name} deixou a batalha!'


class Leave(Event):
    viking: str

    def __init__(self, viking: str) -> None:
        self.viking = viking

    def __str__(self) -> str:
        return f'O Camarada {self.viking} deixou a batalha!'


class JoinCode(Event):
    join_code: str

    def __init__(self, join_code: str) -> None:
        self.join_code = join_code

    def __str__(self) -> str:
        return f'*Código de entrada: {self.join_code}*'


class ServerOn(Event):
    def __str__(self) -> str:
        return '🟢 **Mundo aberto e rodando!** 🟢'


class ServerOff(Event):
    def __str__(self) -> str:
        return '🛑 **Mundo está fechado** 🛑'


class WorldSave(Event):
    duration: str

    def __init__(self, duration) -> None:
        self.duration = duration

    def __str__(self) -> str:
        return f'*Mundo foi salvo. Levou {self.duration}!*'
