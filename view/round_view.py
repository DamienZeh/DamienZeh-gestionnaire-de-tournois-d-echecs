from controller import round_controller
import time


class ShowRound:
    @staticmethod
    def view_error_hour():
        print("Entrez une heure.\n")

    @staticmethod
    def view_round_end():
        print("\nLe round est terminé.")

    @staticmethod
    def view_none_round():
        print("\nIl n'y a pas de matchs, ni de rounds pour le moment.")

    @staticmethod
    def view_round_work():
        print("\nLancement du round...")
        time.sleep(2)
        input("Appyuez sur une touche quand le round est terminé...")
        print("...round terminé.\n")
        time.sleep(1)
        print("Et voici les résultats de la simulation, de ce round :")

    @staticmethod
    def view_matches_round(matches):
        print()
        try:
            print(f'nom du round :{matches["nom_du_round"]}')
            print(f'date de debut :{matches["date_debut_round"]}')
            print(f'date de fin :{matches["date_fin_round"]}')
        except:
            pass
        match_index = 1
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
            match = f"match {match_index}"
            list_data = f"{match}: {item}"
            list_data_clean = (
                list_data.replace("{", "")
                .replace("}", "")
                .replace("'", "")
                .replace("[", "")
                .replace("]", "")
            )
            print(list_data_clean)
            match_index += 1

    @staticmethod
    def view_end_round():
        print("Ce round est fini, et les points de matchs ont été rentré.\n")

    @staticmethod
    def view_timestamp_end(timestamp):
        print(f"date et heure de fin du round :{timestamp}")
