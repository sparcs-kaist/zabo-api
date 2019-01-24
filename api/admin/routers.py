from rest_framework.routers import SimpleRouter
from .views import AdminViewSet

admin_router = SimpleRouter()


admin_router.register(
    prefix=r'admin',
    viewset=AdminViewSet,
)
