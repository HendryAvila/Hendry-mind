from .forms import SearchForm


def get_searchForm(request):
    return {'searchForm': SearchForm()}