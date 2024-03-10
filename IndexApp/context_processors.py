def query(request):
    query = request.POST.get('query', None)
    return {'query': query}
