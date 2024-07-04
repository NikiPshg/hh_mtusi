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
            area =  form.cleaned_data['area']
            return HttpResponseRedirect(f'/vacancies/?keyword={keyword}&area={area}')
    else:
        form = SearchForm()
    return render(request, 'hhapp/home.html', {'form': form})

def vacancy_list(request):
    keyword = request.GET.get('keyword', '')
    area = request.GET.get('area', 1)  # Получаем ключевое слово из GET-параметра
    print(area)
    if keyword:
        fetch_and_save_vacancies(keyword=keyword,
                                 area=area )  # Получаем и сохраняем вакансии, если ключевое слово задано

    vacancies = Vacancy.objects.order_by('-id')[:10]
    return render(request, 'hhapp/vacancy_list.html', {
                                                        'vacancies': vacancies,
                                                        'keyword': keyword ,
                                                        'area' : area,
                                                        })
