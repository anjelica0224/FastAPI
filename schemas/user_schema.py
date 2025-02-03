def UserDictionary(player) -> dict:
    return {
        "id" : str(player["_id"]),
        "name": player["name"],
        "time_taken": player["time_taken"]
    }

def UserList(players) -> list:
    return [UserDictionary(player) for player in players]