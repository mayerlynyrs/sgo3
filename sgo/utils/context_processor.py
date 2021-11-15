"""Utils Context Processor"""


def menu(request):
    path = request.path
    paths = path.split('/')
    #print(paths)
    #del paths[0]    # Se elimina el primero de la lista que es vacio.
    #del paths[-1]
    # Elimino todos los elementos vacios de la lista
    paths = [elemento for elemento in paths if elemento != '']
    # Elimino todos los numeros de la lista
    paths = [elemento for elemento in paths if not elemento.isdigit()]

    app = 'home'
    module = None
    page = None

    # print(path)
    # print(paths)
    # print(len(paths))
    # print(paths[-1])

    if len(paths) > 1:
        app = paths[0]
        page = paths[-1]
        if page != paths[1]:
            module = paths[1]
    elif len(paths) == 1:
        app = paths[0]

    return {'menu': path,
            'menu_app': app,
            'menu_module': module,
            'menu_page': page
            }
