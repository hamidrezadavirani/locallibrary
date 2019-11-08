from django.shortcuts import render, get_object_or_404
from catalog.models import Author, Book, BookInstance
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

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

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'author_list.html'

    def get_queryset(self):
        return Author.objects.all()[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['arbitrary'] = 'This is an arbitrary data added by my self '
        return context


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

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):

    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        # form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            # book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})
        form = RenewBookModelForm(initial={'due_back':proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'book_renew_librarian.html', context=context)

class AllBorrowedListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'all_borrowed_books.html'
    permission_required = 'catalog.can_mark_returned'
    def get_queryset(self):
        context = BookInstance.objects.filter(status__exact='o')
        for item in context:
            print(item.book.title)
            print(item.borrower.first_name)
        return context

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    template_name = 'author_form.html'
    fields = '__all__'
    initial = { 'date_of_death' : '05/01/2018' }


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name= 'author_form.html'

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'author_confirm_delete.html'

