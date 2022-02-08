from controller import player_controller


class ShowPlayer:
    @staticmethod
    def view_player_already_exist():
        print("Vous avez déja entré ce joueur")

    @staticmethod
    def view_enter_player(number_players_entered, number_players):
        print(f"Entrez le joueur n° : {number_players_entered} sur {number_players} : ")

    @staticmethod
    def view_player_already_exist_tournament():
        print(
            "Cette personne est déjà enregistrée dans la liste des joueurs du tournoi."
        )

    @staticmethod
    def view_player_already_exist_ranking():
        print(
            "Cette personne est déjà enregistrée  dans la liste des joueurs(hors tournoi en cours)."
        )

    @staticmethod
    def view_error_not_int():
        print("Erreur, veuillez taper des lettres")

    @staticmethod
    def view_error_not_str():
        print("Erreur, veuillez taper un chiffre")

    @staticmethod
    def view_error_sex():
        print("Erreur, veuillez taper 'H','F', ou 'X'")

    @staticmethod
    def view_error_date():
        print("Erreur. Veuillez taper une date (xx/xx/xxxx).")

    @staticmethod
    def view_player(players_list_deserializer):
        print(players_list_deserializer)

    @staticmethod
    def view_all_players_already_here(number_players_entered):
        print(f"Vous avez déjà les {number_players_entered}")

    @staticmethod
    def view_total_players_message():
        print("Vous avez rentré tous les joueurs. Les joueurs sont prêts.")

    @staticmethod
    def view_none_player():
        print("Il n'y a pas encore de joueurs dans cette liste.")

    @staticmethod
    def view_player_clean(player_clean):
        print(player_clean)

    @staticmethod
    def view_player_wrong_name():
        print("erreur: Personne n'a ce nom et/ou prénom")

    @staticmethod
    def view_new_player_in_ranking(checkName):
        sentence = f"Vous avez ajouté : {checkName}, en joueur"
        clean_sentence = (
            sentence.replace("{", "")
            .replace("}", "")
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
        )
        return print(clean_sentence)

    @staticmethod
    def view_player_change_rank(lastname, firstname, rank):
        print(
            f"{lastname} {firstname} à bien la position {rank}, au classement général. "
        )

    @staticmethod
    def view_player_change_point(lastname, firstname, point, total_point):
        print(
            f"{lastname} {firstname} à bien {point} point pour ce match.\n"
            f"Ce qui lui fait pour l'instant un total de {total_point} point(s) dans ce tournoi.\n"
        )

    @staticmethod
    def show_pair_players_match(first_list, second_list, round_name):
        print(f"\nVoici les matchs prévus pour le {round_name.replace('_',' ')} :")
        for first_list, second_list in zip(first_list, second_list):
            print(f"{first_list} --contre -- {second_list}.")

    @staticmethod
    def point_player(match_index, players_table, matches, tournament_name):
        print("\nEntrez les résultats")
        del matches["id_round_tournoi"]
        del matches["nom_du_round"]
        del matches["date_debut_round"]
        del matches["date_fin_round"]
        for item in matches:
            match = matches[f"match {match_index}"]
            for player in match:
                print(f"{player[0]} (le simulateur lui donne : {player[1]} point).")
                player_controller.PlayersDeserializer.change_point_player(
                    players_table, player[0], tournament_name
                )
            match_index += 1
