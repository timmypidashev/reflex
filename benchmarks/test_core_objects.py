import reflex as rx


def test_component_fragment(benchmark):
    benchmark(rx.fragment)


def test_state_fields_000(benchmark):
    benchmark(rx.State)


def test_state_fields_001(benchmark):
    class _State(rx.State):
        f0: int

    benchmark(_State)


def test_state_fields_005(benchmark):
    class _State(rx.State):
        f0: int
        f1: int
        f2: int
        f3: int
        f4: int
        f5: int

    benchmark(_State)


def test_state_fields_010(benchmark):
    class _State(rx.State):
        f0: int
        f1: int
        f2: int
        f3: int
        f4: int
        f5: int
        f6: int
        f7: int
        f8: int
        f9: int

    benchmark(_State)
