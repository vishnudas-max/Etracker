from django.shortcuts import render
from rest_framework import viewsets
from .Serializers import ExpenseSerializer
from .models import Expense
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExpenseFilter
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAdminOrReadOnly


CATEGORY_CHOICES = [
    ('FOOD', 'Food'),
    ('TRAVEL', 'Travel'),
    ('UTILITIES', 'Utilities'),
    ('MISC', 'Miscellaneous'),
]

class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    
    def get_queryset(self):
        if self.request.user.is_superuser:  # adding condition to generate queryset, for admin have access to all users,expenses
            return Expense.objects.all().order_by('-id')
        return Expense.objects.filter(user=self.request.user).order_by('-id') #only athenticated user can access his expenses
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False,methods=['get'],url_path='summery')
    def summery(self,request):
        from decimal import Decimal
        from collections import defaultdict

        queryset = self.get_queryset()

        # Manual aggregation to ensure accuracy
        category_totals = defaultdict(lambda: Decimal('0'))

        for expense in queryset:
            category_totals[expense.category] += expense.amount

        print("=== Category Totals ===")
        for category, total in category_totals.items():
            print(f"{category}: {total}")

        # Build summary
        summary = []
        for code, label in CATEGORY_CHOICES:
            summary.append({
                'category': code,
                'label': label,
                'total': float(category_totals[code])
            })

        return Response(summary, status=status.HTTP_200_OK)