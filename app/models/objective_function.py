from models.grasp_solution import GraspSolution

def objective_function(solution: GraspSolution) -> float:
    return len(solution.bins) * 100000 - solution.calculate_sum_of_squared_rectangules()