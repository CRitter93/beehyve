Feature: Test monkeypatching

    @monkeypatch
    Scenario: Monkeypatch non-existing environment variable
        Given the value of environment variable ENV_C is monkeypatched to def
        Then the value of environment variable ENV_C is def

    @monkeypatch
    Scenario: Monkeypatch non-existing environment variable (alternative step)
        Given env(ENV_C) <-monkeypatch- def
        Then env(ENV_C) equals def

    @dummy_env
    @monkeypatch
    Scenario: Monkeypatch existing environment variable
        Given env(ENV_A) <-monkeypatch- 3
        Then env(ENV_A) equals 3
        And env(ENV_B) equals abc

    @monkeypatch
    Scenario: Monkeypatch a constant with a value
        Given the attribute SOME_CONSTANT of module features.example_functions is monkeypatched to "xyz"
        When constant_value <- features.example_functions.get_some_constant()
        Then constant_value equals "xyz"

    @monkeypatch
    Scenario: Monkeypatch a constant with a value (alternative step)
        Given features.example_functions[SOME_CONSTANT] <-monkeypatch- "xyz"
        When constant_value <- features.example_functions.get_some_constant()
        Then constant_value equals "xyz"

    @monkeypatch
    Scenario: Monkeypatch a property
        Given the attribute some_property of object SomeObject of module features.example_functions is monkeypatched to "xyz"
        When property_value <- features.example_functions.get_some_property_from_some_object()
        Then property_value equals "xyz"

    @monkeypatch
    Scenario: Monkeypatch a property (alternative step)
        Given features.example_functions.SomeObject[some_property] <-monkeypatch- "xyz"
        When property_value <- features.example_functions.get_some_property_from_some_object()
        Then property_value equals "xyz"

    @monkeypatch
    Scenario: Monkeypatch a constant with another constant
        Given the attribute SOME_CONSTANT of module features.example_functions is monkeypatched to object ANOTHER_CONSTANT of module features.example_functions
        When constant_value <- features.example_functions.get_some_constant()
        Then constant_value equals "tuvxyz"

    @monkeypatch
    Scenario: Monkeypatch a constant with another constant (alternative step)
        Given features.example_functions[SOME_CONSTANT] <-monkeypatch- features.example_functions.ANOTHER_CONSTANT
        When constant_value <- features.example_functions.get_some_constant()
        Then constant_value equals "tuvxyz"

    @monkeypatch
    Scenario: Monkeypatch a property with another function
        Given the attribute some_property of object SomeObject of module features.example_functions is monkeypatched to object SOME_CONSTANT of module features.example_functions
        When property_value <- features.example_functions.get_some_property_from_some_object()
        Then property_value equals "abcdef"

    @monkeypatch
    Scenario: Monkeypatch a property with another function (alternative step)
        Given features.example_functions.SomeObject[some_property] <-monkeypatch- features.example_functions.SOME_CONSTANT
        When property_value <- features.example_functions.get_some_property_from_some_object()
        Then property_value equals "abcdef"

    @monkeypatch
    Scenario: Monkeypatch an object with another object
        Given features.example_functions[SomeObject] <-monkeypatch- features.example_functions.AnotherObject
        When property_value <- features.example_functions.get_some_property_from_some_object()
        Then property_value equals 987654

    @monkeypatch
    Scenario: Monkeypatch a function with another function
        Given features.example_functions[get_some_constant] <-monkeypatch- features.example_functions.return_abc
        When constant_value <- features.example_functions.get_some_constant()
        Then constant_value equals "abc"
