class Player:
    def __init__(
        self,
        id_player="",
        lastname="",
        firstname="",
        date_of_birth="",
        sex="",
        tournament_point="",
        ranking="",
    ):
        self.id_player = id_player
        self.lastname = lastname
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.tournament_point = tournament_point


class Tournament:
    def __init__(
        self,
        id_tournament="",
        name="",
        place="",
        start_date="",
        round_number="",
        time_control="",
        description="",
        players_id="",
    ):
        self.id_tournament = id_tournament
        self.name = name
        self.place = place
        self.start_date = start_date
        self.round_number = round_number
        self.time_control = time_control
        self.description = description
        self.players_id = players_id


class Round:
    def __init__(
        self,
        id_round="",
        name_round="",
        players_id="",
        number_round=4,
        start_date="",
        end_date="",
    ):
        self.id_round = id_round
        self.name_round = name_round
        self.players_id = players_id
        self.number_round = number_round
        self.start_date = start_date
        self.end_date = end_date


class Match:
    def __init__(self, match_name, first_player="", second_player="", result=""):
        self.match_name = match_name
        self.first_player = first_player
        self.second_player = second_player
        self.result = result
