Feature: Example Variable Steps Feature

    Scenario: Load value into variable
        Given the value 1 is loaded into variable i
        Then the value of variable i is 1
        And the type of variable i is int

    Scenario: Load value into variable (alternative steps)
        Given i <- 1
        Then i equals 1
        And type(i) equals int

    Scenario Outline: Load different values into a variables
        Given the value <value> is loaded into variable <name>
        Then the value of variable <name> is <value>
        And the type of variable <name> is <type>

        Examples:
            | name | value      | type  |
            | v1   | -1         | int   |
            | v2   | False      | bool  |
            | v3   | 3.4        | float |
            | v4   | [1, 2]     | list  |
            | v5   | (3, 4, 5)  | tuple |
            | v6   | {'a': 'b'} | dict  |

    Scenario: Load table of values into variables
        Given the following variables are loaded
            | var | val        |
            | v1  | -1         |
            | v2  | False      |
            | v3  | 3.4        |
            | v4  | [1, 2]     |
            | v5  | (3, 4, 5)  |
            | v6  | {'a': 'b'} |
        Then v1 equals -1
        And v2 equals False
        And v3 equals 3.4
        And v4 equals [1, 2]
        And v5 equals (3, 4, 5)
        And v6 equals {'a': 'b'}
        And type(v1) equals int
        And type(v2) equals bool
        And type(v3) equals float
        And type(v4) equals list
        And type(v5) equals tuple
        And type(v6) equals dict

    Scenario: Unpack variable
        Given l1 <- [1, 2, 3]
        When the variable l1 is unpacked into (v1, v2, v3)
        Then v1 equals 1
        And v2 equals 2
        And v3 equals 3

    Scenario: Unpack variable (alternative step)
        Given l1 <- [1, "a", 3.5]
        When (v1, v2, v3) <- l1
        Then v1 equals 1
        And v2 equals "a"
        And v3 equals 3.5
        And type(v1) equals int
        And type(v2) equals str
        And type(v3) equals float

    Scenario: Access element
        Given l <- [1, 2, 3]
        And d <- {"a": 4, "b": 5}
        And t <- (6, 7, 8)
        When the element 0 of variable l is stored in new variable l0
        And the element "b" of variable d is stored in new variable db
        And the element 2 of variable t is stored in new variable t2
        Then l0 equals 1
        And db equals 5
        And t2 equals 8

    Scenario: Access element (alternative step)
        Given l <- [1, 2, 3]
        And d <- {"a": 4, "b": 5}
        And t <- (6, 7, 8)
        When l0 <- l[0]
        And db <- d["b"]
        And t2 <- t[2]
        Then l0 equals 1
        And db equals 5
        And t2 equals 8