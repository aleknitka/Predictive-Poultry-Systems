import sys
from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    import salabim as sim


def setup_simulation_logger(env: "sim.Environment") -> None:
    """Configures loguru to include simulation time in every log entry.

    Args:
        env: The salabim environment to fetch current simulation time from.
    """
    # Use configure to apply the patch and add the handler globally.
    # Note: This removes all existing handlers, including the default one.
    logger.configure(
        patcher=lambda record: record["extra"].update({"sim_time": env.now()}),
        handlers=[
            {
                "sink": sys.stderr,
                "format": (
                    "<green>{time:HH:mm:ss.SSS}</green> | "
                    "<cyan>[{extra[sim_time]:>8.2f}]</cyan> | "
                    "<level>{level: <8}</level> | "
                    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
                ),
                "level": "INFO",
            }
        ],
    )

    logger.info("Simulation logger initialized with environment time integration.")
