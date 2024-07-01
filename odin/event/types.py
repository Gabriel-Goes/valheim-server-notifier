from . import Event


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
        return f'*Camarada {self.viking} se uniu a batalha!*'


class Leave(Event):
    viking: str

    def __init__(self, viking: str) -> None:
        self.viking = viking

    def __str__(self) -> str:
        return f'*Camarada {self.viking} abandonou a batalha!*'


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
