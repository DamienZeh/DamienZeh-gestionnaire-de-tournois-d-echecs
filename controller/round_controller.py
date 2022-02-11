from view import player_view, round_view
from model import models
from view import menus_view, tournament_view
from controller import (
    player_controller,
    tournament_controller,
    writer_data_controller,
    match_controller,
)
from view import player_view

from tinydb import TinyDB, Query

import re

user = Query()
tournament_table = writer_data_controller.tournament_table
round_table = writer_data_controller.round_table


class EnterDataRound:
    @staticmethod
    def round_name(tournament_name):
        id_tournament = EnterDataRound.id_round(tournament_name)
        data_round = round_table.search(user.id_round_tournoi == id_tournament)
        if data_round == []:
            name_round = "Round_1"
        else:
            number_round = int(len(data_round) + 1)
            name_round = f"Round_{number_round}"
        return name_round

    @staticmethod
    def id_round(tournament_name):
        tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        id_tournament = (tournament[0])["id_tournament"]
        id_round = id_tournament
        return id_round

    @staticmethod
    def enter_start_date():
        while True:
            choice = input("Tapez la date de début du round (xx/xx/xxxx) : ")
            if choice == "":
                player_view.ShowPlayer.view_error_date()
            else:
                return choice

    @staticmethod
    def enter_start_hour():
        while True:
            choice = input("tapez l'heure de début de round : ")
            if choice == "":
                round_view.ShowRound.view_error_hour()
            else:
                return choice

    @staticmethod
    def enter_end_date():
        while True:
            round_view.ShowRound.view_round_end()
            choice = input("Tapez la date de fin du round (xx/xx/xxxx) : ")
            if choice == "":
                player_view.ShowPlayer.view_error_date()
            else:
                return choice

    @staticmethod
    def enter_end_hour():
        while True:
            choice = input("tapez l'heure de fin de round : ")
            if choice == "":
                round_view.ShowRound.view_error_hour()
            else:
                return choice


class DataRound(models.Round):
    def __init__(self):
        super().__init__(self)
        self.start_round = {}
        self.end_round = {}

    def round_start_date(self, tournament_name, round_name):
        self.name_round = round_name
        self.id_round = EnterDataRound.id_round(tournament_name)
        self.start_date = ""
        self.start_round["id_round_tournoi"] = self.id_round
        self.start_round["nom_du_round"] = self.name_round
        self.start_round["date_debut_round"] = self.start_date
        return self.start_round

    def round_end_date(self):
        self.end_date = ""
        self.end_round["date_fin_round"] = self.end_date
        return self.end_round


class RoundSerializer:
    @staticmethod
    def round_start_serializer(tournament_name, round_name):
        round_serializer = []
        start_round = DataRound().round_start_date(tournament_name, round_name)
        round_serializer.append(start_round)
        return round_serializer

    @staticmethod
    def round_end_serializer(tournament_name, round_name):
        round_serializer = []
        end_round = DataRound().round_end_date()
        round_serializer.append(end_round)
        return round_serializer


class RoundDeserializer:
    @staticmethod
    def matches_round(tournament_name, round_name):
        user = Query()
        data_tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        id_tournament = (data_tournament[0])["id_tournament"]
        data_rounds_tournament = round_table.search(
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
        matches = RoundDeserializer.matches_round(tournament_name, round_name)

        round_view.ShowRound.view_matches_round(matches)

    @staticmethod
    def enter_result_player(tournament_name, round_name):
        players_table = writer_data_controller.players_table
        matches = RoundDeserializer.matches_round(tournament_name, round_name)
        match_index = 1
        player_view.ShowPlayer.point_player(
            match_index, players_table, matches, tournament_name
        )

    @staticmethod
    def all_rounds(tournament_name):
        tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        id_tournament = (tournament[0])["id_tournament"]
        data_round = round_table.search(user.id_round_tournoi == id_tournament)
        names_round = []
        for round in data_round:
            names_round.append(round["nom_du_round"])
        return names_round

    @staticmethod
    def all_matches_rounds(tournament_name):
        data_tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        rounds = data_tournament[0]["rounds_finis"]
        if rounds == "aucun pour le moment.":
            round_view.ShowRound.view_none_round()
        else:
            data_tournament = tournament_table.search(
                user.nom_tournoi == tournament_name
            )
            id_tournament = (data_tournament[0])["id_tournament"]
            data_rounds_tournament = round_table.search(
                user.id_round_tournoi == id_tournament
            )
            index = 0
            for round in data_rounds_tournament:
                round_view.ShowRound.view_matches_round(round)
                index += 1
