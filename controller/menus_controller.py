import view.player_view
from view import menus_view, tournament_view, round_view
from controller import (
    player_controller,
    tournament_controller,
    writer_data_controller,
    match_controller,
    round_controller,
)
from view import player_view
from tinydb import TinyDB, Query
import itertools

user = Query()
tournament_table = writer_data_controller.tournament_table
players_table = writer_data_controller.players_table


class Menus:
    @staticmethod
    def welcome_menu():
        menus_view.Menu.view_welcome_main_menu()
        Menus.main_menu()

    @staticmethod
    def main_menu():
        choice = 0
        choice_list = [1, 2, 3, 4, 5, 6]
        while choice not in choice_list:
            menu = input(
                "\nMenu principal\nTapez un nombre correspondant à un des choix proposés.\n"
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
            Menus.previous_menu_without_parameter(Menus.main_menu)
        elif choice == 2:
            Menus.players_list_menu()
            Menus.previous_menu_without_parameter(Menus.main_menu)
        elif choice == 3:
            Menus.loading_tournament_menu()
        elif choice == 4:
            Menus.creation_tournament_menu()
        elif choice == 5:
            player_controller.PlayersDeserializer.change_rank_player(players_table)
            Menus.previous_menu_without_parameter(Menus.main_menu)
        elif choice == 6:
            quit()

    @staticmethod
    def creation_tournament_menu():
        Menus.second_menu(writer_data_controller.writer_data_tournament())

    @staticmethod
    def loading_tournament_menu():
        Menus.second_menu(tournament_controller.LoadingTournament.tournaments_list())

    @staticmethod
    def choice_second_menu(choice_list, choice):
        while choice not in choice_list:
            menu = input(
                "\n1 - Affichez les informations sur le tournoi en cours.\n"
                "2 - Affichez la liste des joueurs du tournoi avec les points totaux.\n"
                "3 - Affichez la liste de tous les joueurs déjà enregistrés.\n"
                "4 - Entrez un joueur.\n"
                "5 - Ou choississez un joueur présent dans le classement général.\n"
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
        choice = 0
        choice_list = [1, 2, 3, 4, 5, 6, 7, 8]
        length_players_list_id = (
            player_controller.PlayersSerializer.length_players_list_id(tournament_name)
        )
        number_players = player_controller.PlayersSerializer.number_players()
        if length_players_list_id == 8:
            menus_view.Menu.view_number_players_complete(
                length_players_list_id, number_players
            )
        else:
            menus_view.Menu.view_number_players(length_players_list_id, number_players)
        while length_players_list_id != number_players:
            choice = Menus.choice_second_menu(choice_list, choice)
            if choice == 1:
                tournament_controller.TournamentDeserializer.info_tournament(
                    tournament_name
                )

                Menus.previous_menu_with_parameters(
                    Menus.choice_second_menu(choice_list, choice)
                )
            elif choice == 2:
                menu = Menus()
                menu.players_list_tournament_menu(tournament_name)
                menu.previous_menu_with_parameter_name(
                    menu.second_menu, tournament_name
                )
            elif choice == 3:
                menu = Menus()
                menu.players_list_menu()
                Menus.previous_menu_with_parameters(
                    Menus.choice_second_menu(choice_list, choice)
                )
            elif choice == 4:
                writer_data_controller.players_number(tournament_name)
                write = writer_data_controller.writer_players_in_list(tournament_name)
                if write:
                    length_players_list_id += 1
            elif choice == 5:
                player_controller.PlayersDeserializer.choose_player_in_rank(
                    tournament_name
                )
                Menus.previous_menu_with_parameter_name(
                    Menus.second_menu, tournament_name
                )
            elif choice == 6:
                player_controller.PlayersDeserializer.change_rank_player(players_table)
                Menus.previous_menu_with_parameter_name(
                    Menus.second_menu, tournament_name
                )
            elif choice == 7:
                Menus.main_menu()
            elif choice == 8:
                quit()
            choice = 0
        player_view.ShowPlayer.view_total_players_message()
        Menus.tournament_start_menu(tournament_name)

    @staticmethod
    def tournament_start_menu(tournament_name=""):
        data_tournament = tournament_table.search(
            user.nom_tournoi == f"{tournament_name}"
        )
        print(data_tournament)
        date_end = data_tournament[0]["date_de_fin"]
        print(date_end)
        if date_end == "Le tournoi n'est pas encore fini.":
            print("coucou")
            round_name = round_controller.EnterDataRound.round_name(tournament_name)
            choice = 0
            choice_list = [1, 2, 3, 4, 5, 6, 7, 8]
            while choice not in choice_list:
                menu = input(
                    "\nTapez un nombre correspondant à un des choix proposés.\n"
                    "1 - Affichez les informations sur le tournoi en cours.\n"
                    "2 - Affichez la liste des joueurs du tournoi avec les points totaux.\n"
                    "3 - Affichez tous les matchs du tournoi.\n"
                    "4 - Affichez la liste de tous les joueurs déjà enregistrés.\n"
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
                Menus.previous_menu_with_parameter_name(
                    Menus.tournament_start_menu, tournament_name
                )
            elif choice == 2:
                Menus.players_list_tournament_menu(tournament_name)
                Menus.previous_menu_with_parameter_name(
                    Menus.tournament_start_menu, tournament_name
                )
            elif choice == 3:
                round_controller.RoundDeserializer.all_matches_rounds(tournament_name)
                Menus.previous_menu_with_parameter_name(
                    Menus.tournament_start_menu, tournament_name
                )
            elif choice == 4:
                Menus.players_list_menu()
                Menus.previous_menu_with_parameter_name(
                    Menus.tournament_start_menu, tournament_name
                )
            elif choice == 5:

                writer_data_controller.writer_data_start_round(
                    tournament_name, round_name
                )
                writer_data_controller.writer_data_matches_round(
                    tournament_name, round_name
                )
                writer_data_controller.writer_timestamp_start_round(
                    tournament_name, round_name
                )
                round_view.ShowRound.view_round_work()
                round_controller.RoundDeserializer.show_matches_round(
                    tournament_name, round_name
                )
                writer_data_controller.writer_data_end_round(
                    tournament_name, round_name
                )
                writer_data_controller.writer_rounds_name(tournament_name)
                writer_data_controller.writer_timestamp_end_round(
                    tournament_name, round_name
                )
                Menus.enter_result_menu(tournament_name, round_name)
                number_round = int(round_name.replace("Round_", ""))
                if number_round >= 4:
                    Menus.continue_or_finish_menu(number_round, tournament_name)
                else:
                    Menus.previous_menu_with_parameter_name(
                        Menus.tournament_start_menu, tournament_name
                    )
            elif choice == 6:
                player_controller.PlayersDeserializer.change_rank_player(players_table)
                Menus.previous_menu_with_parameter_name(
                    Menus.tournament_start_menu, tournament_name
                )
            elif choice == 7:
                Menus.main_menu()
            elif choice == 8:
                quit()
        Menus.tournament_finished_menu(tournament_name)

    @staticmethod
    def continue_or_finish_menu(number_round, tournament_name):
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
            writer_data_controller.writer_timestamp_end_tournament(tournament_name)
            Menus.tournament_finished_menu(tournament_name)

    @staticmethod
    def tournament_finished_menu(tournament_name):
        choice = 0
        choice_list = [1, 2, 3, 4, 5, 6, 7]
        while choice not in choice_list:
            menu = input(
                "\nTapez un nombre correspondant à un des choix proposés.\n"
                "1 - Affichez les informations sur le tournoi en cours.\n"
                "2 - Affichez la liste des joueurs du tournoi avec les points totaux.\n"
                "3 - Affichez tous les matchs du tournoi.\n"
                "4 - Affichez la liste de tous les joueurs déjà enregistrés.\n"
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
            Menus.previous_menu_with_parameter_name(
                Menus.tournament_finished_menu, tournament_name
            )
        elif choice == 2:
            Menus.players_list_tournament_menu(tournament_name)
            Menus.previous_menu_with_parameter_name(
                Menus.tournament_finished_menu, tournament_name
            )
        elif choice == 3:
            round_controller.RoundDeserializer.all_matches_rounds(tournament_name)
            Menus.previous_menu_with_parameter_name(
                Menus.tournament_finished_menu, tournament_name
            )
        elif choice == 4:
            Menus.players_list_menu()
            Menus.previous_menu_with_parameter_name(
                Menus.tournament_finished_menu, tournament_name
            )
        elif choice == 5:
            player_controller.PlayersDeserializer.change_rank_player(players_table)
            Menus.previous_menu_with_parameter_name(
                Menus.tournament_finished_menu, tournament_name
            )
        elif choice == 6:
            Menus.main_menu()
        elif choice == 7:
            quit()

    @staticmethod
    def enter_result_menu(tournament_name, round_name):
        round_controller.RoundDeserializer.enter_result_player(
            tournament_name, round_name
        )

    @staticmethod
    def end_round_menu(tournament_name):
        round_view.ShowRound.view_end_round()
        Menus.previous_menu_with_parameter_name(
            Menus.tournament_start_menu, tournament_name
        )

    @staticmethod
    def players_list_tournament_menu(tournament_name):
        players_list_tournament = []
        data_tournament = tournament_table.search(user.nom_tournoi == tournament_name)
        player_list_id = (data_tournament[0])["id_des_joueurs_et_points"]
        points_players = []
        for player in player_list_id:
            id_player = players_table.search(user.id_joueur == player[0])
            players_list_tournament.append(
                id_player[0]
            )  # changer en 1 pour avoir les points
            point = player[1]
            point_players = {"Points totaux du tournoi": point}
            points_players.append(point_players)
        for data, point_player in zip(players_list_tournament, points_players):
            data.update(point_player)
            try:
                del data["id_joueur"]
            except KeyError:
                continue

        choice = 0
        choice_list = [1, 2, 3]
        while choice not in choice_list:
            menu = input(
                "\n1 - Liste des joueurs du tournoi en cours par ordre alphabéthique.\n"
                "2 - Liste des joueurs du tournoi en cours par ordre de classement.\n"
                "3 - Liste des joueurs du tournoi en cours par ordre de points.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()
        if choice == 1:
            player_controller.PlayersDeserializer.players_list_tournament_order(
                players_list_tournament,
                player_controller.PlayersDeserializer.key_order_alphabetical(),
            )
        elif choice == 2:
            player_controller.PlayersDeserializer.players_list_tournament_order(
                players_list_tournament,
                player_controller.PlayersDeserializer.key_order_ranking(),
            )
        elif choice == 3:
            player_controller.PlayersDeserializer.players_list_tournament_order(
                players_list_tournament,
                player_controller.PlayersDeserializer.key_order_point(),
            )

    @staticmethod
    def players_list_menu():
        choice = 0
        choice_list = [1, 2]
        while choice not in choice_list:
            menu = input(
                "\n1 - Liste du classement général des joueurs en cours par ordre alphabéthique.\n"
                "2 - Liste du classement général des joueurs en cours par ordre de classement.\n"
            )
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()
        if choice == 1:
            player_controller.PlayersDeserializer.players_list_order(
                players_table,
                player_controller.PlayersDeserializer.key_order_alphabetical(),
            )
        elif choice == 2:
            player_controller.PlayersDeserializer.players_list_order(
                players_table,
                player_controller.PlayersDeserializer.key_order_ranking(),
            )

    @staticmethod
    def previous_menu_without_parameter(menu_back):
        choice = 0
        choice_list = [1]
        while choice not in choice_list:
            menu = input("\nPour revenir au menu précédent, tapez 1.\n")
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()
        if choice == 1:
            menu_back()

    @staticmethod
    def previous_menu_with_parameter_name(menu_back, tournament_name=""):
        choice = 0
        choice_list = [1]
        while choice not in choice_list:
            menu = input("\nPour revenir au menu précédent, tapez 1.\n")
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()
        if choice == 1:
            menu_back(tournament_name)

    @staticmethod
    def previous_menu_with_parameters(menu_back):
        choice = 0
        choice_list = [1]
        while choice not in choice_list:
            menu = input("\nPour revenir au menu précédent, tapez 1.\n")
            try:
                choice = int(menu)
            except ValueError:
                menus_view.Menu.error_not_number()
        if choice == 1:
            menu_back
