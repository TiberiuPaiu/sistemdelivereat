
Feature: Registro de Partners
  Como usuario con el roll partner
  Quiero registrarme como partner
  Para poder acceder a la sistema y a las funcionalidades de partners

  Scenario: Registro exitoso de partner
    Given estoy en la página de registro de partners
    When lleno el formulario de partners con los siguientes datos
      | username      | email             | password       | prefix_tel | telefono  | first_name | last_name | nombre_negocio  |
      | tibi_partner  | tibi@ejemplo.com  | Tiberiu.1234   | +34       | 600000000  | Test       | Partner   | Test Business   |
    And envío el formulario
    Then debería ver la página de inicio de sesión de partners
    And debería haber un username registrado con el username "tibi_partner" con el siguiente rol "partners"

  Scenario: Registro fallido de partner por no añadir achivos pdf
    Given estoy en la página de registro de partners
    When lleno el formulario de partners con los siguientes datos
    | username      | email             | password       | prefix_tel | telefono  | first_name | last_name | nombre_negocio  |
    | tibi_partner  | tibi@ejemplo.com  | Tiberiu.1234   | +34       | 600000000  | Test       | Partner   | Test Business   |
    And envío el formulario
    Then debería ver la página de registro con el siguiente "Es obligatorio añadir archivos de Licencias comerciales, permisos de salud y registros sanitarios"
    And debería de no existir el usuario con el username "tibi_partner"