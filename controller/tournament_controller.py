from model import models
from view import player_view, menus_view, tournament_view, round_view
from controller import writer_data_controller, menus_controller, round_controller
from tinydb import TinyDB, Query
import os
import time

user = Query()
tournament_table = writer_data_controller.tournament_table


class EnterDataTournement:
    @staticmethod
    def id_tournament():
        id_tournament = len(tournament_table) + 1
        return id_tournament

    @staticmethod
    def enter_name():
        while True:
            choice = input("Quel nom du tournoi ? ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice

    @staticmethod
    def enter_place():
        while True:
            choice = input("A quel endroit ? ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice

    @staticmethod
    def mode_tournament():
        choice = 0
        choice_list = [1, 2, 3]
        while choice not in choice_list:

            mode = input(
                "Quel mode pour le tournoi ?\n"
                "1 - Blitz ?\n"
                "2 - Bullet ?\n"
                "3 - Coup rapide ?\n"
            )
            try:
                choice = int(mode)
            except ValueError:
                menus_view.Menu.error_not_number()
        if choice == 1:
            choice = "blitz"
        elif choice == 2:
            choice = "bullet"
        else:
            choice = "coup_rapide"
        return choice

    @staticmethod
    def enter_description():
        while True:
            choice = input("Tapez une description du tournoi : ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice


class DataTournament(models.Tournament):
    def __init__(self):
        super().__init__(self)
        self.id_tournament = EnterDataTournement.id_tournament()
        self.name = EnterDataTournement.enter_name()
        self.place = EnterDataTournement.enter_place()
        self.start_date = "Le tournoi n'a pas encore commencé."
        self.round_number = "aucun pour le moment."
        self.time_control = EnterDataTournement.mode_tournament()
        self.description = EnterDataTournement.enter_description()
        self.players_id = []

    def data_tournament(self):
        self.tournament = {}
        self.tournament["id_tournament"] = self.id_tournament
        self.tournament["nom_tournoi"] = self.name
        self.tournament["endroit"] = self.place
        self.tournament["date_de_debut"] = self.start_date
        self.tournament["rounds_finis"] = self.round_number
        self.tournament["mode_blitz_bullet_ou_coup_rapide"] = self.time_control
        self.tournament["description"] = self.description
        self.tournament["id_des_joueurs_et_points"] = self.players_id
        return self.tournament

    @staticmethod
    def timestamp():
        now = time.localtime(time.time())
        timestamp = time.strftime("%d/%m/%Y %H:%M", now)
        return timestamp


class TournamentSerializer:
    @staticmethod
    def tournament_serializer():
        serialized_tournaments = []
        data_tournament = DataTournament().data_tournament()
        serialized_tournaments.append(data_tournament)
        return serialized_tournaments


class LoadingTournament:
    @staticmethod
    def tournaments_list():
        new_tournaments_list = TournamentDeserializer.list_tournaments()
        name_tournament = input("\nTapez le nom du tournoi :\n")
        if name_tournament in new_tournaments_list:
            tournament_view.ShowTournament.view_tournament_name_choose(name_tournament)
        else:
            tournament_view.ShowTournament.view_tournament_not_exist()
            menus_controller.Menus.main_menu()
        return name_tournament


class TournamentDeserializer:
    @staticmethod
    def info_tournament(tournament_name):
        tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        name = (tournament[0])["nom_tournoi"]
        place = (tournament[0])["endroit"]
        start_date = (tournament[0])["date_de_debut"]
        round_number = (tournament[0])["rounds_finis"]
        time_control = (tournament[0])["mode_blitz_bullet_ou_coup_rapide"]
        description = (tournament[0])["description"]
        tournament_view.ShowTournament.view_info_tournament(
            name, place, start_date, round_number, time_control, description
        )

    @staticmethod
    def list_tournaments():
        tournaments_list = TournamentDeserializer.all_tournaments_name()
        if len(tournament_table) == 0:
            tournament_view.ShowTournament.view_none_tournament()
            menus_controller.Menus.main_menu()
        else:
            new_tournaments_list = tournament_view.ShowTournament.view_all_tournaments(
                tournaments_list
            )
            return new_tournaments_list

    @staticmethod
    def all_tournaments_name():
        name_tournaments = []
        for data in tournament_table:
            names = data["nom_tournoi"]
            name_tournaments.append(names)
        return name_tournaments
