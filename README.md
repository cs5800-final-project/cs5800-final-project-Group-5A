# cs5800-final-project

data sources:
1. Museums in Manhattan: https://overpass-turbo.eu/
    [out:json];
    area["name"="Manhattan"]->.manhattanArea;
    (
        node["tourism"="museum"](area.manhattanArea);
        way["tourism"="museum"](area.manhattanArea);
        relation["tourism"="museum"](area.manhattanArea);
    );
    out center;
    
    以上可导出geojson格式的file，同时手动删除了个别非纽约曼哈顿的数据。
    最后得到manhattan_ny_museums.geojson

    [geojson.io](https://geojson.io/)可导入geojson file看具体数据内容，或是下载成csv等其他格式

2. NYC airbnb open data
https://www.kaggle.com/datasets/vrindakallu/new-york-dataset


Algorithms：
以下两个算法都是用于find optimal airbnb，二选一即可。
- dijkstra: 
    计算从不同airbnb分别到每个museum的最短距离，从而计算出总距离最短的那个就是要选择的airbnb。
- greedy:
    可以自选criteria是啥，最简易的就是按距离，进阶版的可以同时考虑价格、rating等。
    算法好像比较简单粗暴：
    Calculate the distance from each Airbnb to each museum.
    Sum these distances for each Airbnb.
    Select the Airbnb with the smallest total distance to all museums.


这个作为optional的内容：
- MST(Kruskal/prim):
    假设一天之中打算逛完n个museum，计算从airbnb出发、陆续到达n个museum、返回airbnb的最短总路径。
