#coding:utf-8
'''
Created on 2017年10月30日
@author: heyuanhao
'''
import numpy as np
import math

NOISE = 'NOISE'
UNCLUSTERED = False

def distance(str1, str2):
    """Implementation of Distance Calculation of various types 
       calculate the Levenshtein Distance
    """
    assert type(str1) == str and type(str2) == str, 'vec1/vec2 must be string type when dist_type is Lev'
    cnt = 0.0
    for i in range(0, min(len(str1), len(str2))):
        if str1[i] == str2[i]: cnt += 1.0
    return 1- cnt / max(len(str1), len(str2))    #more less, more similarity

def eps_region(datas, point_id, eps):
    ''' Implementation of calculate EPS region of pt_id'''
    seeds = []
    points_num = len(datas)
    for i in range(0, points_num):
        #print datas[point_id], datas[i], distance(datas[i], datas[point_id])
        if distance(datas[i], datas[point_id]) <= eps:
            seeds.append(i)
    return seeds

def expand_cluster(datas, cluster_list, cluster_id, point_id, eps, minpts):  
    seeds = eps_region(datas, point_id, eps)
    #print seeds
    if len(seeds) < minpts: 
        cluster_list[point_id] = NOISE
        return False
    else:
        cluster_list[point_id] = cluster_id
        for seed_id in seeds:
            cluster_list[seed_id] = cluster_id
        
        while len(seeds) > 0:
            current_point_id = seeds[0]
            current_seeds = eps_region(datas, current_point_id, eps)
            if len(current_seeds) >= minpts:
                for i in range(0, len(current_seeds)):
                    delta_point_id = current_seeds[i]
                    if cluster_list[delta_point_id] == UNCLUSTERED or cluster_list[delta_point_id] == NOISE:
                        if cluster_list[delta_point_id] == UNCLUSTERED:
                            seeds.append(delta_point_id)
                            cluster_list[delta_point_id] = cluster_id
            seeds = seeds[1:] 
    return True

def dbscan(datas, eps, minpts):
    '''Implementation of DBSCAN clutering
    Inputs：
        datas     - if dist_type is 'Lev', datas must be a list of string. eg.['abc', 'bcd'];
                    other dist_type value, datas must be a matrix whose columns are points and rows are features
        dist_type - such as 'Lev', 'Euc'
        eps       - maximum value of two points to be regionally related
        minpts    - minimum number of points to make a cluster
    
    Outputs：
            An array with either a cluster id number or dbscan.NOISE for each column vector in datas
    '''
    cluster_id = 1
    points_num = len(datas)
    cluster_list = [UNCLUSTERED] * points_num
    for point_id in range(0, points_num):
        if cluster_list[point_id] == UNCLUSTERED:
            if expand_cluster(datas, cluster_list, cluster_id, point_id, eps, minpts):
                cluster_id += 1
    return cluster_list
    
if __name__=='__main__':
    datas_lev = ['abc','abce','accd','def','deh','ghkef']
    #print datas_lev
    eps = 0.5 
    minpts = 2
    
    cluster_ids = dbscan(datas_lev, eps, minpts)
    print cluster_ids
    
    