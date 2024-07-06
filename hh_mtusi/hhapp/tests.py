

from django.test import TestCase, Client
from django.urls import reverse
from .models import Vacancy
from datetime import datetime

class HomeViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'hhapp/home.html')

class VacancyListViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_vacancy_list_view_status_code(self):
        response = self.client.get(reverse('vacancy_list'))
        self.assertEqual(response.status_code, 200)

    def test_vacancy_list_view_template(self):
        response = self.client.get(reverse('vacancy_list'))
        self.assertTemplateUsed(response, 'hhapp/vacancy_list.html')

    def test_vacancy_list_contains_vacancies(self):

        Vacancy.objects.create(
            hh_id='123456',
            name='Test Job',
            company='Test Company',
            salary=50000.00,
            area=1,
            employment='Full-time',
            url='https://example.com/test-job',
            published_at=datetime.now(),
            experience='1-3 years'
        )
        
        response = self.client.get(reverse('vacancy_list'), count_created=1)
        self.assertContains(response, 'Test Job')
