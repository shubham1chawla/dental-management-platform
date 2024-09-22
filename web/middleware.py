from django.http.response import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path

        # Avoid checking authentication for /admin and /api
        if path.startswith('/api') or path.startswith('/admin'):
            return view_func(request, *view_args, **view_kwargs)
        
        user = request.user

        # Checking if user is logged-in and trying to access the login page
        if user.is_authenticated and path.startswith('/login'):
            return HttpResponseRedirect(redirect_to='/')
        
        # Checking if user is not logged-in and trying to access any other page
        if not user.is_authenticated and not path.startswith('/login'):
            return HttpResponseRedirect(redirect_to='/login')
        
        return view_func(request, *view_args, **view_kwargs)
