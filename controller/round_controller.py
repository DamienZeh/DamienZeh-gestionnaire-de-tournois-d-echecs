from tinydb import Query
from view import round_view, player_view
from model import models
from controller import writer_data_controller as w

user = Query()


class EnterDataRound:
    """It Allows you to enter data."""
    @staticmethod
    def round_name(tournament_name):
        """It creates round name based on previous existing round name,
        located by the tournament name.
        Returns next name_round.
        """
        id_tournament = EnterDataRound.id_round(tournament_name)
        data_round = w.round_table.\
            search(user.id_round_tournoi == id_tournament)

        if data_round == []:
            name_round = "Round_1"
        else:
            number_round = int(len(data_round) + 1)
            name_round = f"Round_{number_round}"
        return name_round

    @staticmethod
    def id_round(tournament_name):
        """It seeks id_round based on the tournament name.
        Returns id_round.
        """
        tournament = w.tournament_table.\
            search(user.nom_tournoi == tournament_name)
        id_tournament = (tournament[0])["id_tournament"]
        id_round = id_tournament
        return id_round


class DataRound(models.Round):
    """It inherits from the model Round"""
    def __init__(self):
        """It initializes in the class the dictionaries
         star_round and end_round.
        """
        super().__init__(self)
        self.start_round = {}
        self.end_round = {}

    def round_start_date(self, tournament_name, round_name):
        """It initializes attributes name_round, id_round, start_date,
        in dictionary start_round.
        Returns dictionary start_round.
        """
        self.name_round = round_name
        self.id_round = EnterDataRound.id_round(tournament_name)
        self.start_date = ""
        self.start_round["id_round_tournoi"] = self.id_round
        self.start_round["nom_du_round"] = self.name_round
        self.start_round["date_debut_round"] = self.start_date
        return self.start_round

    def round_end_date(self):
        """It initializes attributes end_date
        in dictionary end_round.
        Returns dictionary end_round.
        """
        self.end_date = ""
        self.end_round["date_fin_round"] = self.end_date
        return self.end_round


class RoundSerializer:
    """Serialization's methods for round data."""
    @staticmethod
    def round_start_serializer(tournament_name, round_name):
        """It serializes dictionary round_start,
         located by tournament_name and round_name
        Returns round_start
        """
        round_serializer = []
        start_round = DataRound().round_start_date(tournament_name, round_name)
        round_serializer.append(start_round)
        return round_serializer

    @staticmethod
    def round_end_serializer():
        """It serializes dictionary end_start
        Returns end_start
        """
        round_serializer = []
        end_round = DataRound().round_end_date()
        round_serializer.append(end_round)
        return round_serializer


class RoundDeserializer:
    """It deserializes rounds data."""
    @staticmethod
    def matches_round(tournament_name, round_name):
        """It deserializes all matches in a round
         located by tournament_name and round_name.
        Returns matches
         """
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == tournament_name)
        id_tournament = (data_tournament[0])["id_tournament"]
        data_rounds_tournament = w.round_table.search(
            user.id_round_tournoi == id_tournament
        )
        all_rounds = ""

        for rounds in data_rounds_tournament:
            name = rounds.get("nom_du_round")
            if name == round_name and "match 1" in rounds:
                all_rounds = rounds
        matches = all_rounds
        return matches

    @staticmethod
    def show_matches_round(tournament_name, round_name):
        """It takes matches from match_round and send it to the viewer
         located by tournament_name and round_name."""
        matches = RoundDeserializer.matches_round(tournament_name, round_name)
        round_view.ShowRound.view_matches_round(matches)

    @staticmethod
    def enter_result_player(tournament_name, round_name):
        """It takes matches from method match_round,
         tournament_name and round_name and sends them to point_player method
         """
        matches = RoundDeserializer.matches_round(tournament_name, round_name)
        match_index = 1
        player_view.ShowPlayer.point_player(
            match_index, w.players_table, matches, tournament_name, round_name
        )

    @staticmethod
    def all_rounds(tournament_name):
        """thanks to tournament_name, it create a list of name rounds.
        Return names_round.
        """
        tournament = w.tournament_table.\
            search(user.nom_tournoi == tournament_name)
        id_tournament = (tournament[0])["id_tournament"]
        data_round = w.round_table.\
            search(user.id_round_tournoi == id_tournament)
        names_round = []

        for round in data_round:
            names_round.append(round["nom_du_round"])
        return names_round

    @staticmethod
    def all_matches_rounds(tournament_name):
        """It gets all data in rounds thanks to tournament_name.
        It sends them to view_matches_round method
        """
        data_tournament = w.tournament_table\
            .search(user.nom_tournoi == tournament_name)
        rounds = data_tournament[0]["rounds_finis"]
        if rounds == "aucun pour le moment.":
            round_view.ShowRound.view_none_round()
        else:
            data_tournament = w.tournament_table.search(
                user.nom_tournoi == tournament_name
            )
            id_tournament = (data_tournament[0])["id_tournament"]
            data_rounds_tournament = w.round_table.search(
                user.id_round_tournoi == id_tournament
            )
            index = 0
            for round in data_rounds_tournament:
                round_view.ShowRound.view_matches_round(round)
                index += 1
