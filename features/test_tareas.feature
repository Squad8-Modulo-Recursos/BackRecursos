Feature: Tareas


Scenario: ver horas por tarea 

    Given una tarea "A"
    When consulto las horas trabajadas de la tarea sin especificar el periodo
    Then se me mostraran las horas totales cargadas a la tarea

    Given una tarea "B"
    When consulto las horas trabajadas de la tarea en un periodo determinado 
    Then se me mostraran las horas cargadas a la tarea en ese periodo

    Given una tarea sin horas cargadas
    When consulto las horas trabajadas 
    Then se notificara que no hay horas cargadas a la tarea
    