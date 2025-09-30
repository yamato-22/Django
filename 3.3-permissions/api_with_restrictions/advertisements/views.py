from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(),IsOwnerOrStaffOrReadOnly()]
        return []

    def get_queryset(self):
        # Все опубликованные объявления за исключением черновиков
        base_queryset = Advertisement.objects.exclude(status = AdvertisementStatusChoices.DRAFT)

        if self.request.user.is_authenticated:
            # Автор видит свои объявления в черновике
            author_drafts = Advertisement.objects.filter(creator = self.request.user,
                                                         status=AdvertisementStatusChoices.DRAFT)
            return base_queryset | author_drafts
        else:
            # Неавторизованный пользователь видит только опубликованные объявления
            return base_queryset

