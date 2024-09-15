from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from base.views import map_view


class TestUrls(SimpleTestCase):
    """ Contains tests for the URLs to ensure that they are resolved to correct view functions. """
    def test_map_view_url_resolves(self):
        url = reverse('map_view')
        self.assertEqual(resolve(url).func, map_view)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)
