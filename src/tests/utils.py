def assert_dicts(result, expected):
    """
    Assert that check that the dict result contains all keys in expected.
    And the values are the same.
    If a value in expected contains "*" the value in result can be any value.

    :param result: dict with result of the response
    :param expected: dict with subset
    """
    for key in expected.keys():
        assert key in result.keys(), key
        if not expected[key] == '*':
            assert result[key] == expected[key], key
