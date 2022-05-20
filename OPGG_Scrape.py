from bs4 import BeautifulSoup
from lxml import etree
import requests


def recent_match_history(
        username, region='na', result='wins',
        game_modes=['Ranked Solo', 'ARAM', "Normal", "Flex 5:5 Rank", "Clash"],
        debug=False
):

    """
        Scrapes User Data About The Games A User Has Played In The Past 24 Hours.

    Notes:
        - Currently Assumes That The User's Profile Is Up To Date

    Args:
        username: (str) The Username That We Whose OP.gg We Are Scraping.
        region: (str) The Region String That The User Plays In.
        result: (str) 'wins', 'all' or 'losses'.
        game_modes: (list) Strings Of Game mode Text As They Are Found On op.gg.
        debug: (bool) Decides If The Program Should Be Executed In Debug Mode.

    Returns:
        A Dictionary Whose Keys Are The Strings Of Gamemodes That Are Tracked And Whose Values Are The Number
        Of Wins/Losses In The Gamemode Within The Last 24h Hours.

    Alternate Return:
         If The Region Of The User Is Specified But Not Valid, This Method Returns An Empty Dictionary.
         Similarly, If The Type Of Results That The User Specified Is Not Valid, This Method Returns An Empty Dictionary.
    """

    # List Of League Regions With Servers As Of May 2022
    list_of_region_strs = ['na', 'euw', 'eune', 'oce', 'kr', 'jp', 'br', 'las', 'lan', 'ru', 'tr']

    # region Return If Invalid Arguments

    result = result.lower()

    if region not in list_of_region_strs:
        if debug:
            print(f"Region String '{region}' Is Not A Recognized Region String")

        return dict()

    elif result not in ('wins', 'losses', 'all'):   # Permissible Result Options
        if debug:
            print(f"Result String '{result}' Is Not A Recognized Result String")

        return dict()

    # endregion

    # OP.gg Page Follows This Structure (The 'na' Just Means Its Where The Website Is Hosted)
    match_history_url = f'https://na.op.gg/summoners/{region}/{username}'

    if debug:
        # Doesn't Print Hyperlink Correctly, This Does Not Impact Functionality
        print(f"Match History URL Generated:\t{match_history_url}")

    HEADERS = (
        {'User-Agent':
             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
         'Accept-Language': 'en-US, en;q=0.5'}
    )

    webpage = requests.get(match_history_url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    # Future Update Profile Implementation Here

    def get_game_mode_result(gamemode_str, result_str, debug=debug):

        """
            Creates And Uses Queries To Obtain The Number Of Times A Result Was Achieved In A Particular Gamemode.

        Notes:
            - Query Returns Are Buggy When There Is More Than 1 Resulting Object When Using The Query.
            - bs4 Does Not Directly Support Xpath Queries

        Args:
            gamemode_str: The Text That op.gg Uses On Their Website When Refering To That Gamemode.
            result_str: Either 'Victory' or 'Defeat' Exactly
            debug: (bool) If The Method Should Be Executed In Debug Mode.

        Returns:
            An Integer That Corresponds To The Number Of Times A Certain Result Occured For A Particular Gamemode
            Within The Last 24 Hours.

        """

        # Must Account For Singular And Plural Of Minutes And Hours
        query = f"count(//div[@class='game'and" \
                f" ./div[contains(text(),'{gamemode_str}')]" \
                f" and ./div[contains(text(),'{result_str}')]" \
                f" and ( (./div/div[contains(text(), 'minute')])" \
                f" | (./div/div[contains(text(), 'hour')]))" \
                f"])"

        if debug:
            print(f"Generated Query:\t{query}")

        return int(dom.xpath(query))

    # Execute Profile Update Here

    if result == 'wins':
        results_dict = {game_mode: get_game_mode_result(game_mode, 'Victory', debug=False) for game_mode in game_modes}

    elif result == 'all':
        results_dict = dict()
        for game_mode in game_modes:
            results_dict[f"{game_mode} Victory"] = get_game_mode_result(game_mode, 'Victory', debug=False)
            results_dict[f"{game_mode} Defeat"] = get_game_mode_result(game_mode, 'Defeat', debug=False)

    else:   # Losses
        results_dict = {game_mode: get_game_mode_result(game_mode, 'Defeat', debug=False) for game_mode in game_modes}

    if debug:
        print(f'{username}:\t{results_dict}\n')


    return results_dict
