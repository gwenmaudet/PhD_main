import numpy as np
# from scipy.spatial.distance import cosine
from dtw import dtw, accelerated_dtw
import conf
import statistics
import math


def Dynamic_time_warping(x, y, dist=conf.dist, warp=conf.warp):
    """
    exple x and y arrays :
    x = np.random.rand(1000).reshape(-1,1)
    y = np.random.rand(1000).reshape(-1,1)

    :param array x: N1*M array
    :param array y: N2*M array
    :param string or func dist: distance parameter for cdist. When string is given, cdist uses optimized functions for the distance metrics.
    If a string is passed, the distance function can be 'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean',
     'hamming', 'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'wminkowski', 'yule'.
    :param int warp: how many shifts are computed.
    here warp = 3 considered that to have good results, you should at least have
    """
    d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(x, y, dist, warp=warp)
    return d, cost_matrix, acc_cost_matrix, path






def proportion_of_an_interval_into_another_one(inter1, inter2): #proportion of the inter1 into the inter 2
    inter2_len = (inter2[1] - inter2[0])
    if inter1[1]<inter2[0] or inter1[0]>inter2[1]:
        return 0
    elif inter1[0] > inter2[0] and inter1[1]<inter2[1]:
        return (inter1[1] - inter1[0]) * 100 / inter2_len
    elif inter1[0] < inter2[0] and inter1[1] > inter2[1]:
        return 100
    elif inter1[0] < inter2[0]:
        return (inter1[1] - inter2[0]) / inter2_len
    elif inter1[1] > inter2[1]:
        return (inter2[1] - inter1[0]) / inter2_len
    else:
        print("ERROR")
        return
def inter_inclusions_of_confidence_intervals(inter1, simulation):
    T_prim = statistics.mean(simulation)
    std_prim = statistics.pstdev(simulation)
    prop = 1.96 * std_prim / math.sqrt(len(simulation))
    inter2 = (T_prim - prop, T_prim + prop)
    print(inter2)
    return proportion_of_an_interval_into_another_one(inter1, inter2)

