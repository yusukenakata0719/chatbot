from django.shortcuts import render, redirect
from django.conf import settings
from .models import UploadedURL, PDFDocument
from .form import URLUploadForm, PDFUploadForm
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage, download_loader
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
import os, glob
import shutil
import openai
openai.api_key = settings.OPENAI_API_KEY
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def select_data(request):
    return render(request, 'select_data.html')

@login_required
def upload_and_list_pdf(request):
    if request.method == 'POST':
        # PDFアップロードの処理
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            document = PDFDocument(name=pdf_file.name, pdf_file=pdf_file)
            document.save()
            return redirect('upload_and_list_pdf')

    else:
        form = PDFUploadForm()

    # PDFドキュメントのリストを取得
    pdf_documents = PDFDocument.objects.all()

    context = {
        'form': form,
        'pdf_documents': pdf_documents,
    }
    
    return render(request, 'upload_and_list_pdf.html', context)

class PDFListView(ListView):
    template_name = 'upload_and_list_pdf.html'
    model = PDFDocument


@login_required
def delete_pdf(request, pk):
    number = PDFDocument.objects.all().count()
    if number > 0:
        document = PDFDocument.objects.get(pk=pk)
        document.delete()
        return redirect('upload_and_list_pdf')
    else:
        return redirect('upload_and_list_pdf')

@login_required
def dealing_pdf(request):
    # ファイルの読み込み処理を書く
    documents = SimpleDirectoryReader("pdfs").load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    return redirect('delete_all_pdf')


@login_required
def delete_all_pdf(request):
    documents = PDFDocument.objects.all()
    documents.delete()
    return redirect('ask_questions')

@login_required
def upload_web(request):
    if request.method == 'POST':
        form = URLUploadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            uploaded_url = UploadedURL(url=url)
            uploaded_url.save()
            return redirect('dealing_web')
    else:
        form = URLUploadForm() # GETの時fromのインスタンスを作成してテンプレートに渡す
        return render(request, 'upload_web.html', {'form': form})

@login_required
def dealing_web(request):
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
    loader = BeautifulSoupWebReader()
    # アップロードされたURLを取得
    uploaded_url = UploadedURL.objects.latest('uploaded_at')
    url = uploaded_url.url
    # URLを使用してデータを読み込む
    documents = loader.load_data(urls=[url])
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    return redirect('ask_questions')


@login_required
def ask_questions(request):
    if request.method == 'POST':
        question = request.POST['question']
        # ここで質問に対する回答を取得する処理を書く
        strorage_context = StorageContext.from_defaults(persist_dir='./storage')
        index = load_index_from_storage(strorage_context)
        query_engine = index.as_query_engine()
        answer = query_engine.query(question)
        return render(request, 'answer.html', {'answer':answer})
    else:
        return render(request, 'ask.html',)

@login_required
def setting(request):
    return render(request, 'setting.html')  # ここで設定を変更する処理を書く

@login_required
def delete_all(request):
    shutil.rmtree('./storage')
    os.mkdir('./storage')
    return redirect('complete_delete_all')

@login_required
def confirm_delete_all(request):
    return render(request, 'confirm_delete_all.html')

@login_required
def complete_delete_all(request): 
    return render(request, 'complete_delete_all.html')


def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            return redirect('log_in')
        except IntegrityError:
            return render (request, 'signup.html', {'error':'このユーザーは既に登録されています'})
        
    else:
        return render(request, 'signup.html',{})


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html',{'error':'ログインに失敗しました'})
    else:
        return render(request, 'login.html',{})
    
def log_out(request):
    logout(request)
    return redirect('log_in')