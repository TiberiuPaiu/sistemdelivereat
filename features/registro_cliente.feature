Feature: Registro de Cliente en el Sistema
  Como usuario con el roll cliente
  Quiero registrarme como cliente en el sistema
  Para poder acceder a la sitema de envio de comida

  Scenario: Registro exitoso de un cliente
    Given estoy en la página de registro de clientes
    When lleno el formulario con los siguientes datos
      | nombre         | apellidos      | email            | telefono  | prefijo | username       | password     | pais    | ciudad       | codigo_postal| direccion          | numero |
      | Tiberiu        | Paiu           | tibi@ejemplo.com | 610344405 | +34     | tibi_user_test | Tiberiu.1234 | España  | Valladolid   | 47011        | Calle del Universo | 1      |
    And envío el formulario
    Then debería ver la página de inicio de sesión
    Then debería haber un username registrado con el username "tibi_user_test" con el siguiente rol "cliente"

  Scenario: Falla en el registro debido a dirección inválida
    Given estoy en la página de registro de clientes
    When lleno el formulario con los siguientes datos
    | nombre         | apellidos      | email            | telefono  | prefijo | username       | password     | pais    | ciudad       | codigo_postal| direccion          | numero |
    | Tiberiu        | Paiu           | tibi@ejemplo.com | 610344405 | +34     | tibi_user_test_2 | Tiberiu.1234 | España  | Valladolid   | 47011        | direccion_error    | 1      |
    And envío el formulario
    #Then debería ser redirigido a la página de registro de clientes
    Then debería ver la página de registro con el siguiente "No se encontró la dirección. Por favor ingrese la dirección."
    Then debería de no existir el usuario con el username "tibi_user_test"
