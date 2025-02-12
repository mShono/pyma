from majava.matchers import Matcher, Mismatch, _match


class DictContains(Matcher):
    """ Matches, if a dict contains expected subset of key-value pairs
    """

    def __init__(self, expected, *, recursive=True):
        self.expected = expected
        self.recursive = recursive

    def __repr__(self):
        return f"DictContains({repr(self.expected)})"

    def _match(self, other):
        for k, val in self.expected.items():
            if k not in other:
                raise Mismatch(other, k, f"key '{k}' not found")
            actual_val = other[k]
            try:
                if self.recursive and isinstance(val, dict):
                    val = DictContains(val)
                _match(val, actual_val)
            except Mismatch as e:
                raise e.prepend(k)


class InInterval:
    # The matcher matches, if a given value (other) lies in the interval

    def __init__(self, *value):
        self.first_value, self.second_value = value

    def __eq__(self, other):
        if self.first_value is None:
            return other <= self.second_value
        if self.second_value is None:
            return self.first_value <= other
        return self.first_value <= other <= self.second_value

    def __repr__(self):
        return f"{self.first_value}, {self.second_value}"


class IsType:
    def __init__(self, *types):
        self.types = types

    def __eq__(self, other):
        return isinstance(other, self.types)

    def __repr__(self):
        return ', '.join(it.__name__ for it in self.types)


class AnyOf:
    """Actual value must match at least one of the expected values."""

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value in other

    def __repr__(self):
        return repr(self.value)
    

class SimilarList:
    """List must match the other list no matter the order"""

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if len(set(self.value)) == len(set(other)):
            common_issues = [i for i in self.value if i in other]
            if len(set(common_issues)) == len(set(other)):
                return common_issues
    
    def __repr__(self):
        return repr(self.value)
