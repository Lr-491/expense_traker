"""
api/views.py

Ce fichier contient toutes les views de l'application API :

- CategoryViewSet : CRUD des catégories
- ExpenseViewSet : CRUD des dépenses (filtrées par utilisateur)
- RegisterView : Inscription d'un nouvel utilisateur
- CurrentUserView : Récupération des informations de l'utilisateur connecté
"""

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User

from .models import Category, Expense
from .serializers import (
    CategorySerializer,
    ExpenseSerializer,
    RegisterSerializer
)


# =====================================================
# CATEGORY VIEWSET
# =====================================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les catégories.

    Permet :
    - GET (liste des catégories)
    - POST (création)
    - PUT/PATCH (modification)
    - DELETE (suppression)

    Sécurisé : utilisateur doit être authentifié.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# =====================================================
# EXPENSE VIEWSET
# =====================================================

class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les dépenses.

    Fonctionnement :
    - Chaque utilisateur ne voit QUE ses propres dépenses
    - Lors de la création, la dépense est automatiquement liée à l'utilisateur connecté
    """

    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Obligatoire pour que le DRF Router fonctionne
    queryset = Expense.objects.all()

    def get_queryset(self):
        """
        Retourne uniquement les dépenses
        appartenant à l'utilisateur connecté.
        """
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Lors de la création d'une dépense,
        on associe automatiquement l'utilisateur connecté.
        """
        serializer.save(user=self.request.user)


# =====================================================
# REGISTER VIEW
# =====================================================

class RegisterView(generics.CreateAPIView):
    """
    Permet la création d'un nouvel utilisateur.

    Endpoint : POST /api/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# =====================================================
# CURRENT USER VIEW
# =====================================================

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Retourne les informations de l'utilisateur actuellement connecté.

    Endpoint : GET /api/me/

    Nécessite un token JWT valide dans le header :
    Authorization: Bearer <access_token>
    """

    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })