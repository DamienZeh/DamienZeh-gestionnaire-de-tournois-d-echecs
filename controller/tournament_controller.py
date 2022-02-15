import time
from tinydb import Query
from model import models
from view import menus_view, tournament_view
from controller import writer_data_controller as w, menus_controller

user = Query()


class EnterDataTournement:
    """It Allows you to enter data for tournament."""
    @staticmethod
    def id_tournament():
        """It gets id_tournament from length to tournament_table.
        Returns id_tournament
        """
        id_tournament = len(w.tournament_table) + 1
        return id_tournament

    @staticmethod
    def enter_name():
        """It gets input for name's tournament in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("Quel nom du tournoi ? ").upper().replace(" ", "_")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice

    @staticmethod
    def enter_place():
        """It gets input for place's tournament in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("A quel endroit ? ").upper().replace(" ", "_")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice

    @staticmethod
    def mode_tournament():
        """It gets input for mode's tournament in choice.
        Returns choice or error message.
        """
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
        """It gets input for description's tournament in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("Tapez une description du tournoi : ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice


class DataTournament(models.Tournament):
    """It inherits from the model Tournament"""
    def __init__(self):
        """It initializes in the class id_tournament, name,
         place, start_date, end_date, round_number, time_control,
          description and dictionary players_id.
        """
        super().__init__(self)
        self.id_tournament = EnterDataTournement.id_tournament()
        self.name = EnterDataTournement.enter_name()
        self.place = EnterDataTournement.enter_place()
        self.start_date = "Le tournoi n'a pas encore commencé."
        self.end_date = "Le tournoi n'est pas encore fini."
        self.round_number = "aucun pour le moment."
        self.time_control = EnterDataTournement.mode_tournament()
        self.description = EnterDataTournement.enter_description()
        self.players_id = []

    def data_tournament(self):
        """It creates dictionary tournament with inside id_tournament,
         name,place, start_date, end_date, round_number,
          time_control and description.
        Returns tournament
        """
        self.tournament = {}
        self.tournament["id_tournament"] = self.id_tournament
        self.tournament["nom_tournoi"] = self.name
        self.tournament["endroit"] = self.place
        self.tournament["date_de_debut"] = self.start_date
        self.tournament["date_de_fin"] = self.end_date
        self.tournament["rounds_finis"] = self.round_number
        self.tournament["mode_blitz_bullet_ou_coup_rapide"] = self.time_control
        self.tournament["description"] = self.description
        self.tournament["id_des_joueurs_et_points"] = self.players_id
        return self.tournament

    @staticmethod
    def timestamp():
        """Its gets date thanks to timestamp.
        Returns timestamp.
        """
        now = time.localtime(time.time())
        timestamp = time.strftime("%d/%m/%Y %H:%M", now)
        return timestamp


class TournamentSerializer:
    """serialization's methods for player data."""
    @staticmethod
    def tournament_serializer():
        """It gets serialize data_tournament.
        Returns serialized_tournaments
        """
        serialized_tournaments = []
        data_tournament = DataTournament().data_tournament()
        serialized_tournaments.append(data_tournament)
        return serialized_tournaments


class LoadingTournament:
    """Here is the method for loading a tournament."""
    @staticmethod
    def tournaments_list():
        """Its gets new_tournament_list, and name_tournament thanks to a input,
        and check if name_tournament is in new_tournament_list.
        Returns name_tournament.
        """
        new_tournaments_list = TournamentDeserializer.list_tournaments()
        name_tournament = input("\nTapez le nom du tournoi :\n").upper()
        if name_tournament in new_tournaments_list:
            tournament_view.ShowTournament.\
                view_tournament_name_choose(name_tournament)
        else:
            tournament_view.ShowTournament.view_tournament_not_exist()
            menus_controller.Menus.main_menu()
        return name_tournament


class TournamentDeserializer:
    """Deserialization's methods for tournament data."""
    @staticmethod
    def info_tournament(name_tournament):
        """Thanks to name_tournament, it gets data from tournament."""
        tournament_name = name_tournament.upper().replace(" ", "_")
        tournament = w.tournament_table.\
            search(user.nom_tournoi == tournament_name)

        name = (tournament[0])["nom_tournoi"]
        place = (tournament[0])["endroit"]
        start_date = (tournament[0])["date_de_debut"]
        round_number = (tournament[0])["rounds_finis"]
        time_control = (tournament[0])["mode_blitz_bullet_ou_coup_rapide"]
        description = (tournament[0])["description"]
        end_date = (tournament[0])["date_de_fin"]

        tournament_view.ShowTournament.view_info_tournament(
            name, place, start_date,
            round_number, time_control, description, end_date
        )

    @staticmethod
    def list_tournaments():
        """It gets tournament_list, and check the number of tournaments existing.
        Return new_tournaments_list or message for say none tournament.
        """
        tournaments_list = TournamentDeserializer.all_tournaments_name()
        if len(w.tournament_table) == 0:
            tournament_view.ShowTournament.view_none_tournament()
            menus_controller.Menus.main_menu()
        else:
            new_tournaments_list = \
                tournament_view.ShowTournament.view_all_tournaments(
                    tournaments_list
                )
            return new_tournaments_list

    @staticmethod
    def all_tournaments_name():
        """It gets tournaments name thanks to tournament_table.
        Return name_tournaments.
        """
        name_tournaments = []
        for data in w.tournament_table:
            names = data["nom_tournoi"]
            name_tournaments.append(names)
        return name_tournaments
