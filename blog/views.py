from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost


class BlogListView(ListView):
    """
    Контроллер списка блоговых записей
    Отображает только опубликованные статьи
    """
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """
        Переопределяем queryset для вывода только опубликованных статей
        """
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """
    Контроллер отдельной блоговой записи
    При открытии увеличивает счетчик просмотров
    """
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """
        Переопределяем метод для увеличения счетчика просмотров
        """
        obj = super().get_object(queryset)
        # Увеличиваем счетчик просмотров
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    """
    Контроллер создания блоговой записи
    """
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    """
    Контроллер редактирования блоговой записи
    """
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        """
        После редактирования перенаправляем на страницу просмотра статьи
        """
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """
    Контроллер удаления блоговой записи
    """
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    context_object_name = 'post'
