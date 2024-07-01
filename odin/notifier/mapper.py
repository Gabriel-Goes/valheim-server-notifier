# Autor Gabriel Góes Rocha de Lima
# Data: 2024-06-25
# Descrição:
# valheim-server-notifier/odin/notifier/mapper.py

# ------------------------- IMPORTS------------------------------------------ #
from lib.config import SCOREBOARD_FILE as scoreboard_file
from event import types
from . import Template
import os
import json
from datetime import datetime


# ------------------------- Armazenamento de ZDOID -------------------------- #
player_zdoid_map = {}


# ----------------------- Funções de Placar de Mortes ----------------------- #
def read_scoreboard():
    if not os.path.exists(scoreboard_file):
        raise f"Scoreboard file not found: {scoreboard_file}"
        return {}
    scoreboard = {}
    print(f"Reading scoreboard from {scoreboard_file}")
    with open(scoreboard_file, 'r') as f:
        next(f)
        for line in f:
            if line.strip() and ';' in line:
                parts = line.strip().split(';')
                if len(parts) == 3:
                    player, deaths, dates = parts
                    if player and deaths and dates:
                        scoreboard[player.strip()] = (
                            int(deaths.strip()),
                            json.loads(dates.strip())
                        )
    return scoreboard


def save_scoreboard(scoreboard):
    with open(scoreboard_file, 'w') as f:
        f.write("NOME;MORTES;DATAS\n")
        for player, (deaths, dates) in scoreboard.items():
            f.write(f"{player};{deaths};{json.dumps(dates)}\n")


def return_scoreboard_with_last_dates(scoreboard):
    last_dates_scoreboard = {}
    for player, (deaths, dates) in scoreboard.items():
        last_dates_scoreboard[player] = (deaths, dates[-1])

    return last_dates_scoreboard


def save_join_event(player_name, zdoid, scoreboard):
    player_zdoid_map[zdoid] = player_name
    if player_name not in scoreboard:
        scoreboard[player_name] = (1, [datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    save_scoreboard(scoreboard)


def save_death_event(player_name):
    scoreboard = read_scoreboard()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if player_name in scoreboard:
        deaths, dates = scoreboard[player_name]
        dates.append(current_date)
        scoreboard[player_name] = (deaths + 1, dates)
    else:
        scoreboard[player_name] = (1, [current_date])
        print(f"Player {player_name} not found in scoreboard when should be.")
    save_scoreboard(scoreboard)


def get_scoreboard_str(player_name):
    scoreboard = read_scoreboard()
    save_death_event(player_name)
    scoreboard_atualizado = return_scoreboard_with_last_dates(scoreboard)

    max_player_length = max(len(player) for player in scoreboard_atualizado) if scoreboard_atualizado else len("NOME")
    max_deaths_length = len("MORTES")
    max_date_length = len("ÚLTIMA MORTE")

    header = f"{'NOME'.ljust(max_player_length)}  {'MORTES'.ljust(max_deaths_length)}  {'ÚLTIMA MORTE'.ljust(max_date_length)}\n"
    separator = "=" * (max_player_length + max_deaths_length + max_date_length + 4) + "\n"
    scoreboard_str = f"Placar de Mortes:\n{header}{separator}"
    for player, (deaths, last_date) in scoreboard_atualizado.items():
        scoreboard_str += f"{player.ljust(max_player_length)}  {str(deaths).ljust(max_deaths_length)}  {last_date.ljust(max_date_length)}\n"

    return scoreboard_str


# ----------------------- CLASSES TEMPLATES --------------------------------- #
class ServerOnTemplate(Template):
    def get_payload(self) -> dict:
        payload = super().get_payload()
        payload['embeds'] = [{
            'author': {
                'name': 'Yamanderu',
                'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
            },
            'title': 'Nosso mundo está pronto para a reunião dos maiores guerreiros',
            'description': 'Quem se unirá à nossa luta?',
        }]
        return payload


class ServerOffTemplate(Template):
    def get_payload(self) -> dict:
        payload = super().get_payload()
        payload['embeds'] = [{
            'author': {
                'name': 'Yamanderu',
                'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
            },
            'title': 'Nós precisamos de descanço. Até breve!',
            'description': 'Após a prática é necessário retornar à teoria. Nos veremos em breve!',
        }]
        return payload


class JoinTemplate(Template):
    def get_payload(self) -> dict:
        player_name = self.event.viking
        zdoid = self.event.zdoid
        scoreboard = read_scoreboard()
        if player_name not in scoreboard:
            save_join_event(player_name, zdoid, scoreboard)
            payload = super().get_payload()
            payload['embeds'] = [{
                'author': {
                    'name': 'Yamanderu',
                    'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
                },
                'title': f'Seja bemvindo, caro camarada {self.event.viking}!, esta é apenas a sua primeira morte!',
                'description': 'Unidos venceremos!',
            }]
        else:
            payload = super().get_payload()
            payload['embeds'] = [{
                'author': {
                    'name': 'Yamanderu',
                    'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
                },
                'title': f'{self.event.viking}, retornou à nossa luta!',
                'description': 'Unidos venceremos!',
            }]
        return payload


class JoinCodeTemplate(Template):
    def get_payload(self) -> dict:
        payload = super().get_payload()
        payload['embeds'] = [{
            'author': {
                'name': 'Yamanderu',
                'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
            },
            'title': 'Código de entrada disponível',
            'description': f'Código: {self.event.join_code} e senha: "marxleninmao"',
        }]
        return payload


class DeathTemplate(Template):
    def get_payload(self) -> dict:
        player_name = self.event.viking
        scoreboard_str = get_scoreboard_str(player_name)
        payload = super().get_payload()
        payload['embeds'] = [{
            'author': {
                'name': 'Yamanderu',
                'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
            },
            'title': f'Ah não, {player_name}! Sua hora não chegou, levante-se!',
            'description': f'{scoreboard_str}\n',
        }]
        return payload


class WorldSaveTemplate(Template):
    pass


MAP = {
    types.ServerOn: ServerOnTemplate,
    types.ServerOff: ServerOffTemplate,
    types.Join: JoinTemplate,
    types.JoinCode: JoinCodeTemplate,
    types.Death: DeathTemplate,
    types.WorldSave: WorldSaveTemplate,
}


def build_template(event: types.Event) -> Template:
    print(f'Building template for event <{type(event)}>...')
    template = MAP.get(type(event))
    if not template:
        print(f'Template mapping for given event <{type(event)}> not found')
        raise Exception(f'Template mapping for given event <{type(event)}> not found')

    return template(event)
