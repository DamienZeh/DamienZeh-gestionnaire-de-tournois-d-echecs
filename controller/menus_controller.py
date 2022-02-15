from tinydb import Query
from view import menus_view, round_view, player_view
from controller import (
    player_controller,
    tournament_controller,
    writer_data_controller as w,
    round_controller,
)

user = Query()


class Menus:
    """It includes all methods for menus"""
    @staticmethod
    def welcome_menu():
        """Launches view_welcome_main_menu and main_menu"""
        menus_view.Menu.view_welcome_main_menu()
        Menus.main_menu()

    @staticmethod
    def main_menu():
        """Allows to view all tournaments, or view all players,
         or loading a tournament, or create a tournament,
          or change rank for player, or quit the software """
        choice = 0
        choice_list = [1, 2, 3, 4, 5, 6]
        while choice not in choice_list:
            menu = input(
                "\nMenu principal\nTapez un nombre"
                " correspondant à un des choix proposés.\n"
                "1 - Affichez tous les tournois en cours ou terminé.\n"
                "2 - Affichez la liste de tous les joueurs déjà enregistrés.\n"
                "3 - chargez un tournoi en cours ou terminé.\n"
                "4 - Créez un tournoi.\n"
                "5 - Modifiez le rang d'un joueur dans le classement général"
                "(hors joueur en cours d'un tournoi).\n"
                "6 - Quittez le programme.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()

        if choice == 1:
            tournament_controller.TournamentDeserializer.list_tournaments()
            Menus.previous_menu(Menus.main_menu)
        elif choice == 2:
            Menus.players_list_menu()
            Menus.previous_menu(Menus.main_menu)
        elif choice == 3:
            Menus.loading_tournament_menu()
        elif choice == 4:
            Menus.creation_tournament_menu()
        elif choice == 5:
            player_controller.\
                PlayersDeserializer.change_rank_player(w.players_table)
            Menus.previous_menu(Menus.main_menu)
        elif choice == 6:
            quit()

    @staticmethod
    def creation_tournament_menu():
        """Launches second_menu with
        writer_data_tournament in argument."""
        Menus.second_menu(w.writer_data_tournament())

    @staticmethod
    def loading_tournament_menu():
        """Launches second_menu with
        tournaments_list in argument."""
        Menus.second_menu(
            tournament_controller.LoadingTournament.tournaments_list())

    @staticmethod
    def choice_second_menu(choice_list, choice):
        """Allows to view info on tournament,
        or view players of tournament,
        or view all players, or add a player in tournament,
        or pick a player existing in the list,
        or change rank for player, or quit the tournament,
        or quit the software.
        Returns choice.
        """
        while choice not in choice_list:
            menu = input(
                "\n1 - Affichez les informations sur le tournoi en cours.\n"
                "2 - Affichez la liste des joueurs"
                " du tournoi avec les points totaux.\n"
                "3 - Affichez la liste de tous les joueurs déjà enregistrés.\n"
                "4 - Entrez un joueur.\n"
                "5 - Ou choississez un joueur"
                " présent dans le classement général.\n"
                "6 - Modifiez le classement d'un joueur.\n"
                "7 - Quittez le tournoi.\n"
                "8 - Quittez le programme.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()
        return choice

    @staticmethod
    def second_menu(tournament_name=""):
        """ gets choice from choice_second_menu and execute
        the matching choice.
        Launches view_total_players_message and
         tournament_start_menu.
        """
        choice = 0
        choice_list = [1, 2, 3, 4, 5, 6, 7, 8]
        length_players_list_id = (
            player_controller.PlayersSerializer.
            length_players_list_id(tournament_name)
            )
        number_players = player_controller.PlayersSerializer.number_players()

        if length_players_list_id == 8:
            menus_view.Menu.view_number_players_complete(
                length_players_list_id, number_players
            )
        else:
            menus_view.Menu.view_number_players(
                length_players_list_id, number_players)
        while length_players_list_id != number_players:
            choice = Menus.choice_second_menu(choice_list, choice)

            if choice == 1:
                tournament_controller.TournamentDeserializer.info_tournament(
                    tournament_name
                )
                Menus.previous_menu(
                    Menus.choice_second_menu(choice_list, choice))
            elif choice == 2:
                menu = Menus()
                menu.players_list_tournament_menu(tournament_name)
                menu.previous_menu(menu.second_menu, tournament_name)
            elif choice == 3:
                menu = Menus()
                menu.players_list_menu()
                Menus.previous_menu(
                    Menus.choice_second_menu(choice_list, choice))
            elif choice == 4:
                w.players_number(tournament_name)
                write = w.writer_players_in_list(tournament_name)
                if write:
                    length_players_list_id += 1
            elif choice == 5:
                w.players_number(tournament_name)
                player_controller.PlayersDeserializer.choose_player_in_rank(
                    tournament_name
                )
                Menus.previous_menu(Menus.second_menu, tournament_name)
            elif choice == 6:
                player_controller.PlayersDeserializer.change_rank_player(
                    w.players_table
                )
                Menus.previous_menu(Menus.second_menu, tournament_name)
            elif choice == 7:
                Menus.main_menu()
            elif choice == 8:
                quit()

            choice = 0
        player_view.ShowPlayer.view_total_players_message()
        Menus.tournament_start_menu(tournament_name)

    @staticmethod
    def tournament_start_menu(name_tournament=""):
        """Allows to view info on tournament,
        or view players of tournament,
        or view all matches from tournament, or view all players,
        or launch a round, or change rank for player,
        or quit the tournament, or quit the software.
        Launches tournament_finished_menu.
        """
        tournament_name = name_tournament.upper().replace(" ", "_")
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == f"{tournament_name}"
        )
        date_end = data_tournament[0]["date_de_fin"]
        if date_end == "Le tournoi n'est pas encore fini.":
            round_name = round_controller.\
                EnterDataRound.round_name(tournament_name)
            choice = 0
            choice_list = [1, 2, 3, 4, 5, 6, 7, 8]

            while choice not in choice_list:
                menu = input(
                    "\nTapez un nombre correspondant"
                    " à un des choix proposés.\n"
                    "1 - Affichez les informations sur le tournoi en cours.\n"
                    "2 - Affichez la liste des joueurs "
                    "du tournoi avec les points totaux.\n"
                    "3 - Affichez tous les matchs du tournoi.\n"
                    "4 - Affichez la liste de tous"
                    " les joueurs déjà enregistrés.\n"
                    f"5 - Lancez le {round_name.replace('_',' ')}.\n"
                    "6 - Modifiez le classement d'un joueur.\n"
                    "7 - Quittez le tournoi.\n"
                    "8 - Quittez le programme.\n"
                )
                try:
                    choice = int(menu)
                except ValueError:
                    menus_view.Menu.error_not_number()

            if choice == 1:
                tournament_controller.TournamentDeserializer.info_tournament(
                    tournament_name
                )
                Menus.previous_menu(
                    Menus.tournament_start_menu, tournament_name)
            elif choice == 2:
                Menus.players_list_tournament_menu(tournament_name)
                Menus.previous_menu(
                    Menus.tournament_start_menu, tournament_name)
            elif choice == 3:
                round_controller.RoundDeserializer.all_matches_rounds(
                    tournament_name)
                Menus.previous_menu(
                    Menus.tournament_start_menu, tournament_name)
            elif choice == 4:
                Menus.players_list_menu()
                Menus.previous_menu(
                    Menus.tournament_start_menu, tournament_name)
            elif choice == 5:
                w.writer_data_start_round(tournament_name, round_name)
                w.writer_data_matches_round(tournament_name, round_name)
                w.writer_timestamp_start_round(tournament_name, round_name)
                round_view.ShowRound.view_round_work()
                round_controller.RoundDeserializer.show_matches_round(
                    tournament_name, round_name
                )
                w.writer_data_end_round(tournament_name, round_name)
                w.writer_rounds_name(tournament_name)
                w.writer_timestamp_end_round(tournament_name, round_name)
                Menus.enter_result_menu(tournament_name, round_name)
                number_round = int(round_name.replace("Round_", ""))
                if number_round >= 4:
                    Menus.continue_or_finish_menu(
                        number_round, tournament_name)
                else:
                    Menus.previous_menu(
                        Menus.tournament_start_menu, tournament_name)
            elif choice == 6:
                player_controller.PlayersDeserializer.change_rank_player(
                    w.players_table
                )
                Menus.previous_menu(
                    Menus.tournament_start_menu, tournament_name)
            elif choice == 7:
                Menus.main_menu()
            elif choice == 8:
                quit()

        Menus.tournament_finished_menu(tournament_name)

    @staticmethod
    def continue_or_finish_menu(number_round, tournament_name):
        """Gets number_round and tournament_name, and allows to
         launch another round or finish the tournament """
        choice = 0
        choice_list = [1, 2]
        while choice not in choice_list:
            menu = input(
                f"Vous avez fait {number_round} rounds."
                "\n1 - faire encore un autre round.\n"
                "2 - terminer le tournoi.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()

        if choice == 1:
            Menus.tournament_start_menu(tournament_name)
        elif choice == 2:
            w.writer_timestamp_end_tournament(tournament_name)
            Menus.tournament_finished_menu(tournament_name)

    @staticmethod
    def tournament_finished_menu(tournament_name):
        """Allows to view info on tournament, or view players of tournament,
        or view all matches from tournament, or view all players,
        or change rank for player, or quit the tournament,
        or quit the software.
        """
        choice = 0
        choice_list = [1, 2, 3, 4, 5, 6, 7]
        while choice not in choice_list:
            menu = input(
                "\nTapez un nombre correspondant"
                " à un des choix proposés.\n"
                "1 - Affichez les informations"
                " sur le tournoi en cours.\n"
                "2 - Affichez la liste des joueurs"
                " du tournoi avec les points totaux.\n"
                "3 - Affichez tous les matchs du tournoi.\n"
                "4 - Affichez la liste de tous"
                " les joueurs déjà enregistrés.\n"
                "5 - Modifiez le classement d'un joueur.\n"
                "6 - Quittez le tournoi.\n"
                "7 - Quittez le programme.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()

        if choice == 1:
            tournament_controller.TournamentDeserializer.info_tournament(
                tournament_name
            )
            Menus.previous_menu(
                Menus.tournament_finished_menu, tournament_name)
        elif choice == 2:
            Menus.players_list_tournament_menu(tournament_name)
            Menus.previous_menu(
                Menus.tournament_finished_menu, tournament_name)
        elif choice == 3:
            round_controller.RoundDeserializer.all_matches_rounds(
                tournament_name)
            Menus.previous_menu(
                Menus.tournament_finished_menu, tournament_name)
        elif choice == 4:
            Menus.players_list_menu()
            Menus.previous_menu(
                Menus.tournament_finished_menu, tournament_name)
        elif choice == 5:
            player_controller.PlayersDeserializer.change_rank_player(
                w.players_table)
            Menus.previous_menu(
                Menus.tournament_finished_menu, tournament_name)
        elif choice == 6:
            Menus.main_menu()
        elif choice == 7:
            quit()

    @staticmethod
    def enter_result_menu(tournament_name, round_name):
        """Gets tournament_name and round_name and sends them to
        enter_result_player."""
        round_controller.RoundDeserializer.enter_result_player(
            tournament_name, round_name
        )

    @staticmethod
    def end_round_menu(tournament_name):
        """Launches view_end_round() then previous_menu to go to
        tournament_start_menu."""
        round_view.ShowRound.view_end_round()
        Menus.previous_menu(Menus.tournament_start_menu, tournament_name)

    @staticmethod
    def players_list_tournament_menu(tournament_name):
        """Thanks to tournament_name, allows to show the players of tournament
         in different orders.
        Alphabetical or rank order or order points."""
        keys = (
            "nom",
            "prenom",
            "date_de_naissance",
            "sexe",
            "rang_dans_le_classement_general",
            "Points totaux du tournoi",
        )
        players_list_tournament = []
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == tournament_name)
        player_list_id = (data_tournament[0])["id_des_joueurs_et_points"]
        points_players = []

        for player in player_list_id:
            id_player = w.players_table.search(user.id_joueur == player[0])
            players_list_tournament.append(
                id_player[0]
            )
            point = player[1]
            point_players = {"Points totaux du tournoi": point}
            points_players.append(point_players)

        for data, point_player in zip(players_list_tournament, points_players):
            data.update(point_player)
        choice = 0
        choice_list = [1, 2, 3]
        while choice not in choice_list:
            menu = input(
                "\n1 - Liste des joueurs du tournoi"
                " en cours par ordre alphabéthique.\n"
                "2 - Liste des joueurs du tournoi"
                " en cours par ordre de classement.\n"
                "3 - Liste des joueurs du tournoi"
                " en cours par ordre de points.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()

        if choice == 1:
            player_controller.PlayersDeserializer.\
                players_list_order(
                    players_list_tournament,
                    player_controller.PlayersDeserializer.
                    key_order_alphabetical(),
                    keys)
        elif choice == 2:
            player_controller.PlayersDeserializer\
                .players_list_order(
                    players_list_tournament,
                    player_controller.
                    PlayersDeserializer.key_order_ranking(),
                    keys)
        elif choice == 3:
            player_controller.PlayersDeserializer.\
                players_list_order(
                    players_list_tournament,
                    player_controller.PlayersDeserializer.key_order_point(),
                    keys)

    @staticmethod
    def players_list_menu():
        """Allows to show the players list in different orders.
        Alphabetical or rank order."""
        keys = (
            "nom",
            "prenom",
            "date_de_naissance",
            "sexe",
            "rang_dans_le_classement_general",
        )
        choice = 0
        choice_list = [1, 2]
        while choice not in choice_list:
            menu = input(
                "\n1 - Liste du classement général des joueurs"
                " en cours par ordre alphabéthique.\n"
                "2 - Liste du classement général des joueurs"
                " en cours par ordre de classement.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()

        if choice == 1:
            player_controller.PlayersDeserializer.players_list_order(
                w.players_table,
                player_controller.
                PlayersDeserializer.key_order_alphabetical(), keys)
        elif choice == 2:
            player_controller.PlayersDeserializer.players_list_order(
                w.players_table,
                player_controller.PlayersDeserializer.key_order_ranking(),
                keys
            )

    @staticmethod
    def previous_menu(menu_back, tournament_name=""):
        """Allows thanks to menu_back to come back to
         the previous menu where we were in tape 1."""
        choice = 0
        choice_list = [1]
        while choice not in choice_list:
            menu = input("\nPour revenir au menu précédent, tapez 1.\n")
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()

        if choice == 1:
            if type(menu_back) == int:
                int(menu_back)
            else:
                try:
                    menu_back(tournament_name)
                except TypeError:
                    menu_back()
