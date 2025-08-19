from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def recipes(request, dish):
    count = request.GET.get("servings")
    if count:
        count = int(count)
    else:
        count = 1

    if dish in DATA:
        new_dict = {key: value * count for key, value in DATA[dish].items()}
        context = {'recipe': new_dict,
                   'dish': f' Заказн рецепт блюда: {dish}',
                   'count': f'Количество порций: {count}'
                   }
    else:
        context = {}
    return render(request, 'calculator/index.html', context)