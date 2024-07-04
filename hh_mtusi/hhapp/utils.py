import requests
from .models import Vacancy
import random
from fake_useragent import UserAgent



def chek_salary(item):
    try:
        return item['salary']['from']
    except:
        return 1.0

#получение response c api
def get_response(keyword:str,
                area:int,
                per_page:int=20):
    
    ua = UserAgent()
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': keyword,
        'page': random.randint(0,5),
        'per_page': per_page,
        'area': area,
    }
    random_user_agent = ua.random
    headers = {'User-Agent': random_user_agent}
    response = requests.get(f"{url}", params=params, headers=headers)
    return response 


def save_to_db( hh_id:int,
                name:str,
                employment:str,
                company:str,
                salary:int,
                url,
                published_at,
                area:int):

    #добавление в бд
    Vacancy.objects.update_or_create(hh_id=hh_id,
                                    defaults={
                                    'name': name,
                                    'company': company,
                                    'salary' :salary,
                                    'url': url,
                                    'published_at': published_at,
                                    'employment' : employment,
                                    'area' : area})
    
    
#добавление response в бд 
def receiving_data_from_response(response):
    data = response.json()
    for item in data['items']:
        hh_id = item['id']
        name = item['name']
        company = item['employer']['name']
        salary = chek_salary(item)
        url = item['alternate_url']
        published_at = item['published_at']
        employment = item['employment']['name'] 
        area = item['area']['id']
        save_to_db(hh_id, name, employment, company,salary, url, published_at, area)


def fetch_and_save_vacancies(keyword , area:1):
    response = get_response(keyword,area)
    receiving_data_from_response(response)


    

