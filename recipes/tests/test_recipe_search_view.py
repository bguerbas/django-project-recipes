from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


# resolve -> qual função está sendo usada para renderizar a página
class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes-search'))
        self.assertEqual(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes-search') + '?q=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes-search') + '?q=<teste>'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn('Search for &quot;&lt;teste&gt;&quot;', content)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes-search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
