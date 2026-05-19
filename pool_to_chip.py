def add_pool_to_evo(pool_list,pool_names,evo):
    remain_list = []
    volume = 0
    max_vol = 820

    for pool in pool_list:
        if volume < max_vol:
            evo.add_pool(pool)
            pool_list.remove(pool)
        else:
            break
    if len(pool_list)>0:
        remain_list = pool_list
    return remain_list