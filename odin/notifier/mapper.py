from event import types
from . import Template


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
        payload = super().get_payload()
        payload['embeds'] = [{
            'author': {
                'name': 'Yamanderu',
                'icon_url': 'https://raw.githubusercontent.com/Gabriel-Goes/valheim-server-notifier/main/images/Yamanderu_retrato.jpg',
            },
            'title': f'Ah não, {self.event.viking}! Sua hora não chegou, levante-se!',
            'description': 'Retorne à batalha, guerreiro!',
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
