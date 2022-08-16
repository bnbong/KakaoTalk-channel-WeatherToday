def test_could_get_data_from_weather_api():
    from dotenv import load_dotenv

    import os
    import requests

    load_dotenv()

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    serviceKey = os.getenv('WEATHER_SECRET_KEY_DECODED')
    nx = '61'
    ny = '126'

    # location set to Gangnam
    request_data = {
        'serviceKey' : serviceKey,
        'numOfRows' : '10',
        'pageNo' : '1',
        'dataType' : 'JSON',
        'base_date' : '20220815',
        'base_time' : '0500',
        'nx' : nx,
        'ny' : ny
    }

    response = requests.get(url, params=request_data)
    
    response_weather_data_json = response.json().get('response').get('body').get('items')

    assert None != response_weather_data_json

    print(response_weather_data_json)