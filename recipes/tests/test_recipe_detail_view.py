from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


# resolve -> qual função está sendo usada para renderizar a página
class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertEqual(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        # Need a recipe for this test
        needed_title = 'This is a detail page - It load one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')

        # Check if one recipe is loaded
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        url = reverse(
            'recipes:recipe',
            kwargs={'pk': recipe.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
