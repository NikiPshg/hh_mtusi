import requests
from .models import Vacancy
import random
from fake_useragent import UserAgent


exp_to_rutext ={
    "noExperience" : 'Нет опыта',
    "between1And3" : 'От 1 года до 3 лет',
    "between3And6" : 'От 3 до 6 лет',
    "moreThan6" : 'Более 6 лет',
}

rutext_to_exp ={
    'Нет опыта' : "noExperience",
    'От 1 года до 3 лет' : "between1And3",
    'От 3 до 6 лет' :"between3And6", 
    'Более 6 лет' :  "moreThan6",
}


citi_to_index ={
    'москва':1,
    'питер':2,
    'петербург':3,
    'екатринбург':3,
    'екб':3
}


def chek_salary(item):
    try:
        return item['salary']['from']
    except:
        return 1.0

#получение response c api
def get_response(keyword:str,
                area:int,
                experience:str,
                per_page:int=20,):
    
    ua = UserAgent()
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': keyword,
        'page': random.randint(0,5),
        'per_page': per_page,
        'area': area,
        'experience': experience
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
                area:int,
                experience:str):

    #добавление в бд
    Vacancy.objects.update_or_create(hh_id=hh_id,
                                    defaults={
                                    'name': name,
                                    'company': company,
                                    'salary' :salary,
                                    'url': url,
                                    'experience' : experience,
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
        experience = item['experience']['id']
        area = item['area']['id']

        save_to_db( hh_id = hh_id,
                    name = name,
                    employment = employment,
                    company = company,
                    salary = salary,
                    experience = exp_to_rutext.get(experience , experience),
                    url = url,
                    published_at = published_at,
                    area = area)


def fetch_and_save_vacancies(keyword , experience , area:1):
    response = get_response(keyword,area,experience)
    receiving_data_from_response(response)


    

