from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .src import md_reading_list as mdrl
from .forms import AuthForm
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    form = AuthForm(request.POST)
    if form.is_valid():
        if token := login(form, request):
            return HttpResponseRedirect(
                reverse('main:readlist', kwargs={'session_token':token})
            )
    return render(
        request=request, template_name='main/index.html', context={'form':form}
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

def readlist(request, session_token):
    follows = mdrl.get_follow_list(session_token)
    
    read_chapters = mdrl.get_last_read(
        session_token, follows['id'].to_list()
    )
    
    last_read_chapter = mdrl.get_chapter_detail(read_chapters)
    
    reading_list = follows.join(
        last_read_chapter.set_index('id'), on='id'
    )
    reading_list['mu_id'] = reading_list['mu_id'].map(
        lambda x: f'https://www.mangaupdates.com/series.html?id={x}' 
            if x else 'None'
    )

    return render(
        request=request, 
        template_name='main/readlist.html', 
        context={
            'reading_list': reading_list[
                    ['title', 'last_read', 'chapter_title', 'mu_id']
            ].to_html(classes=['striped', 'responsive-table'])
        }
    )


def blank(request):
    print('yeehaw')
    print('m8awejfklajsdf;aj;dsjf')
    return render(request, 'main/blank.html')
