# cs5800-final-project

data sources:
1. Museums in Manhattan: https://overpass-turbo.eu/
    [out:json];
    area[name="Manhattan"]->.searchArea;
    (
    node["tourism"="museum"](area.searchArea);
    node["addr:state"="NY"](area.searchArea);
    way["tourism"="museum"](area.searchArea);
    relation["tourism"="museum"](area.searchArea);
    );
    out center;
    
    以上可导出geojson格式的file，同时手动删除了个别非纽约曼哈顿的数据。
    最后得到manhattan_ny_museums.geojson

    [geojson.io](https://geojson.io/)可导入geojson file看具体数据内容

2. NYC airbnb open data
https://www.kaggle.com/datasets/vrindakallu/new-york-dataset