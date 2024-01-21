import time
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from celery import shared_task

from .models import CustomUser, Organization, Event
from .serializers import CustomUserSerializer, OrganizationSerializer, EventSerializer


class EventFilter(filters.FilterSet):
    """Фильтры для мероприятий."""
    title = filters.CharFilter(lookup_expr='icontains', label='Название')
    organizations__title = filters.CharFilter(
        lookup_expr='icontains',
        label='Название организации'
    )
    date = filters.DateFilter(label='Дата', input_formats=['%Y-%m-%d'])

    class Meta:
        model = Event
        fields = ['title', 'organizations__title', 'date']


@shared_task
def create_event_async(data):
    time.sleep(60)

    serializer = EventSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.data


class EventView(generics.ListCreateAPIView):
    """Представление для просмотра и создания мероприятий."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        data = request.data
        result = create_event_async.delay(data)
        data = result.get()

        return Response(data, status=status.HTTP_201_CREATED)


class CreateUserView(generics.CreateAPIView):
    """Представление для создания пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
        user = CustomUser.objects.get(id=data['id'])

        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return response


class CreateOrganizationView(generics.CreateAPIView):
    """Представление для создания организации."""
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
