from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from django.urls import reverse


class AdminSite(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin"londonapp.com',
            password='password123'
            )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@loandonapp.com',
            password='test123',
            name='test user full name',
        )

    def test_users_listed(self):
        '''test that users are listed on user page'''
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        ''' test the userr edit page works '''
        url = reverse('admin:core_user_change', args=[self.user.id])
        # self.user.ig generates /admin/core/user/1(id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        '''test that create user page works'''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
