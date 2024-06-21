from . import Event


class Death(Event):
    viking: str

    def __init__(self, viking: str) -> None:
        self.viking = viking

    def __str__(self) -> str:
        return f'**Camarada {self.viking} deitou!**'


class Join(Event):
    viking: str

    def __init__(self, viking: str) -> None:
        self.viking = viking

    def __str__(self) -> str:
        return f'*Camarada {self.viking} se uniu a batalha!*'


class ServerOn(Event):
    def __str__(self) -> str:
        return '🟢 **Mundo aberto e rodando!** 🟢'


class ServerOff(Event):
    def __str__(self) -> str:
        return f'🛑 **Mundo está fechado** 🛑'


class WorldSave(Event):
    duration: str

    def __init__(self, duration) -> None:
        self.duration = duration

    def __str__(self) -> str:
        return f'*Mundo foi salvo. Levou {self.duration}!*'
