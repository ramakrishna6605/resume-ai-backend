from django.http import JsonResponse
class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = [
            '/api/auth/login/',
            '/api/auth/register/',
        ]
        if request.path.startswith('/api/auth/'):
            return self.get_response(request)
        print(f"METHOD: {request.method} | PATH: {request.path}")

        response = self.get_response(request)

        print(f"STATUS: {response.status_code}")

        return response