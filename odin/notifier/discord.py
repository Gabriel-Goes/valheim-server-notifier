from requests import post

from . import Template


def publish_event(webhook_url: str, event: Template):
    json = event.get_payload()
    print(f'Event published: {json}')
    post(
        webhook_url,
        json=json,
        headers={'Content-Type': 'application/json'}
    )
