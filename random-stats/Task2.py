import pandas as pd
import numpy as np
import mip
import multiprocessing as mp

def init_model():
    model = mip.Model(sense=mip.MINIMIZE)
    boxes = {}
    for i in range(w):
        boxes[i] = {}
        for j in range(s):
            boxes[i][j] = model.add_var(name=f"W{i}S{j}", var_type=mip.INTEGER, lb=0)

    costs = [[4, 6, 9, 5, 8, 6], [5, 4, 7, 6, 4, 5], [6, 7, 4, 3, 6, 4]]
    model.objective = mip.xsum(
        costs[i][j] * boxes[i][j] for i in range(w) for j in range(s)
    )

    model += mip.xsum(boxes[0][j] for j in range(s)) <= 100
    model += mip.xsum(boxes[1][j] for j in range(s)) <= 80
    model += mip.xsum(boxes[2][j] for j in range(s)) <= 120
    return model, boxes

def find_sol(id, row):

    model, boxes = init_model()
    for j in range(len(row)):
        model += mip.xsum(boxes[i][j] for i in range(w)) == int(row[j])

    status = model.optimize()

    if status == mip.OptimizationStatus.OPTIMAL or status == mip.OptimizationStatus.FEASIBLE:
        result = (id, True, model.objective_value)
    else:
        result = (id, False, pd.NA)
    model.clear()
    return result

def sol_wrapper(args):

    return find_sol(*args)



if __name__ == "__main__":

    demand = {
        "Store": [f"S{n}" for n in range(6)],
        "Mean": [40, 50, 60, 30, 70, 50],
        "Std": [5, 6, 8, 4, 10, 6],
    }
    stores_df = pd.DataFrame(data=demand)

    N = 1000
    w = 3
    s = 6
    real_demand_df = pd.DataFrame({})
    for i in range(len(stores_df["Mean"])):
        real_demand_df[i] = np.random.normal(
            (stores_df["Mean"])[i], (stores_df["Std"])[i], N
        )

    with mp.Pool(processes= mp.cpu_count()) as pool:
        results = pool.map(sol_wrapper, real_demand_df.iterrows())

    res_df = pd.DataFrame(results, columns=["No", "Feasible", "Total"])

    '''
    for id, row in real_demand_df.iterrows():
        status, model = find_sol(id, row) 
        if status == mip.OptimizationStatus.OPTIMAL:
            res_df.loc[id] = [id, True, model.objective_value]
        else:
            res_df.loc[id] = [id, False, pd.NA]
        model.clear()
    '''
    print(res_df['Feasible'].value_counts(normalize=True) * 100)


