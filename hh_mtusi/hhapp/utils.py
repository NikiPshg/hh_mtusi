import requests
from .models import Vacancy
from fake_useragent import UserAgent



def chek_salary(item):
    try:
        return item['salary']['from']
    except:
        return 1.0

def fetch_and_save_vacancies(keyword, page=0, per_page=20 , salary=None):
    ua = UserAgent()
    url = 'https://api.hh.ru/vacancies/'
    params = {
        'text': keyword,
        'page': page,
        'per_page': per_page,
        'area': 1
    }
    random_user_agent = ua.random
    headers = {'User-Agent': random_user_agent}
    response = requests.get(f"{url}", params=params, headers=headers)
    data = response.json()
    for item in data['items']:
        hh_id = item['id']
        name = item['name']
        company = item['employer']['name']
        salary = chek_salary(item)
        url = item['alternate_url']
        published_at = item['published_at']

        # Сохраняем вакансию в базе данных
        Vacancy.objects.update_or_create(
            hh_id=hh_id,
            defaults={
                'name': name,
                'company': company,
                'salary' :salary,
                'url': url,
                'published_at': published_at,
            }
        )
