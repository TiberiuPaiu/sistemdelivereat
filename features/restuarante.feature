Feature: Creación de Restaurantes

  Scenario: Usuario partners añade un nuevo restaurante
    Given estoy autenticado como partner con el nombre de usuario "Tiberiu_test_bdd" y contraseña "tiberiu.1234"
    When añado un restaurante con los siguientes datos
      | nombre        | descripcion         | direccion        | numero | codigo_postal | pais   | ciudad   | img |
      | Restaurante 1 | Descripción 1       | España  | Valladolid   | 47011        | Calle del Universo    | 1      | restaurante-4.jpg |
    #Then debería ver el mensaje "El restaurante se creado exitosamente"
    Then debería ver el restaurante "Restaurante 1" en la lista de mis restaurantes