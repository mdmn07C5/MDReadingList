from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .src import md_reading_list as mdrl
from .forms import AuthForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.http import JsonResponse
# Create your views here.

def index(request):
    form = AuthForm(request.POST)
    if form.is_valid():
        if token := login(form, request):
            request.session['token'] = token
            return HttpResponseRedirect(
                'readlist'
            )
    return render(
        request=request, 
        template_name='main/index.html', 
        context={ 'form':form }
    )

def login(form, request):
    payload = {
        'username': form.cleaned_data.get('username'),
        'password': form.cleaned_data.get('password')
    }
    token = mdrl.login(payload)
    if token == None:
        messages.error(request, 'Invalid username or password')
    return token

def readlist(request):
    print(request.session['token'])
    return render(request, 'main/readlist.html')   

def return_reading_list_json(request):
    session_token = request.session['token']
    
    follows = mdrl.get_follow_list(session_token)

    # for tests because mangadex's api is slow 
    # follows = follows[:5]

    read_chapters = mdrl.get_last_read(
        session_token, follows['id'].to_list()
    )
    
    last_read_chapter = mdrl.get_chapter_detail(read_chapters)

    reading_list = follows.join(
        last_read_chapter.set_index('id'), on='id'
    )

    # <a href="url">link text</a> 
    reading_list['mu_id'] = reading_list['mu_id'].map(
        lambda x: f'https://www.mangaupdates.com/series.html?id={x}' 
            if x else 'None'
    )

    reading_list.rename(
        columns={
            'title': 'Title',
            'last_read': 'Last Chapter Read',
            'chapter_title': 'Chapter Title',
            'mu_id': 'Mangaupdates Link'
        },
        inplace=True
    )

    request.session['reading_list_as_csv'] = reading_list.to_csv(
        encoding='utf-8'
    )

    reading_list_html = reading_list[
        ['Title', 'Last Chapter Read', 'Chapter Title', 'Mangaupdates Link']
    ].to_html(
        classes=['striped', 'responsive-table'],
        render_links=True,
        index=False,
    )

    return JsonResponse(
        {'content': reading_list_html},
        status=200
    )

def download_reading_list_as_csv(request):
    response = HttpResponse(
        content = request.session['reading_list_as_csv'],
        content_type = 'text/csv'
    )
    response['Content-Disposition'] = 'attachment; filename="Reading_List.csv"'
    
    return response

def blank(request):
    print('yeehaw')
    print('m8awejfklajsdf;aj;dsjf')
    return render(request, 'main/blank.html')