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