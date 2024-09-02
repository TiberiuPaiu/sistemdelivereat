Feature: Login de Usuario
  Quiero iniciar sesión en mi apartado correspondiente a mi rol


  Scenario: Login exitoso de usuario registrado
    Given estoy en la página de inicio de sesión
    Given existen las sigentes cuentas registradas en el sistema
    |rol  | username| password|
    | cliente | tibi_cliente_test| Tiberiu.1234 |
    | partners | tibi_partners_test| Tiberiu.1234 |
    | cocina | tibi_cocina_test| Tiberiu.1234 |
    | repartidor | tibi_repartidor_test| Tiberiu.1234 |
    When ingreso mis credenciales
      | username | password |
      | tibi_cliente_test| Tiberiu.1234 |
      | tibi_partners_test| Tiberiu.1234 |
      | tibi_cocina_test| Tiberiu.1234 |
      | tibi_repartidor_test| Tiberiu.1234 |
    And presiono el botón de iniciar sesión
    Then debería ser redirigido a la página corespodiente a mi rol
     | rol         | url                              |
    | cliente     | restaurantes_list_cliente         |
    | partners    | restaurantes_list                 |
    | cocina      | pedidos_actualizados              |
    | repartidor  | pedidos_repartidor                |

    Scenario: el nombre de usuario no registrado no puede iniciar sesión
    When inicio sesión como usuario "inexistente" con contraseña "contraseña"
    And presiono el botón de iniciar sesión
    Then debería ver la página de login con el siguiente mensaje "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas."

  Scenario: error tipográfico incorrecto, el usuario registrado no puede iniciar sesión
    Given existe un usuario "nombredeusuario" con contraseña "contraseña"
    When inicio sesión como usuario "nombredeusuario" con contraseña "contraseña incorrecta"
    And presiono el botón de iniciar sesión
    Then debería ver la página de login con el siguiente mensaje "Por favor, introduzca un nombre de usuario y clave correctos. Observe que ambos campos pueden ser sensibles a mayúsculas."



