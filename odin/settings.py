from event import types

# Inspired from https://www.reddit.com/r/valheim/comments/n7vv9b/comment/gxihljp
LOG_EVENT_TYPE_REGEXES = {
    "player_died": {
        "regex": r"Got character ZDOID from (?P<viking>\w+[ \w+]*) : 0:0",
        'class': types.Death,
    },
    "player_joined": {
        "regex": r"Got character ZDOID from (?P<viking>\w+[ \w+]*) : [-0-9]*:[-0-9]*$",
        'class': types.Join,
    },
    "game_server_connected": {
        "regex": r"Game server connected",
        'class': types.ServerOn,
    },
    "game_server_shutdown": {
        "regex": r"OnApplicationQuit",
        'class': types.ServerOff,
    },
    "world_saved": {
        "regex": r"World saved \( (\d+\.\d+ms) \)",
        'class': types.WorldSave,
    },
    "found_location": {
        "regex": r"Found location of type (\w+)",
        "capture_groups": {1: "location_type"},
    },
    "steam_user_joined": {
        "regex": r"Got connection SteamID (\d+)",
        "capture_groups": {1: "steam_id"},
    },
    "valheim_version": {
        "regex": r"Valheim version:(\d+\.\d+\.\d+)",
        "capture_groups": {1: "valheim_version"},
    },
}
