from rest_framework.decorators import api_view
from rest_framework.response import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from .queryset import FarmaciasQuerySet

REQUEST_COUNT = Counter('django_http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

@api_view(['GET'])
def listar_farmacias(request):
    return FarmaciasQuerySet.listar_farmacias()

@api_view(['POST'])
def crear_farmacia(request):
    return FarmaciasQuerySet.crear_farmacia(request)

@api_view(['GET'])
def metrics_view(request):
    """
    Vista para exponer métricas en /metrics para Prometheus.
    """
    metrics_data = generate_latest()
    return Response(metrics_data, content_type=CONTENT_TYPE_LATEST)