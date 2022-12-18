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
}


def main_view(request):
    context = {'dish_name_list': DATA.keys()}
    return render(request, 'calculator/main.html', context)


def recipe_view(request):
    dish = request.path[1:-1]
    persons = int(request.GET.get('servings', 1))
    context = {'dish': dish,
               'persons': persons,
               'dish_dict': {key: value * persons for key, value in DATA[dish].items()}}
    return render(request, 'calculator/index.html', context)

