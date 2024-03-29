import django_filters as filters
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe
from users.models import User

User = get_user_model()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='В корзине.'
    )
    is_favorited = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='В избранных.'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Ссылка'
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']


class LimitFilter(filters.FilterSet):
    limit = filters.AllValuesMultipleFilter('recipes_limit')

    class Meta:
        model = Recipe
        fields = ('limit',)
