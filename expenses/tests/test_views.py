from users.tests.test_setup import TestSetup
from rest_framework import status
from django.contrib.auth.models import User
from expenses.models import Expense
from decimal import Decimal
from django.urls import reverse


from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from expenses.models import Expense

class TestViews(TestSetup):
    def setUp(self):
        super().setUp()
        self.exp1 = Expense.objects.create(user=self.user,title='title1', category='FOOD', amount=Decimal('100'), date='2025-12-3')
        self.exp2 = Expense.objects.create(user=self.user,title='title2', category='TRAVEL', amount=Decimal('50'), date='2025-12-3')
        self.exp3 = Expense.objects.create(user=self.user2,title='title3', category='MISC', amount=Decimal('300'), date='2025-12-3')

        self.expense_url = reverse('expenses-list')
        self.summary_url = reverse('expenses-summery')

    def test_unauthenticated_user_cannot_access_expenses(self):
        res = self.client.get(self.expense_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_see_own_expenses(self):
        self.client.force_login(self.user)
        res = self.client.get(self.expense_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_admin_can_see_all_expenses(self):
        self.client.force_login(self.admin)
        res = self.client.get(self.expense_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 3)

    def test_user_can_create_expense(self):
        self.client.force_login(self.user)
        data = {
            'title':'food expense from bakery',
            'category': 'FOOD',
            'amount': '75.50',
            'date': '2025-12-05'
        }
        res = self.client.post(self.expense_url, data)
        if res.status_code != 201:
            print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.filter(user=self.user).count(), 3)

    def test_user_can_update_own_expense(self):
        self.client.force_login(self.user)
        url = reverse('expenses-detail', args=[self.exp1.id])
        res = self.client.put(url, {'title':'updated-title-from-user','category': 'TRAVEL', 'amount': '120.00', 'date': '2025-12-10'})
        self.assertEqual(res.status_code, 200)
        self.exp1.refresh_from_db()
        self.assertEqual(self.exp1.amount, Decimal('120.00'))

    def test_user_cannot_update_others_expense(self):
        self.client.force_login(self.user)
        url = reverse('expenses-detail', args=[self.exp3.id])
        res = self.client.put(url, {'title':'updated-title-by-test-user','category': 'FOOD', 'amount': '500.00', 'date': '2025-12-10'})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_own_expense(self):
        self.client.force_login(self.user)
        url = reverse('expenses-detail', args=[self.exp1.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Expense.objects.filter(id=self.exp1.id).exists())

    def test_admin_can_update_any_expense(self):
        self.client.force_login(self.admin)
        url = reverse('expenses-detail', args=[self.exp1.id])
        res = self.client.put(url, {'title':'updated-title-from-admin','category': 'MISC', 'amount': '999.00', 'date': '2025-12-10'})
        self.assertEqual(res.status_code, 200)
        self.exp1.refresh_from_db()
        self.assertEqual(self.exp1.amount, Decimal('999.00'))

    def test_admin_can_delete_any_expense(self):
        self.client.force_login(self.admin)
        url = reverse('expenses-detail', args=[self.exp2.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Expense.objects.filter(id=self.exp2.id).exists())

    def test_user_can_see_summary_of_their_expenses(self):
        self.client.force_login(self.user)
        res = self.client.get(self.summary_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(any(item['category'] == 'FOOD' for item in res.data))
        self.assertTrue(all(item['category'] in ['FOOD', 'TRAVEL', 'UTILITIES', 'MISC'] for item in res.data))

    def test_admin_can_see_summary_of_all_expenses(self):
        self.client.force_login(self.admin)
        res = self.client.get(self.summary_url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(any(item['category'] == 'MISC' and item['total'] == 300.0 for item in res.data))
