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


base = 'https://{0}.api.pvp.net/'

player_by_name = 'api/lol/{region}/v1.4/summoner/by-name/{summonerNames}'

ranked_match_history = 'api/lol/{region}/v2.2/matchhistory/{summonerId}'

match_details = '/api/lol/{region}/v2.2/match/{matchId}'

recent_match_history = '/api/lol/{region}/v1.3/game/by-summoner/{summonerId}/recent'

ranked_stats = '/api/lol/{region}/v1.3/stats/by-summoner/{summonerId}/ranked'

summary_stats = '/api/lol/{region}/v1.3/stats/by-summoner/{summonerId}/summary'

champion_data = '/api/lol/static-data/{region}/v1.2/champion'

champion_data_by_id = champion_data + '/{id}'

rune_data = '/api/lol/static-data/{region}/v1.2/rune'

rune_data_by_id = rune_data + '/{id}'

mastery_data = '/api/lol/static-data/{region}/v1.2/mastery'

mastery_data_by_id = mastery_data + '/{id}'

summoner_spell_data = '/api/lol/static-data/{region}/v1.2/summoner-spell'

summoner_spell_data_by_id = summoner_spell_data + '/{id}'

item_data = '/api/lol/static-data/{region}/v1.2/item'

item_data_by_id = item_data + '/{id}'

league_data = '/api/lol/{region}/v2.5/league/by-summoner/{summonerIds}'

current_game = '/observer-mode/rest/consumer/getSpectatorGameInfo/{platformId}/{summonerId}'