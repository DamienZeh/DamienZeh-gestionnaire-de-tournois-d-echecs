from model import models
from view import player_view, tournament_view
from controller import tournament_controller, writer_data_controller

from tinydb import TinyDB, Query

user = Query()
tournament_table = writer_data_controller.tournament_table
players_table = writer_data_controller.players_table


class EnterDataPlayer:
    @staticmethod
    def id_player():
        id_player = len(writer_data_controller.players_table) + 1
        return id_player

    @staticmethod
    def enter_lastname():
        while True:
            choice = input("Nom : ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice

    @staticmethod
    def enter_firstname():
        while True:
            choice = input("Prénom : ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice

    @staticmethod
    def enter_date_of_birth():
        while True:
            choice = input("Date de naissance (xx/xx/xxxx) : ")
            if choice == "":
                player_view.ShowPlayer.view_error_date()
            else:
                return choice

    @staticmethod
    def enter_sex():
        while True:
            choice = input("Sexe (H/F/X) : ")
            if choice != "H" and choice != "F" and choice != "X":
                player_view.ShowPlayer.view_error_sex()
            else:
                return choice

    @staticmethod
    def enter_ranking():
        while True:
            try:
                choice = int(input("Rang dans le classement général: "))
                return choice
            except ValueError:
                player_view.ShowPlayer.view_error_not_str()

    @staticmethod
    def enter_point():
        while True:
            try:
                choice = float(input("Tapez son point pour ce match :"))
                return choice
            except ValueError:
                player_view.ShowPlayer.view_error_not_str()


class DataPlayer(models.Player):
    def __init__(self):
        super().__init__(self)
        self.id_player = EnterDataPlayer.id_player()
        self.lastname = EnterDataPlayer.enter_lastname()
        self.firstname = EnterDataPlayer.enter_firstname()
        self.date_of_birth = EnterDataPlayer.enter_date_of_birth()
        self.sex = EnterDataPlayer.enter_sex()
        self.ranking = EnterDataPlayer.enter_ranking()
        self.tournament_point = 0.0

    def player_list(self):
        self.player = {}
        self.player["id_joueur"] = self.id_player
        self.player["nom"] = self.lastname
        self.player["prenom"] = self.firstname
        self.player["date_de_naissance"] = self.date_of_birth
        self.player["sexe"] = self.sex
        self.player["rang_dans_le_classement_general"] = self.ranking
        return self.player


class PlayersSerializer:
    @staticmethod
    def length_players_list_id(tournament_name=""):
        data_tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        player_list_id = (data_tournament[0])["id_des_joueurs_et_points"]
        lenght_players_id = len(player_list_id)
        return lenght_players_id

    @staticmethod
    def number_players_entered(tournament_name):
        lenght_players = PlayersSerializer.length_players_list_id(tournament_name)
        number_entered = lenght_players + 1
        return number_entered

    @staticmethod
    def number_players():
        players_number = 8
        return players_number

    @staticmethod
    def players_serializer():
        serialized_players = []
        data_list = DataPlayer().player_list()
        serialized_players.append(data_list)
        return serialized_players

    @staticmethod
    def lastname_players():
        lastnames_list = []
        for item in players_table:
            lastname = item["nom"]
            lastnames_list.append(lastname)
        return lastnames_list

    @staticmethod
    def firstname_players():
        firstnames_list = []
        for item in players_table:
            firstname = item["prenom"]
            firstnames_list.append(firstname)
        return firstnames_list


class PlayersDeserializer:
    @staticmethod
    def choose_player_in_rank(players_table, tournament_name):
        players_list_lastnames = []
        players_list_firstnames = []
        point_start = 0.0
        name = input("Tapez son nom : ")
        firstname = input("Tapez son prénom : ")
        checkName = players_table.search(user.nom == name)
        checkFirstname = players_table.search(user.prenom == firstname)
        data_tournament = tournament_table.search(
            user.nom_tournoi == f"{tournament_name}"
        )
        id_players_list = (data_tournament[0])["id_des_joueurs_et_points"]
        if checkName and checkFirstname:
            for player in id_players_list:
                lastnames_list = players_table.search(user.id_joueur == player[0])
                players_list_lastnames.append((lastnames_list[0])["nom"])
                firstnames_list = players_table.search(user.id_joueur == player[0])
                players_list_firstnames.append((firstnames_list[0])["prenom"])

            id_player = [(checkName[0])["id_joueur"], point_start]
            dict_checkmate = checkName[0]
            lastname = dict_checkmate["nom"]
            firstname = dict_checkmate["prenom"]
            if (
                lastname not in players_list_lastnames
                or firstname not in players_list_firstnames
            ):
                id_players_list.append(id_player)
                tournament_table.update(
                    {"id_des_joueurs_et_points": id_players_list},
                    user.nom_tournoi == f"{tournament_name}",
                )
                player_view.ShowPlayer.view_new_player_in_ranking(checkName)
            else:
                player_view.ShowPlayer.view_player_already_exist_tournament()
        else:
            player_view.ShowPlayer.view_player_wrong_name()

    @staticmethod
    def change_rank_player(list_player):
        lastname = input("Tapez son nom : ")
        firstname = input("Tapez son prénom : ")

        checkName = list_player.search(user.nom == lastname)
        checkFirstname = list_player.search(user.prenom == firstname)

        if checkName and checkFirstname:

            rank = EnterDataPlayer.enter_ranking()
            list_player.update(
                {"rang_dans_le_classement_general": rank},
                user.nom == lastname,
            )
            player_view.ShowPlayer.view_player_change_rank(lastname, firstname, rank)
        else:
            player_view.ShowPlayer.view_player_wrong_name()

    @staticmethod
    def change_point_player(players_table, player_name, tournament_name):
        name_split = str(player_name).split()
        lastname = name_split[0]
        firstname = name_split[1]
        checkName = players_table.search(user.nom == lastname)
        checkFirstname = players_table.search(user.prenom == firstname)
        data_tournament = tournament_table.search(
            user.nom_tournoi == f"{tournament_name}"
        )
        point = EnterDataPlayer.enter_point()
        if checkName and checkFirstname:
            id_player = (checkName[0])["id_joueur"]
            id_players_list = (data_tournament[0])["id_des_joueurs_et_points"]
            point_existing = 0
            id_and_new_point = []
            for player in id_players_list:
                id = player[0]
                if id_player == id:
                    point_existing = player[1]
                    player[1] = point + point_existing
                id_and_new_point.append(player)
                tournament_table.update(
                    {"id_des_joueurs_et_points": id_players_list},
                    user.nom_tournoi == tournament_name,
                )
            total_point = point + point_existing

            player_view.ShowPlayer.view_player_change_point(
                lastname, firstname, point, total_point
            )
        else:
            player_view.ShowPlayer.view_player_wrong_name()

    @staticmethod
    def players_list_order(players_table, key_order):
        list_players = players_table.all()
        if len(list_players):
            list_players_sort_name = sorted(list_players, key=key_order)
            index_player = 1
            for item in list_players_sort_name:
                try:
                    del item["id_joueur"]
                except KeyError:
                    continue
                player = f"joueur {index_player}: {item}"
                player_clean = player.replace("{", "").replace("}", "").replace("'", "")
                player_view.ShowPlayer.view_player_clean(player_clean)
                index_player += 1
        else:
            player_view.ShowPlayer.view_none_player()

    @staticmethod
    def players_list_tournament_order(list_players, key_order):

        if len(list_players):
            list_players_sort_name = sorted(list_players, key=key_order)
            index_player = 1
            for item in list_players_sort_name:
                player = f"joueur {index_player}: {item}"
                player_clean = player.replace("{", "").replace("}", "").replace("'", "")
                player_view.ShowPlayer.view_player_clean(player_clean)
                index_player += 1
        else:
            player_view.ShowPlayer.view_none_player()

    @staticmethod
    def key_order_alphabetical():
        key = lambda nom: nom["nom"]
        return key

    @staticmethod
    def key_order_ranking():
        key = lambda rang: rang["rang_dans_le_classement_general"]
        return key

    @staticmethod
    def key_order_point():
        key = lambda rang: rang["Points totaux du tournoi"]
        return key
