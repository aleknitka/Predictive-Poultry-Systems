from predictive_poultry_systems.agents.behavior.bt.base import Status
from predictive_poultry_systems.agents.behavior.bt.composites import Sequence, Selector
from predictive_poultry_systems.agents.behavior.bt.leaves import (
    LambdaAction,
    LambdaCondition,
)


class MockContext:
    def __init__(self):
        self.tick_count = 0
        self.action_history = []


def test_sequence_success():
    context = MockContext()

    c1 = LambdaAction(name="c1", func=lambda ctx: Status.SUCCESS)
    c2 = LambdaAction(name="c2", func=lambda ctx: Status.SUCCESS)
    seq = Sequence(name="seq", children=[c1, c2])

    assert seq.tick(context) == Status.SUCCESS
    assert seq.last_running_index == 0


def test_sequence_failure():
    context = MockContext()

    c1 = LambdaAction(name="c1", func=lambda ctx: Status.SUCCESS)
    c2 = LambdaAction(name="c2", func=lambda ctx: Status.FAILURE)
    seq = Sequence(name="seq", children=[c1, c2])

    assert seq.tick(context) == Status.FAILURE


def test_sequence_running():
    context = MockContext()

    # State to simulate running
    state = {"ticks": 0}

    def running_action(ctx):
        state["ticks"] += 1
        if state["ticks"] < 3:
            return Status.RUNNING
        return Status.SUCCESS

    c1 = LambdaAction(name="c1", func=lambda ctx: Status.SUCCESS)
    c2 = LambdaAction(name="c2", func=running_action)
    c3 = LambdaAction(name="c3", func=lambda ctx: Status.SUCCESS)

    seq = Sequence(name="seq", children=[c1, c2, c3])

    # First tick: c1 success, c2 running
    assert seq.tick(context) == Status.RUNNING
    assert seq.last_running_index == 1

    # Second tick: c2 running (resumes from c2)
    assert seq.tick(context) == Status.RUNNING
    assert seq.last_running_index == 1

    # Third tick: c2 success, c3 success
    assert seq.tick(context) == Status.SUCCESS
    assert seq.last_running_index == 0


def test_selector_success():
    context = MockContext()

    c1 = LambdaAction(name="c1", func=lambda ctx: Status.FAILURE)
    c2 = LambdaAction(name="c2", func=lambda ctx: Status.SUCCESS)
    sel = Selector(name="sel", children=[c1, c2])

    assert sel.tick(context) == Status.SUCCESS


def test_selector_failure():
    context = MockContext()

    c1 = LambdaAction(name="c1", func=lambda ctx: Status.FAILURE)
    c2 = LambdaAction(name="c2", func=lambda ctx: Status.FAILURE)
    sel = Selector(name="sel", children=[c1, c2])

    assert sel.tick(context) == Status.FAILURE


def test_condition_node():
    context = MockContext()

    cond_true = LambdaCondition(name="true", func=lambda ctx: True)
    cond_false = LambdaCondition(name="false", func=lambda ctx: False)

    assert cond_true.tick(context) == Status.SUCCESS
    assert cond_false.tick(context) == Status.FAILURE


def test_serialization():
    # Verify that we can serialize and deserialize the tree
    c1 = LambdaAction(name="c1", func=lambda ctx: Status.SUCCESS)
    seq = Sequence(name="seq", children=[c1])

    # Note: Lambdas are not easily serializable with standard Pydantic
    # if we want to round-trip them as code, but the model structure is.
    # For real use, we'd use specific node types.
    json_data = seq.model_dump_json()
    assert '"name":"seq"' in json_data
    assert '"name":"c1"' in json_data
