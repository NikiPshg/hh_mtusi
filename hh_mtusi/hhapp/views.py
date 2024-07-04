from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Vacancy
from .utils import fetch_and_save_vacancies
from .forms import SearchForm

def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            return HttpResponseRedirect(f'/vacancies/?keyword={keyword}')
    else:
        form = SearchForm()
    return render(request, 'hhapp/home.html', {'form': form})

def vacancy_list(request):
    keyword = request.GET.get('keyword', '')  # Получаем ключевое слово из GET-параметра

    if keyword:
        fetch_and_save_vacancies(keyword)  # Получаем и сохраняем вакансии, если ключевое слово задано

    vacancies = Vacancy.objects.all().order_by('-id')[:20]  # Получаем все вакансии из базы данных
    return render(request, 'hhapp/vacancy_list.html', {'vacancies': vacancies, 'keyword': keyword})