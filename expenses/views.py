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


CATEGORY_CHOICES = [
    ('FOOD', 'Food'),
    ('TRAVEL', 'Travel'),
    ('UTILITIES', 'Utilities'),
    ('MISC', 'Miscellaneous'),
]

class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    
    def get_queryset(self):
        if self.request.user.is_superuser:  # adding condition to generate queryset, for admin have access to all users,expenses
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user) #only athenticated user can access his expenses
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False,methods=['get'],url_path='summery')
    def summery(self,request):
        queryset=self.get_queryset()
        totals = queryset.values('category').annotate(total=Sum('amount')) # gettting the total amout for the available categories that user have
        total_dict = {item['category']:item['total'] for item in totals} #converting python object to dictionary
        summery =[]
        for code, label in CATEGORY_CHOICES:
            summery.append(
                {
                    'category':code,
                    'label':label,
                    'total':float(total_dict.get(code,0))
                }
            )    
        return Response(summery,status=status.HTTP_200_OK)
    