class Menu:
    @staticmethod
    def view_welcome_main_menu():
        """view message welcome main menu"""
        print("\nBienvenue dans ce gestionnaire de tournois d'échecs")

    @staticmethod
    def view_show_choices_main_menu():
        """view show choices main menu"""
        print(
            "Menu\n1 - Entrer les joueurs\n2 - Charger un tournoi en cours\
                    \n3 - Afficher le classement général des joueurs"
        )

    @staticmethod
    def error_wrong_number():
        """view message error wrong number"""
        print(
            "ERREUR: tapez un nombre correspondant à"
            " un des choix proposés. Réessayez."
        )

    @staticmethod
    def error_not_number():
        """view message error not number"""
        print("ERREUR: Vous devez rentrer un nombre. Réessayez.")

    @staticmethod
    def view_number_players_complete(length_players_list_id, number_players):
        """view number players"""
        print(f"{length_players_list_id}"
              f" joueur(s) sur {number_players} de prêt(s) .")

    @staticmethod
    def view_number_players(length_players_list_id, number_players):
        """view number players ready"""
        print(
            f"\nVous devez avoir {number_players} joueurs pour le tournoi.\n"
            f"Faites votre choix : "
            f"{length_players_list_id}"
            f" joueur(s) sur {number_players} de prêt(s) ."
        )
