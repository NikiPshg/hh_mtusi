from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Vacancy
from .utils import fetch_and_save_vacancies
from .forms import SearchForm
from .utils import citi_to_index , exp_to_rutext ,rutext_to_exp


def render_home_from_api(request, form):
    if form.is_valid():
        keyword = form.cleaned_data['keyword']
        area =  form.cleaned_data['area']
        experience =  rutext_to_exp.get(form.cleaned_data['experience'] , False )
        min_salary = form.cleaned_data['min_salary']
        if not(experience):
            return HttpResponseRedirect(f'/vacancies/?keyword={keyword}&area={area}&experience=between1And3')
        return HttpResponseRedirect(f'/vacancies/?keyword={keyword}&area={area}&experience={experience}&salary_from={min_salary}&only_with_salary=true')
    
#выдача из db по фильтрам
def render_home_from_db(request, form):
    if form.is_valid():
        experience =  form.cleaned_data['experience']
        keyword = form.cleaned_data['keyword']
        min_salary = form.cleaned_data['min_salary']
        area =  citi_to_index.get(form.cleaned_data['area'].lower(), 1)
        filtered_vacancies = Vacancy.objects.filter(area=area,
                                                    name__icontains=keyword,
                                                    salary__gte=min_salary,
                                                    experience__icontains=experience)
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
    area = citi_to_index.get( request.GET.get('area', 1).lower() , 1)   # Получаем ключевое слово из GET-параметра
    experience = request.GET.get('experience', '')
    min_salary = request.GET.get('min_salary', 0)
    if keyword:
        count_created , response = fetch_and_save_vacancies(keyword=keyword,
                                 area=area,
                                 experience=experience,
                                 min_salary=min_salary)  # Получаем и сохраняем вакансии, если ключевое слово задано

    vacancies = Vacancy.objects.order_by('-id')[:count_created]

    return render(request, 'hhapp/vacancy_list.html', { 'vacancies' : vacancies})
