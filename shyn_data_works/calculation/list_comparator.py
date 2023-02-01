from typing import List

def list_comparator(series_1:List[bool], series_2:List[bool]):
    stop_point = 0
    if len(series_1) != len(series_2): return
    
    for i in range(0, len(series_1)):
        if series_1[i] == series_2[i]:
            stop_point = i
        else: 
            return stop_point
        
    return "matches"