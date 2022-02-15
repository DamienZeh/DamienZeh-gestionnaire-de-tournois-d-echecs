import random
from tinydb import Query
from model import models
from view import player_view
from controller import writer_data_controller as w

user = Query()


class MatchDeserializer:
    """Deserialization's methods for match data."""
    @staticmethod
    def create_pairs_players(tournament_name):
        """thanks to tournament_name, it generates matches of two players between
         eight players based on point and ranking.
        Returns first_list, second_list
        """
        list_players_sort_name = []
        tournament_table = w.tournament_table
        data_tournament = tournament_table.search(
            user.nom_tournoi == f"{tournament_name}"
        )
        id_players_list = (data_tournament[0])["id_des_joueurs_et_points"]

        for player in id_players_list:
            id_player = w.players_table.search(user.id_joueur == player[0])
            points = player[-1]
            (id_player[0])["points_tournoi"] = points
            list_players_sort_name.append(id_player[0])
        list_players_sort_name = sorted(
            list_players_sort_name,
            reverse=True,
            key=lambda score: (
                score["points_tournoi"],
                score["rang_dans_le_classement_general"],
            ),
        )

        first_list = list_players_sort_name[: (
                len(list_players_sort_name) // 2)]
        second_list = list_players_sort_name[(
                len(list_players_sort_name) // 2):]

        return first_list, second_list

    @staticmethod
    def id_pair_players(tournament_name):
        """Thanks to tournament_name and first_list and second_list,
        its gets Lastnames and firstname for each players.
        Returns first_list, second_list
        """
        first_list, second_list = MatchDeserializer.create_pairs_players(
            tournament_name
        )
        id_first_list = []
        id_second_list = []

        for player in first_list:
            lastname = player.get("nom")
            firstname = player.get("prenom")
            id = lastname + " " + firstname
            id_first_list.append(id)

        for player in second_list:
            lastname = player.get("nom")
            firstname = player.get("prenom")
            id = lastname + " " + firstname
            id_second_list.append(id)
        return id_first_list, id_second_list

    @staticmethod
    def random_matches(list_matches):
        """Thanks to list_matches, it generates randomly matches.
        Returns random_match
        """
        random_players = []

        for match in list_matches:
            random_players.extend(match)
        random.shuffle(random_players)
        random_match = []

        for player in random_players:
            random_match.append([player])
        random_match[0] = random_match[0] + random_match[1]
        random_match[1] = random_match[2] + random_match[3]
        random_match[2] = random_match[4] + random_match[5]
        random_match[3] = random_match[6] + random_match[7]
        random_match = random_match[:4]

        return random_match

    @staticmethod
    def gen_new_matches_old_matches(tournament_name):
        """Thanks to tournament_name and first_list and second_list,
        its creates a list of new matches and a list
         of old matches(and matches inverse).
        Returns new_matches, old_matches_and_inverse
        """
        first_list, second_list = MatchDeserializer.id_pair_players(
            tournament_name)
        data_tournament = w.tournament_table.search(
            user.nom_tournoi == tournament_name)
        id_tournament = (data_tournament[0])["id_tournament"]
        data_round = w.round_table.search(
            user.id_round_tournoi == id_tournament)
        new_matches = []
        old_matches_list = []

        for player in zip(first_list, second_list):
            new_matches.append([player[0], player[1]])

        for data in data_round:
            if "match 1" in data.keys():
                first_match = data["match 1"]
                second_match = data["match 2"]
                third_match = data["match 3"]
                fourth_match = data["match 4"]
                old_matches_list.extend(
                    [
                        [(first_match[0])[0], (first_match[1])[0]],
                        [(second_match[0])[0], (second_match[1])[0]],
                        [(third_match[0])[0], (third_match[1])[0]],
                        [(fourth_match[0])[0], (fourth_match[1])[0]],
                    ]
                )
        old_matches_inversed = []
        for matches in old_matches_list:
            old_matches_inversed.append(matches[::-1])
        old_matches_and_inverse = old_matches_list + old_matches_inversed
        return new_matches, old_matches_and_inverse

    @staticmethod
    def check_and_change_order_list_players(tournament_name, round_name):
        """gets old matches thanks to round_name and tournament_name.
        And it prevents repeating the same matches.
        Returns first_list and second_list
        """
        (
            new_matches,
            old_matches_and_inverse,
        ) = MatchDeserializer.gen_new_matches_old_matches(
            tournament_name)

        try:
            rep_match_list = [
                x for x in old_matches_and_inverse if x in new_matches]
            rep_match = []
            rep_match.extend(rep_match_list[0])
            index_sup = 1
            repeat = 1

            while rep_match_list and repeat != 7:
                rep_match_list = [
                    x for x in old_matches_and_inverse if x in new_matches
                ]
                rep_match = []
                rep_match.extend(rep_match_list[0])
                index_player_to_move = new_matches.index(rep_match)
                if (
                    index_player_to_move == 3
                ):
                    new_matches[2], new_matches[3] = \
                        new_matches[3], new_matches[2]

                if index_player_to_move < 3:
                    next_match = new_matches[index_player_to_move + index_sup]
                    player_two_wrong_match = rep_match[1]
                    player_one_next_match = next_match[0]
                    rep_match[1] = player_one_next_match
                    new_matches[index_player_to_move] = rep_match
                    next_match[0] = player_two_wrong_match
                    new_matches[index_player_to_move + index_sup] = next_match

                    if rep_match_list:
                        next_match = \
                            new_matches[index_player_to_move + index_sup]
                        player_two_wrong_match = rep_match[1]
                        player_one_next_match = next_match[1]
                        rep_match[1] = player_one_next_match
                        new_matches[index_player_to_move] = rep_match
                        next_match[1] = player_two_wrong_match
                        new_matches[
                            index_player_to_move + index_sup] = next_match

                repeat += 1
            number_trial = 0

            while rep_match_list and number_trial < 200:
                new_matches = MatchDeserializer.random_matches(new_matches)
                rep_match_list = [
                    x for x in old_matches_and_inverse if x in new_matches
                ]
                number_trial += 1
        except IndexError:
            pass

        first_list = []
        second_list = []

        for match in new_matches:
            first_list.append(match[0])
            second_list.append(match[1])
        player_view.ShowPlayer.show_pair_players_match(
            first_list, second_list, round_name
        )
        return first_list, second_list


class Results:
    """It gets result of the match"""
    @staticmethod
    def random_result():
        """Its gets randomly a result
        Returns random.choice(results)
        """
        results = [[0.0, 1.0], [0.5, 0.5], [1.0, 0.0]]
        return random.choice(results)


class MatchesSerializer:
    """serialization's method for match data."""
    @staticmethod
    def matches_serializer(tournament_name, round_name):
        """It serializes matches_round.
        Returns serialized_matches
        """
        serialized_matches = []
        data_matches = CreateMatch(
        ).create_matches_round(tournament_name, round_name)
        serialized_matches.append(data_matches)
        return serialized_matches


class CreateMatch(models.Match):
    """It inherits from the model Match"""
    def __init__(self):
        """It initializes in the class"""
        super().__init__(self)

    def create_matches_round(self, tournament_name, round_name):
        """It creates dictionary matches_round with inside match
         (with inside point_first_player, point_second_player).
         Returns matches_round.
        """
        (
            id_first_list,
            id_second_list,
        ) = MatchDeserializer.check_and_change_order_list_players(
            tournament_name, round_name
        )
        self.first_player = id_first_list
        self.second_player = id_second_list
        self.match_number = len(self.first_player)
        self.i = 0
        self.matches_round = {}
        while self.i != self.match_number:
            self.result = Results.random_result()
            self.result_first_player = self.result[0]
            self.result_second_player = self.result[1]
            self.match = []
            self.point_first_player = []
            self.point_first_player = [
                self.first_player[self.i],
                self.result_first_player,
            ]
            self.point_second_player = []
            self.point_second_player = [
                self.second_player[self.i],
                self.result_second_player,
            ]
            self.match = self.point_first_player, self.point_second_player
            self.i += 1
            self.matches_round[f"match {self.i}"] = self.match
        return self.matches_round
