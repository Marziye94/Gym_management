from gym.application import create_application
from gym.menus.main_menu import main_menu


def main():
    application = create_application()
    main_menu(application)


if __name__ == "__main__":
    main()
