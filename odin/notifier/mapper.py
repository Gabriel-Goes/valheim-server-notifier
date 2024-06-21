from event import types
from . import Template

import os
import json
from datetime import datetime


# ----------------------- Funções de Placar de Mortes ----------------------- #
def read_scoreboard(scoreboard_file):
    if not os.path.exists(scoreboard_file):
        return {}
    scoreboard = {}
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


def save_scoreboard(scoreboard_file, scoreboard):
    with open(scoreboard_file, 'w') as f:
        f.write("NOME;MORTES;DATAS\n")
        for player, (deaths, dates) in scoreboard.items():
            f.write(f"{player};{deaths};{json.dumps(dates)}\n")


def return_scoreboard_with_last_dates(scoreboard_file):
    scoreboard = read_scoreboard(scoreboard_file)
    last_dates_scoreboard = {}
    for player, (deaths, dates) in scoreboard.items():
        last_dates_scoreboard[player] = (deaths, dates[-1])

    return last_dates_scoreboard


def save_death_event(player_name):
    scoreboard_file = '/home/steam/Valheim/scoreboard.csv'
    scoreboard = read_scoreboard(scoreboard_file)

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if player_name in scoreboard:
        deaths, dates = scoreboard[player_name]
        dates.append(current_date)
        scoreboard[player_name] = (deaths + 1, dates)
    else:
        scoreboard[player_name] = (1, [current_date])
    save_scoreboard(scoreboard_file, scoreboard)


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
        payload = super().get_payload()
        payload['embeds'] = [{
            'author': {
                'name': 'Yamanderu',
                'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
            },
            'title': f'Bemvindo, caro camarada {self.event.viking}, bom revê-lo!',
            'description': 'Unidos venceremos!',
        }]
        return payload


class DeathTemplate(Template):
    def get_payload(self) -> dict:
        player_name = self.event.viking
        save_death_event(player_name)
        scoreboard_file = '/home/steam/Valheim/scoreboard.csv'
        scoreboard_atualizado = return_scoreboard_with_last_dates(scoreboard_file)

        scoreboard_str = "Placar de Mortes:\n   NOME   MORTES   ÚLTIMA MORTE\n================================\n"
        for player, (deaths, last_date) in scoreboard_atualizado.items():
            scoreboard_str += f" {player}  {deaths}   {last_date}\n"

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
    types.Death: DeathTemplate,
    types.WorldSave: WorldSaveTemplate,
}


def build_template(event: types.Event) -> Template:
    template = MAP.get(type(event))
    if not template:
        raise Exception(f'Template mapping for given event <{type(event)}> not found')

    return template(event)
