# Autor Gabriel Góes Rocha de Lima
# Data: 2024-06-25
# Descrição: Script principal para monitoramento de logs do Valheim
# valheim-server-notifier/odin/main.py
# Última atualização: 2024-06-29
# Versão: 0.1.1
# --------------------------------------------------------------------------- #
# Este projeto é um fork do projeto:
#    https://github.com/jaumebecks/valheim-server-notifier

# ------------------------- IMPORTS------------------------------------------ #
from lib.config import VALHEIM_LOG_PATH, DISCORD_WEBHOOK_URL
from lib.utils import read_logs
from event.matcher import resolve_event
from notifier.mapper import build_template
from notifier.discord import publish_event
from typing import Optional


# ------------------------- FUNÇÕES ----------------------------------------- #
def process_log(log: Optional[str] = None, next_log: Optional[str] = None):
    if log is None:
        return

    event = resolve_event(log, next_log)
    if event:
        template = build_template(event)
        publish_event(DISCORD_WEBHOOK_URL, template)


# --------------------------- MAIN ------------------------------------------ #
def main():
    if VALHEIM_LOG_PATH is None:
        raise EnvironmentError('Missing <VALHEIM_LOG_PATH> envvar')

    if DISCORD_WEBHOOK_URL is None:
        raise EnvironmentError('Missing <DISCORD_WEBHOOK_URL> envvar')

    logs = read_logs(path=VALHEIM_LOG_PATH)
    prev_log = None
    for log in logs:
        if prev_log:
            process_log(prev_log, log)
        prev_log = log
    if prev_log:
        process_log(prev_log)


# -------------------------- EXECUÇÃO --------------------------------------- #
if __name__ == '__main__':
    main()
