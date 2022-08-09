from . import utils

def custom_ctx(request):
    return {
        'categories': utils.categories
    }