from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Vacancy
from .utils import fetch_and_save_vacancies
from .forms import SearchForm

def render_home_from_api(request, form):
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        area =  form.cleaned_data['area']
        return HttpResponseRedirect(f'/vacancies/?keyword={keyword}&area={area}')
    
#выдача из db по фильтрам
def render_home_from_db(request, form):
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        area =  form.cleaned_data['area']
        filtered_vacancies = Vacancy.objects.filter(area=area , name__icontains=keyword)
        filtered_vacancies = filtered_vacancies.order_by('-salary')  
        return render(request, 'hhapp/vacancy_list.html',  { 'vacancies': filtered_vacancies })
#рендер страницы home
def home(request):
    form = SearchForm(request.POST)
    if request.method == 'POST' and ('search_button' in request.POST):
        return render_home_from_api(request , form)
    elif request.method == 'POST' and ('search_in_db_button' in request.POST):
        return render_home_from_db(request, form) 
    else:
        form = SearchForm()

    return render(request, 'hhapp/home.html', {'form': form})


#рендер страницы c вакансиями из hhapi
def vacancy_list(request):
    keyword = request.GET.get('keyword', '')
    area = request.GET.get('area', 1)  # Получаем ключевое слово из GET-параметра
    if keyword:
        fetch_and_save_vacancies(keyword=keyword,
                                 area=area)  # Получаем и сохраняем вакансии, если ключевое слово задано

    vacancies = Vacancy.objects.order_by('-id')[:10]
    return render(request, 'hhapp/vacancy_list.html', { 'vacancies' : vacancies,})
