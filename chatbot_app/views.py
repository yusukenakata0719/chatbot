from django.shortcuts import render, redirect
from django.conf import settings
from .models import UploadedURL, PDFDocument
from .form import URLUploadForm, PDFUploadForm
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage, download_loader
from django.views.generic import ListView
import os, glob
import shutil
import openai
openai.api_key = settings.OPENAI_API_KEY

def home(request):
    return render(request, 'home.html')

def select_data(request):
    return render(request, 'select_data.html')

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


def delete_pdf(request, pk):
    number = PDFDocument.objects.all().count()
    if number > 0:
        document = PDFDocument.objects.get(pk=pk)
        document.delete()
        return redirect('upload_and_list_pdf')
    else:
        return redirect('upload_and_list_pdf')



def dealing_pdf(request):
    directory_path = "/Users/yu-suke/pyworks/projects/chatbot_project/pdfs"
    pdf_files = glob.glob(os.path.join(directory_path, '*.pdf'))  # ディレクトリ内のPDFファイルを取得
    if len(os.listdir(directory_path)) > 0:
        if pdf_files:
            CJKPDFReader = download_loader("CJKPDFReader")
            loader = CJKPDFReader()
            documents = []

            for pdf_file in pdf_files:
                document = loader.load_data(pdf_file)
                documents.append(document)

            index = GPTVectorStoreIndex.from_documents(documents)
            index.storage_context.persist()
            return redirect('delete_all_pdf')
    else:
        return redirect('upload_and_list_pdf')



def delete_all_pdf(request):
    documents = PDFDocument.objects.all()
    documents.delete()
    return redirect('ask_questions')


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


def setting(request):
    return render(request, 'setting.html')  # ここで設定を変更する処理を書く

def delete_all(request):
    shutil.rmtree('./storage')
    os.mkdir('./storage')
    return redirect('complete_delete_all')

def confirm_delete_all(request):
    return render(request, 'confirm_delete_all.html')

def complete_delete_all(request): 
    return render(request, 'complete_delete_all.html')