from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRAVEL', 'Travel'),
        ('UTILITIES', 'Utilities'),
        ('MISC', 'Miscellaneous'),
    ]

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,db_index=True)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return f"{self.title} - {self.amount}"

