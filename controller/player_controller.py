from tinydb import Query
from model import models
from view import player_view, tournament_view
from controller import writer_data_controller as w

user = Query()


class EnterDataPlayer:
    """It Allows you to enter data for player."""
    @staticmethod
    def id_player():
        """It gets id_player from length to player_table.
        Returns id_player
        """
        id_player = len(w.players_table) + 1
        return id_player

    @staticmethod
    def enter_lastname():
        """It gets input for lastname's player in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("Nom : ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice.upper().replace(" ", "_")

    @staticmethod
    def enter_firstname():
        """It gets input for firstname's player in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("Prénom : ")
            if choice == "":
                tournament_view.ShowTournament.view_error_empty()
            else:
                return choice.upper().replace(" ", "_")

    @staticmethod
    def enter_date_of_birth():
        """It gets input for date of birth's player in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("Date de naissance (xx/xx/xxxx) : ")
            if choice == "":
                player_view.ShowPlayer.view_error_date()
            else:
                return choice

    @staticmethod
    def enter_sex():
        """It gets input for sex's player in choice.
        Returns choice or error message.
        """
        while True:
            choice = input("Sexe (H/F/X) : ")
            if choice != "H" and choice != "F" and choice != "X":
                player_view.ShowPlayer.view_error_sex()
            else:
                return choice

    @staticmethod
    def enter_ranking():
        """It gets input for ranking's player in choice.
        Returns choice or error message.
        """
        while True:
            try:
                choice = int(input("Rang dans le classement général: "))
                return choice
            except ValueError:
                player_view.ShowPlayer.view_error_not_str_not_float()

    @staticmethod
    def enter_point():
        """It gets input for point's player in choice.
        Returns choice or error message.
        """
        while True:
            try:
                choice = float(input("Tapez son point pour ce match :"))
                return choice
            except ValueError:
                player_view.ShowPlayer.view_error_not_str()


class DataPlayer(models.Player):
    """It inherits from the model Player"""
    def __init__(self):
        """It initializes in the class id_player, lastname,
         firstname, date_of_birth, sex, ranking and tournament_point.
        """
        super().__init__(self)
        self.id_player = EnterDataPlayer.id_player()
        self.lastname = EnterDataPlayer.enter_lastname()
        self.firstname = EnterDataPlayer.enter_firstname()
        self.date_of_birth = EnterDataPlayer.enter_date_of_birth()
        self.sex = EnterDataPlayer.enter_sex()
        self.ranking = EnterDataPlayer.enter_ranking()
        self.tournament_point = 0.0

    def player_list(self):
        """It creates dictionary player with inside id_player,
         lastname, firstname, date_of_birth, sex,
          ranking and tournament_point.
         Returns player
        """
        self.player = {}
        self.player["id_joueur"] = self.id_player
        self.player["nom"] = self.lastname
        self.player["prenom"] = self.firstname
        self.player["date_de_naissance"] = self.date_of_birth
        self.player["sexe"] = self.sex
        self.player["rang_dans_le_classement_general"] = self.ranking
        return self.player


class PlayersSerializer:
    """serialization's methods for player data."""
    @staticmethod
    def length_players_list_id(tournament_name=""):
        """Thanks to tournament_name, gets the number of players.
        Returns length_players_id
        """
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == tournament_name.replace(" ", "_")
        )
        player_list_id = (data_tournament[0])["id_des_joueurs_et_points"]
        length_players_id = len(player_list_id)
        return length_players_id

    @staticmethod
    def number_players_entered(tournament_name):
        """Thanks to tournament_name and tournament_name,
         gets the number of players entered and add one.
        Returns number_entered
        """
        lenght_players = (
            PlayersSerializer.length_players_list_id(tournament_name)
        )
        number_entered = lenght_players + 1
        return number_entered

    @staticmethod
    def number_players():
        """It gets number of players max.
        Returns players_number
        """
        players_number = 8
        return players_number

    @staticmethod
    def players_serializer():
        """It serializes dictionary player.
        Returns serialized_players
        """
        serialized_players = []
        data_list = DataPlayer().player_list()
        serialized_players.append(data_list)
        return serialized_players

    @staticmethod
    def lastname_players():
        """It creates à list of lastnames
        thanks to players_table.
        Returns lastnames_list
        """
        lastnames_list = []
        for item in w.players_table:
            lastname = item["nom"]
            lastnames_list.append(lastname)
        return lastnames_list

    @staticmethod
    def firstname_players():
        """It creates à list of firtsnames
        thanks to players_table.
        Returns firstnames_list
        """
        firstnames_list = []
        for item in w.players_table:
            firstname = item["prenom"]
            firstnames_list.append(firstname)
        return firstnames_list


