from controller import menus_controller


def main():
    """Allows launch all software"""
    launch = menus_controller.Menus
    launch.welcome_menu()


if __name__ == "__main__":
    main()
