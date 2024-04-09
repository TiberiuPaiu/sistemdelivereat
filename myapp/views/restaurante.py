from django.shortcuts import render, redirect


def mi_pagina_restaurante(request):
    return render(request, 'admin/list_restaurante.html')

def post_add_restaurante(request):

    if request.method == 'POST':


            return redirect('myapp:index')
    else:
        form = ""

    ruta_pagina = [
        {
            'text': "Lista de restaurantes",
            'link': "myapp:list_restaurantes",
        },

        {
            'text': "Añadir restaurante",
            'link': "",
        }
    ]

    title_pagina = [
        {
        'label_title': "Añadir el restaurante",
        'title_card': "Añadir el restaurante",
         }
    ]
    context = {
        'ruta_pagina': ruta_pagina,
        'title_pagina': title_pagina,
        'form': form
    }

    return render(request, 'admin/add_restaurante.html',  context)