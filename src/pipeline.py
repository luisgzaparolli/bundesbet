from src.commentary_game.pipeline import update as update_commentary
from src.stats_games.pipeline import update as update_gamestats


def main():
    """
    This functions check and if is necessary update data set's
    """
    #update_commentary()
    update_gamestats()


if __name__ == '__main__':
    main()

