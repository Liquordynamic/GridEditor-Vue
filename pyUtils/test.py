import NHGridHelper as NH

if __name__ == '__main__':
    
    helper = NH.NHGridHelper('./testRes/gridInfo.json')
    helper.export('./output', './testRes/Dem/Digital Terrain Model.tif')
    # helper.export_shp('./output/shp1/node.shp', 10240, './testRes/Dem/Digital Terrain Model.tif', -9999)