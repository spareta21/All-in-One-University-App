from django.shortcuts import redirect

def auth_middleware(get_response):

    def middleware(request):
        # return_URL = request.META['PATH_INFO']
        if not request.session.get('user'):
            return redirect('login')

        response = get_response(request)
        return response

    return middleware