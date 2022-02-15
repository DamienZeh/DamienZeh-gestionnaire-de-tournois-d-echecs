from controller import player_controller


class ShowPlayer:
    @staticmethod
    def view_player_already_exist():
        """view message player already exist"""
        print("Vous avez déja entré ce joueur")

    @staticmethod
    def view_player_not_exist():
        """view message player not exist"""
        print("Ce joueur n'existe pas, dans la liste.")

    @staticmethod
    def view_enter_player(number_players_entered, number_players):
        """view message enter player x on x"""
        print(f"Entrez le joueur n° : "
              f"{number_players_entered} sur {number_players} : ")

    @staticmethod
    def view_player_already_exist_tournament():
        """view message player already exist tournament"""
        print(
            "Cette personne est déjà enregistrée"
            " dans la liste des joueurs du tournoi."
        )

    @staticmethod
    def view_player_not_copy_already_exist_ranking():
        """view message player not copy already exist ranking"""
        print(
            "Ce joueur existe déjà dans le classement général,\n"
            "Vous ne pouvez donc pas le créer , importez"
            " le plutôt avec le choix 5 du menu."
        )

    @staticmethod
    def view_player_already_exist_ranking():
        """view message player already exist ranking"""
        print(
            "Cette personne est déjà enregistrée"
            " dans le classement général(hors tournoi en cours)."
        )

    @staticmethod
    def view_error_not_int():
        """view_message_error_not_int"""
        print("Erreur, veuillez taper des lettres")

    @staticmethod
    def view_error_not_str():
        """view message error not str"""
        print("Erreur, veuillez taper"
              " un chiffre(un point, pas de virgule")

    @staticmethod
    def view_error_not_str_not_float():
        """view message error not str not float"""
        print("Erreur, veuillez taper un nombre entier")

    @staticmethod
    def view_error_sex():
        """view message error sex"""
        print("Erreur, veuillez taper 'H','F', ou 'X'")

    @staticmethod
    def view_error_date():
        """view message error date"""
        print("Erreur. Veuillez taper une date (xx/xx/xxxx).")

    @staticmethod
    def view_player(players_list_deserializer):
        """view players"""
        print(players_list_deserializer)

    @staticmethod
    def view_all_players_already_here(number_players_entered):
        """view message all players already here"""
        print(f"Vous avez déjà les {number_players_entered}")

    @staticmethod
    def view_total_players_message():
        """view message total players message"""
        print("Vous avez rentré tous"
              " les joueurs. Les joueurs sont prêts.")

    @staticmethod
    def view_none_player():
        """view message none player"""
        print("Il n'y a pas encore de joueurs dans cette liste.")

    @staticmethod
    def view_player_clean(player_clean):
        """view player clean"""
        print(player_clean)

    @staticmethod
    def view_player_wrong_name():
        """view message player wrong name"""
        print("erreur: Personne n'a ce nom et/ou prénom")

    @staticmethod
    def view_new_player(checkName):
        """view new player entered"""
        sentence = f"Vous avez ajouté : {checkName} en joueur"
        clean_sentence = (
            sentence.replace("{", "")
            .replace("}", "")
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
        ).replace("_", " ")
        return print(clean_sentence)

    @staticmethod
    def view_player_change_rank(lastname, firstname, rank):
        """view player change rank"""
        print(
            f"{lastname} {firstname} "
            f"à bien la position {rank}, au classement général. "
            )

    @staticmethod
    def view_player_change_point(lastname, firstname, point, total_point):
        """view message player change point"""
        print(
            f"{lastname} {firstname} à bien {point} point pour ce match.\n"
            f"Ce qui lui fait pour l'instant"
            f" un total de {total_point} point(s) dans ce tournoi.\n"
            )

    @staticmethod
    def show_pair_players_match(first_list, second_list, round_name):
        """view show pair players match"""
        print(f"\nVoici les matchs prévus"
              f" pour le {round_name.replace('_',' ')} :")
        for first_list, second_list in zip(first_list, second_list):
            print(f"{first_list} --contre -- {second_list}.")

    @staticmethod
    def point_player(match_index, players_table, matches, tournament_name):
        """View point player for all players"""
        print("\nEntrez les résultats")
        matches_list = []
        matches_list.extend(
            [
                matches["match 1"],
                matches["match 2"],
                matches["match 3"],
                matches["match 4"],
            ]
        )
        for item in matches_list:
            match = matches[f"match {match_index}"]
            for player in match:
                print(f"{player[0]}"
                      f" (le simulateur lui donne : {player[1]} point).")
                player_controller.PlayersDeserializer.change_point_player(
                    players_table, player[0], tournament_name
                )
            match_index += 1
