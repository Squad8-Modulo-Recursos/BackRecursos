Feature: Proyectos

    Feature Description

  Scenario: ver horas por proyecto
    Given un proyecto
    When consulto las horas trabajadas sin especificar el periodo
    Then se me mostraran las horas cargadas a todo el proyecto

    Given un proyecto 
    When consulto las horas trabajadas del proyecto en un periodo determinado 
    Then se me mostraran las horas cargadas al proyecto en ese periodo

    Given un proyecto sin horas cargadas 
    When consulto las horas trabajadas sin especificar el periodo
    Then se notificará que no hay horas cargadas

    Given un proyecto
    When consulto las horas trabajadas sin especificar el periodo
    Then se me mostraran las horas cargadas a todo el proyecto