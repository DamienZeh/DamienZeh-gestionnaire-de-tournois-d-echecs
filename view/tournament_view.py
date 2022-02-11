import time


class ShowTournament:
    @staticmethod
    def view_error_empty():
        print("Erreur, veuillez taper quelque chose.\n")

    @staticmethod
    def view_none_tournament():
        print("Il n'y a aucun tournoi de créé, retour au menu principal.")

    @staticmethod
    def view_all_tournaments(tournaments_list):
        print(f"Vous avez {len(tournaments_list)} tournoi(s) dans la liste :")
        new_tournaments_list = []
        for tournament in tournaments_list:
            tournaments_list_clean = (
                tournament.replace("[", "").replace("]", "").replace(".json", "")
            )
            new_tournaments_list.append(tournaments_list_clean)
            print(tournaments_list_clean)
        return new_tournaments_list

    @staticmethod
    def view_tournament_name_choose(name_tournament):
        print(f"Vous avez choisi le tournoi : {name_tournament}")

    @staticmethod
    def view_tournament_not_exist():
        print("Ce tournoi n'existe pas, retour au menu principal.")

    @staticmethod
    def view_tournament_already_exist(tournament_name):
        print(f"Le tournoi {tournament_name} existe déjà, retour au menu principal.")

    @staticmethod
    def view_info_tournament(
        tournament_name,
        place,
        start_date,
        round_number,
        time_control,
        description,
        end_date,
    ):
        print(f"nom_tournoi : {tournament_name}")
        print(f"endroit : {place}")
        print(f"date_de_debut : {start_date}")
        print(f"rounds_finis : {round_number}")
        print(f"mode : {time_control}")
        print(f"description : {description}")
        print(f"date_de_fin : {end_date}")

    @staticmethod
    def view_timestamp_start_tournament(timestamp):
        print(f"date et heure du debut du tournoi :{timestamp}")

    @staticmethod
    def finish_tournament(timestamp):
        print(
            f"Le tournoi s'est terminé au :{timestamp},\n"
            f"Rentrez les nouveaux score du classement(choix 5),\n"
            "en fonction des points et du classement actuel des joueurs(choix 2)."
        )
