from django.shortcuts import redirect


def user_required(ModelClass, methods=None):
    if methods is None:
        methods = ['GET', 'POST']

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            model_obj = ModelClass.objects.get(pk=pk)
            if request.method not in methods or model_obj.user.user_id == request.user.id:
                return view_func(request, pk, *args, **kwargs)
            return redirect('login')

        return wrapper

    return decorator
