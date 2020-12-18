from final_project_ziqiliao import __version__
from final_project_ziqiliao import final_project_ziqiliao

def test_version():
    assert __version__ == '0.1.0'
    
def find_game(genre, platform, keyword):
    
    import requests
    import json
    import pandas as pd
    import re
    from requests.exceptions import HTTPError
    try:
        r = requests.get('https://www.freetogame.com/api/games')
        r.status_code
        if r.status_code != 200:
            raise print('The connection to the API client is lost.')
        freetogame_json = r.json()
        freetogame_json_df = pd.DataFrame(freetogame_json)
        freetogame_json_df['platform'] = freetogame_json_df['platform'].replace('PC (Windows)','PC')
        freetogame_json_df['platform'] = freetogame_json_df['platform'].replace('Web Browser','WB')
        freetogame_json_df['platform'] = freetogame_json_df['platform'].replace('PC (Windows), Web Browser','PC & WB')
        genreofgame = freetogame_json_df[freetogame_json_df['genre'] == genre]
        platform = genreofgame[genreofgame['platform'] == platform]
        ids = platform.short_description.str.contains(keyword, flags = re.IGNORECASE, regex = True, na = False)

        return platform[ids]
        # If the response was successful, no Exception will be raised
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def test_wrong_input():
    expect = 0
    actual = find_game('wrong','PC','free-to-play')
    assert expect == actual.size
    

def display_image(title):
   
    import requests
    import pandas as pd
    import re
    import io
    import PIL.Image
    r = requests.get('https://www.freetogame.com/api/games')
    freetogame_json = r.json()
    freetogame_json_df = pd.DataFrame(freetogame_json)
    freetogame_json_df

    desiredgame = freetogame_json_df[freetogame_json_df['title']==title]
    url = desiredgame.copy()

    search1 = re.findall(r'(https://www.freetogame.com/g/\d+/thumbnail.jpg)',str(url['thumbnail']))
    result = ''.join(map(str, search1))

    response = requests.get(result)
    image_bytes = io.BytesIO(response.content)

    img = PIL.Image.open(image_bytes)
    img.show()

    return img

def test_wrong_name():
    expect = 0
    actual = display_image('wrong')
    assert expect == actual.size
