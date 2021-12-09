Feature: Usuarios


  Scenario: cargar horas
    Given un empleado
    When carga sus horas trabajadas en una tarea en una fecha determinada
    Then se cargan las horas empleadas en la fecha corresponidiente y se actualizan sus horas trabajas 

    Given un empleado
    When carga un numero negativo de horas trabajas a una tarea en una fecha determinado
    Then no se cargaran las horas
  Scenario: eliminar horas de un empleado

    Given un empleado "C"
    When quiere eliminar una carga de horas a una tarea 
    Then se borrara la carga de hora en el sistema
    
  Scenario: ver horas por empleado
    Given un empleado "A"
    When consulto sus horas trabajadas en un periodo determinado 
    Then se me mostraran las horas trabajadas en ese periodo

    Given un empleado "B"
    When consulto sus horas trabajadas sin especificar el periodo
    Then se me mostraran las horas totales cargadas al empleado

  Scenario: modificar horas de un empleado

    Given que ingrese una cantidad incorrecta de horas a una tarea
    When quiero modificarla ingrensando una nueva cantidad correcta
    Then se actualizara las horas en el sistema 

