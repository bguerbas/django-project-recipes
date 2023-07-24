from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q

from utils.pagination import make_pagination
from .models import Recipe


PER_PAGE = 9


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title': f'{recipes[0].category.name} - Category |'
        })


def recipe(request, id):
    recipe = Recipe.objects.filter(
        pk=id,
        is_published=True,
    ).order_by('-id').first()
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # busca por título que contenha o termo (se colocar title = search_term, busca exata)  # noqa: E501
        # o 'i' no final do icontains significa case insensitive (ignora maiúsculas e minúsculas) # noqa: E501
        Q(
            Q(title__icontains=search_term) |  # o "Q" serve para indicar a busca por OU # noqa: E501
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
        })
