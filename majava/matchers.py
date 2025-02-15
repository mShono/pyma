from typing import Optional


class Mismatch(Exception):
    def __init__(self, value, path, msg):
        self.value = value
        self.path = path
        self.msg = msg

    def prepend(self, path):
        self.path = f"{path}.{self.path}" if self.path else path
        return self

    def __str__(self):
        if not self.path:
            return f"{repr(self.value)} - {self.msg}"
        return f"Value {repr(self.value)} at {repr(self.path)} does not match: {self.msg}"


class Matcher:
    _mismatch = None

    def __eq__(self, other):
        try:
            self._match(other)
            self._mismatch = None
            return True
        except Mismatch as e:
            self._mismatch = e
            return False

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def _match(self, other) -> Optional[str]:
        pass


def _match(matcher, value):
    if isinstance(matcher, Matcher):
        return matcher._match(value)

    if isinstance(matcher, dict):
        if not isinstance(value, dict):
            raise Mismatch(value, "", f"invalid type - got '{type(value)}', expected 'dict'")
        if len(matcher) != len(value):
            raise Mismatch(value, "", f"invalid size - got {len(value)}, expected {len(matcher)}")
        
        for k, matcher_v in matcher.items():
            try:
                actual_v = value[k]
            except KeyError:
                raise Mismatch(value, "", f"expected '{k}' element is missing")
            try:
                _match(matcher_v, actual_v)
            except Mismatch as e:
                raise e.prepend(k)

    if matcher != value:
        raise Mismatch(value, "", f"{repr(value)} != {repr(matcher)}")







class And(Matcher):
    def __init__(self, *matchers):
        self.matchers = matchers

    def __and__(self, other):
        return And(*self.matchers, other)

    def __repr__(self):
        return '&'.join(repr(it) for it in self.matchers)

    def _match(self, other):
        for matcher in self.matchers:
            _match(matcher, other)


class Or(Matcher):
    def __init__(self, *matchers):
        self.matchers = matchers

    def __or__(self, other):
        return Or(*self.matchers, other)

    def __repr__(self):
        return '|'.join(repr(it) for it in self.matchers)

    def _match(self, other):
        mismatches = []
        for matcher in self.matchers:
            try:
                _match(matcher, other)
                return
            except Mismatch as e:
                mismatches.append(e)
        raise Mismatch(other, "", ", ".join(str(i) for i in mismatches))


class _Any(Matcher):
    def __eq__(self, other):
        return True
    def __repr__(self):
        return "<Any>"


Any = _Any()
