__author__ = 'Patrick O\'Brien'
''' COPYRIGHT 2014
    This file is part of lolPy.

    lolPy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lolPy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lolPy.  If not, see <http://www.gnu.org/licenses/>.
'''
import time

import requests

from riot import *
from riot.Constants import *
from riot.Constants.RiotException import RiotException


DEBUG = True


class Client(object):
    """
    Client opens up connections between Python and RiotGames' API for League of Legends. It maps Json Objects from Riot
    into custom Python classes for easier management and use.
    """
    def __init__(self, username, region: str, api_key: str):
        self.__check_api_key(api_key)
        self._username = username
        self._region = region
        self._key = api_key
        self._player = None
        self.__search_for_player()

    @property
    def _champion_data(self):
        payload = {"api_key": self._key, "dataById": True}
        url = (urls.base + urls.champion_data).format(region=self._region)

        r = requests.get(url, params=payload)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            return self._champion_data
        if not self.__api_service_check(r):
            return []

        data = r.json()
        raw_champs = data.get("data", {})
        champs = []

        for champ_id in raw_champs.keys():
            champs += [ChampionData.ChampionData(champ_id, raw_champs.get(champ_id, None))]
        return champs

    @staticmethod
    def __api_service_check(request):
        if request.status_code != RiotException.NoException:
            if DEBUG:
                raise Exception('{0}: {1}'.format(request.status_code, request.reason))
            return False
        return True

    def __check_api_key(self, api_key):
        payload = {"api_key": api_key}
        url = (urls.base + urls.player_by_name).format(region='na', summonerNames='drunk7irishman')
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.AccessDenied:
            raise Exception("Api key is not recognized by RiotGames." +
                            "Check that your key is correct or visit https://developer.riotgames.com to receive one.")
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            self.__check_api_key(api_key)

    def __search_for_player(self):
        payload = {"api_key": self._key}
        url = (urls.base + urls.player_by_name).format(region=self._region, summonerNames=self._username)
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.NotFound:
            raise Exception("Player {0} not found in region {1}", self._username, self._region)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            self.__search_for_player()
        if not self.__api_service_check(r):
            self._player = None
            return

        data = r.json()
        player = Player.Player(data[self._username])
        self._player = player

    def __match_details(self, match_id: int, include_timeline):
        payload = {"api_key": self._key, "includeTimeline": include_timeline}
        url = (urls.base + urls.match_details).format(region=self._region, matchId=match_id)
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            return self.__match_details(match_id, include_timeline)
        if not self.__api_service_check(r):
            return []

        data = r.json()
        return data

    def change_search_parameters(self, username: str=None, region: str=None):
        if (username and username != self._username) or (region and region != self._region):
            self._username = username if username else self._username
            self._region = region if region else self._region
            self.__search_for_player()

    def ranked_match_history(self, skip: int=0, include_timeline: bool=True):
        if self._player is None:
            return []
        payload = {"api_key": self._key, "beginIndex": skip}
        url = (urls.base + urls.ranked_match_history).format(region=self._region, summonerId=self._player.id)
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            return self.ranked_match_history()
        if not self.__api_service_check(r):
            return []

        data = r.json()

        matches_json = data.get("matches", [{}])

        matches = []
        for match in matches_json:
            match_id = match.get("matchId", -1)
            matches += [Match.Match(match_id, self.__match_details(match_id, include_timeline))]

        return matches

    def recent_match_history(self, include_timeline: bool=False):
        if self._player is None:
            return []
        payload = {"api_key": self._key}
        url = (urls.base + urls.recent_match_history).format(region=self._region, summonerId=self._player.id)
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            return self.recent_match_history()
        if not self.__api_service_check(r):
            return []

        data = r.json()

        matches_json = data.get("games", [{}])

        matches = []
        for match in matches_json:
            match_id = match.get("gameId", -1)
            matches += [Match.Match(match_id, self.__match_details(match_id, include_timeline))]
        return matches

    def ranked_stats(self):
        if self._player is None:
            return []
        payload = {"api_key": self._key}
        url = (urls.base + urls.ranked_stats).format(region=self._region, summonerId=self._player.id)
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            return self.ranked_stats()
        if not self.__api_service_check(r):
            return None

        data = r.json()
        stats = RankedStats.RankedStats(data)

        champions_data = self._champion_data
        for champ in stats.champions:
            try:
                champ_data = next(champ_data for champ_data in champions_data if int(champ_data.id) == int(champ.id))
                champ.name = champ_data.name
            except StopIteration:
                champ.name = "Generalized Stats"

        return stats

    def summary_stats(self):
        if self._player is None:
            return []
        payload = {"api_key": self._key}
        url = (urls.base + urls.general_stats).format(region=self._region, summonerId=self._player.id)
        r = requests.get(url, params=payload)
        if r.status_code == RiotException.RateLimitExceeded:
            time.sleep(1)
            return self.ranked_stats()
        if not self.__api_service_check(r):
            return {}

        data = r.json()
        stats = []
        for stat in data.get("playerStatSummaries", [{}]):
            stats += [SummaryStats.SummaryStats(stat)]

        return stats