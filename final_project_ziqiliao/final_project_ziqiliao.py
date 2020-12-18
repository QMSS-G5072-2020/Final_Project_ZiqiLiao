def find_game(genre, platform, keyword):
    """
    The function returns the game lists from the freetogame databse with desired genre and platform to play on.

    Parameters
    ---
    genre:
        str, the genre that the player would like to play, some options are: Shooter, MOBA, Strategy..
        
    platform:
        str, the platform that the player would like to play on, options are: PC, Web Browser, PC and Web Browser
    
    keyword:
        str, the keyword description that the player would like to play, some options are: battle, free-to-play, 3D, action...
    
    Returns
    ---
    output: pandas.DataFrame of the API with required parameters
        
    Index: 
            RangeIndex
    Columns:
            id: object	
            title: object		
            thumbnail: object		
            short_description: object		
            game_url: object		
            genre: object		
            platform: object		
            publisher: object		
            developer: object		
            release_date: object		
            freetogame_profile_url: object	

    Example
    ---
    >>> df = find_game('Strategy','PC','free-to-play')
    >>> df.shape
    (32, 11)
    
    """
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
       

def display_image(title):
    """
    The function would show a image of the game to the user.

    Parameters
    ---
    title:
        str, the title of the game that the user would like to take a look.
        
    Returns
    ---
    It shows an image
        
    Index: 
            RangeIndex
    Columns:
            id: object	
            title: object		
            thumbnail: object		
            short_description: object		
            game_url: object		
            genre: object		
            platform: object		
            publisher: object		
            developer: object		
            release_date: object		
            freetogame_profile_url: object	

    Example
    ---
    >>> img = display_image ('Dauntless')
    >>> img.size
    (365, 206)

    """
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
