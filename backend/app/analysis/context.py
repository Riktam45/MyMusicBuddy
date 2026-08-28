from dataclasses import dataclass

import numpy as np


@dataclass
class AnalysisContext:
    """
    Shared data for all AI analyzers.
    """

    audio: np.ndarray
    sample_rate: int

    features: dict