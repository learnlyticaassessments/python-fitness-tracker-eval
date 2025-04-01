
import numpy as np

def create_step_series(step_list: list) -> np.ndarray:
    #return np.array(step_list)
    #return np.array([1000, 3000, 5000])
    pass
def validate_steps(step_series: np.ndarray) -> bool:
    return np.issubdtype(step_series.dtype, np.integer) and np.all(step_series >= 0)

def compute_fitness_summary(step_series: np.ndarray) -> tuple:
    total = int(step_series.sum())
    avg = round(step_series.mean(), 2)
    max_val = int(step_series.max())
    return total, avg, max_val

def apply_bonus_points(step_series: np.ndarray) -> np.ndarray:
    bonus = step_series.copy()
    bonus[bonus >= 7000] += 100
    return bonus
