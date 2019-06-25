import logging

logger = logging.getLogger("le2m.srvgroup")


class Group:
    def __init__(self, le2msrv, uid, players=None):
        self.le2msrv = le2msrv
        self.uid = uid
        self.session_id = self.le2msrv.gestionnaire_base.session.id
        self._players = players

    def add_players(self, players):
        self._players = players

    def add_player(self, player):
        self._players.append(player)

    def get_players(self):
        return self._players

    def get_player_by_place(self, place):
        """
        Return the player at the given place
        :param place:
        :return: a player
        """
        try:
            return self._players[place]
        except IndexError:
            logger.warning("IndexError, place: {}".format(place))
            return None

    def get_place_of_player(self, player):
        """
        Return the place of the given player in the group
        :param player:
        :return: an integer
        """
        try:
            return self._players.index(player)
        except ValueError:
            logger.warning("ValueError, player: {}".format(player))
            logger.debug("Group's players: {}".format(self.get_players()))
            return None

    def __str__(self):
        return "G{}".format(self.uid.split("_")[2])
