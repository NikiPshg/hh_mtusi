import requests
from .models import Vacancy

def fetch_and_save_vacancies(keyword, page=0, per_page=20):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': keyword,
        'page': page,
        'per_page': per_page
    }
    response = requests.get(url, params=params)
    data = response.json()

    for item in data['items']:
        # Извлекаем данные о вакансии
        hh_id = item['id']
        name = item['name']
        company = item['employer']['name']
        url = item['alternate_url']
        published_at = item['published_at']

        # Сохраняем вакансию в базе данных
        Vacancy.objects.update_or_create(
            hh_id=hh_id,
            defaults={
                'name': name,
                'company': company,
                'url': url,
                'published_at': published_at
            }
        )