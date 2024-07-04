import requests
from .models import Vacancy
import random
from fake_useragent import UserAgent



def chek_salary(item):
    try:
        return item['salary']['from']
    except:
        return 1.0

def get_response(keyword, per_page=20 , area=1):
    ua = UserAgent()
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': keyword,
        'page': random.randint(0,10),
        'per_page': per_page,
        'area': area
    }
    random_user_agent = ua.random
    headers = {'User-Agent': random_user_agent}
    response = requests.get(f"{url}", params=params, headers=headers)
    return response , area

def receiving_data_from_response(response):
    data = response.json()
    for item in data['items']:
        hh_id = item['id']
        name = item['name']
        company = item['employer']['name']
        salary = chek_salary(item)
        url = item['alternate_url']
        published_at = item['published_at']
    return hh_id , name , company , salary , url , published_at
 
def save_to_db(hh_id:int , name:str , company:str , salary:int , url , published_at , area):
    Vacancy.objects.update_or_create(
            hh_id=hh_id,
            defaults={
                'name': name,
                'company': company,
                'salary' :salary,
                'url': url,
                'published_at': published_at,
                'area' : area
            }
        )

def fetch_and_save_vacancies(keyword):
    response , area = get_response(keyword,area=1)
    hh_id , name , company , salary , url , published_at  = receiving_data_from_response(response)
    save_to_db(hh_id , name , company , salary , url , published_at , area)
    

