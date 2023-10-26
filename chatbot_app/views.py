from django.shortcuts import render, redirect
from django.conf import settings
from .models import UploadedURL, PDFDocument, JSONDocument
from .form import URLUploadForm, PDFUploadForm 
from llama_index import StorageContext, load_index_from_storage, download_loader,GPTVectorStoreIndex, SimpleDirectoryReader
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
import os, glob
import shutil
import openai
openai.api_key = settings.OPENAI_API_KEY
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def select_data(request):
    return render(request, 'select_data.html')

@login_required
def upload_and_list_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            # ユーザーとPDFファイルを関連付けて保存
            user_pdf = PDFDocument(user=request.user, pdf_file=pdf_file)
            user_pdf.save()
            return redirect('upload_and_list_pdf')

    else:
        form = PDFUploadForm()

    # ユーザーごとのPDFドキュメントのリストを取得
    pdf_documents = PDFDocument.objects.filter(user=request.user)

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
from django.core.files import File

#pdfファイルを学習させる
def dealing_pdf(request):
    user = request.user
    user_id = str(user.id)
    # JSONファイルを保存するディレクトリパスを生成
    json_directory = os.path.join(settings.MEDIA_ROOT, 'jsons', user_id)
    # ディレクトリが存在しない場合に作成
    os.makedirs(json_directory, exist_ok=True)
    # ユーザーごとのPDFのディレクトリのパスを取得
    pdf_directory = os.path.join(settings.MEDIA_ROOT, 'pdfs', user_id)

    # JSONデータをファイルに保存
    documents = SimpleDirectoryReader(pdf_directory).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=json_directory)

    return redirect('save_json_to_model')

#jsonファイルをモデルに保存
def save_json_to_model(request):
    # ファイルのパスを取得
    json_directory = "/Users/yu-suke/pyworks/projects/chatbot_project/media/jsons"  # ディレクトリのパスを設定
    json_file_paths = glob.glob(os.path.join(json_directory, '*.json'))
    for json_file_path in json_file_paths:
        # JSONファイルを`json_file`フィールドに設定
        with open(json_file_path, 'rb') as file:
            json_document = JSONDocument(user=request.user, json_file=File(file))
            json_document.save()
    return redirect('ask_questions')

#jsonファイルをモデルからローカルに保存
def save_json_from_model(request):
    # ユーザーごとのJSONドキュメントのリストを取得
    json_documents = JSONDocument.objects.filter(user=request.user)
    
    # ローカルの保存先ディレクトリを設定
    json_directory = os.path.join(settings.MEDIA_ROOT, 'user_jsons')
    
    # ユーザーごとのJSONドキュメントをローカルに保存
    for json_document in json_documents:
        # ユーザーごとのディレクトリを作成 (存在しない場合)
        user_directory = os.path.join(json_directory, str(request.user.id))
        os.makedirs(user_directory, exist_ok=True)

        # ファイルの保存パスを生成
        json_file_path = os.path.join(user_directory, json_document.json_file.name)

        # ファイルをローカルに保存
        with open(json_file_path, 'wb') as file:
            file.write(json_document.json_file.read())
    
    return redirect('home')

@login_required
def ask_questions(request):
    if request.method == 'POST':
        question = request.POST['question']
        # ここで質問に対する回答を取得する処理を書く
        #jsonファイルの読み込みディレクトリを確認する！！
        strorage_context = StorageContext.from_defaults(persist_dir='jsons')
        index = load_index_from_storage(strorage_context)
        query_engine = index.as_query_engine()
        answer = query_engine.query(question)
        return render(request, 'answer.html', {'answer':answer})
    else:
        return render(request, 'ask.html',)

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