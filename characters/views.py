from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from extraction_core.executer import retreive_new_collection
from extraction_core.storage_handler import save_clear_data_to_storage


async def get_characters(request, character_page):
    queryset = await retreive_new_collection(
        settings.CONFIG,
        character_page,
        tuple(request.GET.keys())
    )
    results = tuple(
        item.dict(exclude_none=True)
        for item in queryset
    )
    columns = tuple(next(iter(results), []).keys())
    return render(
        request,
        'fetches.html',
        context={
            "results": results,
            "columns": columns
        },
    )


async def download_file(request, character_page):
    results = await retreive_new_collection(
        settings.CONFIG,
        character_page,
        tuple(request.GET.keys())
    )
    path, filename = save_clear_data_to_storage(
        settings.CONFIG.file_storage,
        results,
    )
    with open(path,'r') as file:
        data = file.read()
    resp = HttpResponse(data, content_type='application/x-download')
    resp['Content-Disposition'] = f'attachment;filename={filename}'
    return resp