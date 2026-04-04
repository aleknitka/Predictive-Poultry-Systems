import salabim as sim
import PIL.Image as Image
from pydantic import BaseModel


def test_salabim_env():
    env = sim.Environment(trace=True)
    assert env is not None
    assert env.now() == 0


def test_pydantic_base_model():
    class TestModel(BaseModel):
        name: str
        value: int

    model = TestModel(name="test", value=123)
    assert model.name == "test"
    assert model.value == 123


def test_pillow_available():
    img = Image.new("RGB", (10, 10))
    assert img.size == (10, 10)
