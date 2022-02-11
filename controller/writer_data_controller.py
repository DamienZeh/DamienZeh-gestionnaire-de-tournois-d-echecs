from controller import (
    player_controller,
    tournament_controller,
    menus_controller,
    round_controller,
    match_controller,
)
from view import player_view, tournament_view, round_view
from tinydb import TinyDB, Query
import re

user = Query()
database_manager = TinyDB("database_manager.json", indent=4)
tournament_table = database_manager.table("tournaments")
round_table = database_manager.table("rounds")
players_table = database_manager.table("players")


def writer_data_tournament():
    tournament_serializer = (
        tournament_controller.TournamentSerializer.tournament_serializer()
    )
    name = ""
    for data in tournament_serializer:
        name = data["nom_tournoi"]
    names_list = tournament_controller.TournamentDeserializer.all_tournaments_name()
    if name not in names_list:
        tournament_table.insert_multiple(tournament_serializer)
        writer_timestamp_start_tournament(name)
    else:
        tournament_view.ShowTournament.view_tournament_already_exist(name)
    return name


def writer_data_start_round(tournament_name, round_name):
    start_round_serializer = round_controller.RoundSerializer.round_start_serializer(
        tournament_name, round_name
    )
    round_table.insert_multiple(start_round_serializer)


def writer_data_matches_round(tournament_name, round_name):
    matches_round_serializer = match_controller.MatchesSerializer.matches_serializer(
        tournament_name, round_name
    )
    data_tournament = tournament_table.search(user.nom_tournoi == f"{tournament_name}")
    id_tournament = (data_tournament[0])["id_tournament"]
    round_table.update(
        (matches_round_serializer[0]),
        (user.nom_du_round == f"{round_name}")
        & (user.id_round_tournoi == id_tournament),
    )


def writer_data_end_round(tournament_name, round_name):
    end_round_serializer = round_controller.RoundSerializer.round_end_serializer(
        tournament_name, round_name
    )
    data_tournament = tournament_table.search(user.nom_tournoi == f"{tournament_name}")
    id_tournament = (data_tournament[0])["id_tournament"]
    round_table.update(
        (end_round_serializer[0]),
        (user.nom_du_round == f"{round_name}")
        & (user.id_round_tournoi == id_tournament),
    )


def writer_rounds_name(tournament_name):
    rounds_name = round_controller.RoundDeserializer.all_rounds(tournament_name)
    str_rounds_name = (
        (str(rounds_name)).replace("[", "").replace("]", "").replace("'", "")
    )
    tournament_table.update(
        {"rounds_finis": str_rounds_name},
        user.nom_tournoi == f"{tournament_name}",
    )


def writer_timestamp_start_round(tournament_name, round_name):
    timestamp = tournament_controller.DataTournament.timestamp()
    data_tournament = tournament_table.search(user.nom_tournoi == f"{tournament_name}")
    id_tournament = (data_tournament[0])["id_tournament"]
    round_table.update(
        {"date_debut_round": timestamp},
        (user.nom_du_round == f"{round_name}")
        & (user.id_round_tournoi == id_tournament),
    )


def writer_timestamp_end_round(tournament_name, round_name):
    timestamp = tournament_controller.DataTournament.timestamp()
    round_view.ShowRound.view_timestamp_end(timestamp)
    data_tournament = tournament_table.search(user.nom_tournoi == f"{tournament_name}")
    id_tournament = (data_tournament[0])["id_tournament"]
    round_table.update(
        {"date_fin_round": timestamp},
        (user.nom_du_round == f"{round_name}")
        & (user.id_round_tournoi == id_tournament),
    )


def writer_timestamp_start_tournament(tournament_name):
    timestamp = tournament_controller.DataTournament.timestamp()
    tournament_view.ShowTournament.view_timestamp_start_tournament(timestamp)
    tournament_table.update(
        {"date_de_debut": timestamp}, (user.nom_tournoi == f"{tournament_name}")
    )


def writer_timestamp_end_tournament(tournament_name):
    timestamp = tournament_controller.DataTournament.timestamp()
    tournament_view.ShowTournament.finish_tournament(timestamp)
    tournament_table.update(
        {"date_de_fin": timestamp}, (user.nom_tournoi == f"{tournament_name}")
    )


def writer_players_in_list(tournament_name):
    players_serializer = player_controller.PlayersSerializer.players_serializer()
    point_start = 0.0
    player = players_serializer[0]
    lastname = player["nom"]
    firstname = player["prenom"]
    ids = f"{lastname} {firstname}"
    id_lastname_firstname = (
        player_controller.PlayersDeserializer.compare_id_lastname_firstname(
            lastname, firstname
        )
    )
    data_tournament = tournament_table.search(user.nom_tournoi == f"{tournament_name}")
    id_players_list_with_point = (data_tournament[0])["id_des_joueurs_et_points"]
    id_players_list = []
    for id in id_players_list_with_point:
        id_players_list.append(id[0])
    id_player_with_point = [player["id_joueur"], point_start]
    no_existing = ""
    id_players_table_list = []
    for id_player in players_table.all():
        id_players_table_list.append(id_player["id_joueur"])
    if (
        id_lastname_firstname not in id_players_list
        and id_lastname_firstname not in id_players_table_list
    ):
        id_players_list_with_point.append(id_player_with_point)
        tournament_table.update(
            {"id_des_joueurs_et_points": id_players_list_with_point},
            user.nom_tournoi == f"{tournament_name}",
        )
        player_view.ShowPlayer.view_new_player(ids)
        players_table.insert_multiple(players_serializer)
        no_existing = True
    elif (
        id_lastname_firstname in id_players_list
        and id_lastname_firstname in id_players_table_list
    ):
        player_view.ShowPlayer.view_player_already_exist_tournament()
    elif id_lastname_firstname in id_players_table_list:
        player_view.ShowPlayer.view_player_not_copy_already_exist_ranking()
    return no_existing


def players_number(tournament_name):
    number_entered = player_controller.PlayersSerializer.number_players_entered(
        tournament_name
    )
    players_number = player_controller.PlayersSerializer.number_players()
    player_view.ShowPlayer.view_enter_player(number_entered, players_number)
