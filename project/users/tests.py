import json
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class TestRegisterUser(TestCase):
  def setUp(self):
    self.url = '/user/register/'
    self.client = Client()

  def test_must_render_form_with_email_username_password1_and_password2(self):
    response = self.client.get(self.url)
    form = response.context['form']

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'users/register.html')
    self.assertTrue(form['username'])
    self.assertTrue(form['email'])
    self.assertTrue(form['password1'])
    self.assertTrue(form['password2'])

  def _do_post(self, username, email, password1, password2):
    params = {
      'username': username,
      'email': email,
      'password1': password1,
      'password2': password2,
    }

    response = self.client.post(self.url, params)

    return response

  def test_must_return_json_when_register_user_is_successful(self):
    response = self._do_post('evandrolg', 'evandrolgoncalves@gmail.com', \
                             '123', '123')
    data = json.loads(response.content)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['username'], 'evandrolg')
    self.assertEqual(data['email'], 'evandrolgoncalves@gmail.com')

  def test_must_return_401_when_register_is_unsuccessful(self):
    response = self._do_post('evandrolg', 'evandrolgoncalves@gmail.com', \
                             '123', '1234')

    self.assertEqual(response.status_code, 401)


class TestLoginUser(TestCase):
  def setUp(self):
    self.client = Client()

  def test_must_render_login_page(self):
    response = self.client.get('/user/login/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.templates[0].name, 'users/login.html')

  def _create_new_user(self):
    user = User.objects.create_user('evandrolg', 'evandrolgoncalves@gmail.com', \
                                    '123')
    user.save()

  def test_must_return_json_when_login_is_successful(self):
    self._create_new_user()

    params = {
      'username': 'evandrolg',
      'password': '123',
    }

    response = self.client.post('/user/auth/', params)
    data = json.loads(response.content)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['username'], 'evandrolg')
    self.assertEqual(data['email'], 'evandrolgoncalves@gmail.com')

  def test_must_return_401_when_login_is_unsuccessful(self):
    params = {
      'username': 'evandrolg2',
      'password': '123',
    }

    response = self.client.post('/user/auth/', params)

    self.assertEqual(response.status_code, 401)
