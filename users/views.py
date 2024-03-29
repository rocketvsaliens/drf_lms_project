from rest_framework import generics, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from lms.permissions import IsSelfUser
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    default_serializer = UserSerializer
    queryset = User.objects.all()
    perms_methods = {
        'create': [AllowAny],
        'update': [IsAuthenticated, IsSelfUser | IsAdminUser],
        'partial_update': [IsAuthenticated, IsSelfUser | IsAdminUser],
        'destroy': [IsAuthenticated, IsSelfUser | IsAdminUser],
    }

    def get_permissions(self):
        self.permission_classes = self.perms_methods.get(self.action, self.permission_classes)
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        password = serializer.validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('payed_lesson', 'payed_course')
    ordering_fields = ('date_of_payment',)
