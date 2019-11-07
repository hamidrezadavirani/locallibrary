from django.shortcuts import render

# Create your views here.

from catalog.models import Author, Book, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render (request, 'index.html' , context= context)

from django.views import generic

class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    template_name = 'book_list.html'

    def get_queryset(self):
        return Book.objects.all()[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView , self).get_context_data(**kwargs)
        context ['some_data'] = 'This is just some data'
        return context


class BookDetailView(LoginRequiredMixin ,generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
