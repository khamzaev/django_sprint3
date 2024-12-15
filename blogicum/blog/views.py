from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from .models import Post, Category


def index(request):
    """Отображает главную страницу с последними 5 опубликованными постами."""
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]

    return render(
        request,
        'blog/index.html',
        {'post_list': posts}
    )


def post_detail(request, id):
    """Отображает подробную информацию о посте по его ID."""
    try:
        post = Post.objects.get(id=id)
        now = timezone.now()

        if post.pub_date > now:
            raise Http404("Публикация еще не доступна.")

        elif not post.is_published:
            raise Http404("Публикация не опубликована.")

        elif not post.category.is_published:
            raise Http404("Категория публикации скрыта.")

    except Post.DoesNotExist:
        raise Http404(f'Пост с ID {id} не найден.')

    return render(
        request,
        'blog/detail.html',
        {'post': post}
    )


def category_posts(request, category_slug):
    """
    Отображает все посты, относящиеся к заданной категории.
    Если категория не опубликована — возвращаем ошибку 404.
    """
    try:
        category = Category.objects.get(slug=category_slug)

        if not category.is_published:
            raise Http404("Категория скрыта.")

        now = timezone.now()
        posts = Post.objects.filter(
            category=category,
            pub_date__lte=now,
            is_published=True
        ).order_by('-pub_date')

    except Category.DoesNotExist:
        raise Http404(f'Категория с slug {category_slug} не найдена.')

    return render(
        request,
        'blog/category.html',
        {'post_list': posts, 'category': category})