class PlayersDeserializer:
    """Deserialization's methods for player data."""
    @staticmethod
    def choose_player_in_rank(tournament_name):
        """It gets a player thanks to tournament_name and the
         input for lastname and firstname.
        It adds a player in tournament if possible.
        """
        point_start = 0.0
        name = input("Tapez son nom : ").upper().replace(" ", "_")
        firstname = input("Tapez son prénom : ").upper().replace(" ", "_")
        id_lastname_firstname = (
            PlayersDeserializer.compare_id_lastname_firstname(
                name, firstname
            )
        )
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == f"{tournament_name.replace(' ','_')}"
        )

        id_players_list_with_point = (
            (data_tournament[0])["id_des_joueurs_et_points"]
        )
        players_tournament = []

        for id in id_players_list_with_point:
            players_tournament.append(id[0])
        ids = f"{name} {firstname}"
        id_players_table_list = []

        for id_player in w.players_table.all():
            id_players_table_list.append(id_player["id_joueur"])

        if id_lastname_firstname in id_players_table_list:
            if id_lastname_firstname in players_tournament:
                player_view.ShowPlayer.view_player_already_exist_tournament()
            else:
                check_id = w.players_table.search(
                    user.id_joueur == id_lastname_firstname
                )
                id_player_with_point = [check_id[0]["id_joueur"], point_start]
                id_players_list_with_point.append(id_player_with_point)
                w.tournament_table.update(
                    {"id_des_joueurs_et_points": id_players_list_with_point},
                    user.nom_tournoi == f"{tournament_name.replace(' ','_')}",
                )
                player_view.ShowPlayer.view_new_player(ids)
        else:
            player_view.ShowPlayer.view_player_not_exist()

    @staticmethod
    def change_rank_player(list_player):
        """It gets a player id thanks to list_player and the
         input for lastname and firstname.
        It changes ranking player if possible.
        """
        lastname = input("Tapez son nom : ").upper().replace(" ", "_")
        firstname = input("Tapez son prénom : ").upper().replace(" ", "_")
        checkname = list_player.search(user.nom == lastname)
        checkfirstname = list_player.search(user.prenom == firstname)

        if checkname and checkfirstname:
            rank = EnterDataPlayer.enter_ranking()
            list_player.update(
                {"rang_dans_le_classement_general": rank},
                user.nom == lastname,
            )
            player_view.ShowPlayer.view_player_change_rank(
                lastname, firstname, rank
            )
        else:
            player_view.ShowPlayer.view_player_wrong_name()

    @staticmethod
    def change_point_player(players_table, player_name, tournament_name):
        """It gets a player id thanks to players_table,
         player_name and tournament_name.t
        It changes point player if possible.
        """
        name_split = str(player_name).split()
        lastname = name_split[0]
        firstname = name_split[1]
        checkname = players_table.search(user.nom == lastname)
        checkfirstname = players_table.search(user.prenom == firstname)
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == f"{tournament_name}"
        )
        id_lastname_firstname = (
            PlayersDeserializer.compare_id_lastname_firstname(
                lastname, firstname
            )
        )

        if checkname and checkfirstname:
            id_player = players_table.search(
                user.id_joueur == id_lastname_firstname
            )
            id_players_list = (data_tournament[0])["id_des_joueurs_et_points"]
            point_existing = 0
            id_and_new_point = []
            point = EnterDataPlayer.enter_point()
            for player in id_players_list:
                id = player[0]
                if id_player[0]["id_joueur"] == id:
                    point_existing = player[1]
                    player[1] = point + point_existing
                id_and_new_point.append(player)
                w.tournament_table.update(
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
    def players_list_order(list_players, key_order, keys):
        """It arranges by order the list player, thanks to list_players
        , key_order and keys """
        if len(list_players):
            list_players_sort_name = sorted(
                list_players, key=lambda x: x[key_order])
            index_player = 1
            for item in list_players_sort_name:
                item_cut = {k: item[k] for k in keys}
                player = f"joueur {index_player}: {item_cut}"
                player_clean = (
                    player.replace("{", "")
                    .replace("}", "")
                    .replace("'", "")
                    .replace("_", " ")
                )
                player_view.ShowPlayer.view_player_clean(player_clean)
                index_player += 1
        else:
            player_view.ShowPlayer.view_none_player()

    @staticmethod
    def compare_id_lastname_firstname(lastname, firstname):
        """Thanks to lastname and firstname,
         compare them id player
         Returns if possible id_first_and_lastname
         """
        id_player_lastname = w.players_table.search(
            user.nom == f"{lastname}")
        id_player_firstname = w.players_table.search(
            user.prenom == f"{firstname}")
        id_lastname = []
        id_firstname = []

        for id_l in id_player_lastname:
            id_lastname.append(id_l["id_joueur"])

        for id_f in id_player_firstname:
            id_firstname.append(id_f["id_joueur"])

        if set(id_lastname) & set(id_firstname):
            id = set(id_lastname) & set(id_firstname)
            id_str = str(id)
            id_first_and_lastname = int(id_str.replace(
                "{", "").replace("}", ""))
        else:
            id_first_and_lastname = None

        return id_first_and_lastname
