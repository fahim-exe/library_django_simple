from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, BookInstance, Author, Language, Genre
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required #for function based view we use decorators
from django.contrib.auth.mixins import LoginRequiredMixin #for class based view we use mixins

from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    context = {
        'num_books':num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available
    }

    return render(request, 'catalog/index.html', context=context)


class BookCreate(LoginRequiredMixin, CreateView): #model_form.html -->> book_form.html
    model = Book
    fields = '__all__'


class BookDetail(DetailView):
    model = Book


@login_required
def my_view(request):
    
    return render(request, 'catalog/my_view.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    template_name = 'catalog/signup.html'



class CheckedBooks(LoginRequiredMixin, ListView):
    #list all book instances but filter based off currenty logged in user session

    mode = BookInstance
    template_name = 'catalog/profile.html'
    
    paginate_by = 5 # 5 book instances per page

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)

