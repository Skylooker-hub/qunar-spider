from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType
import csv


class City(object):
    def __init__(self):
        self.cityName = None
        self.hotValue = None


def load_file():
    # 打开csv文件
    with open('result.csv', 'r', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        cityList = []
        # 根据规则读取文件中的每一行文字
        for line in reader:
            if len(line[0].split('·')) > 1:
                city = City()
                city.cityName = line[0].split('·')[1]
                city.hotValue = float(line[5].split(' ')[1])
                foundRepeatCity = 0
                # 获取城市名字cityName和热度信息hotValue
                # 针对城市名字cityName做聚合操作，也就是针对其做热点求和
                for originCity in cityList:
                    if originCity.cityName == city.cityName:
                        originCity.hotValue = originCity.hotValue + city.hotValue
                        foundRepeatCity += 1
                        break
                # 过滤城市列表中 没有在echart 备案过的城市
                if foundRepeatCity == 0 and Geo().get_coordinate(name=city.cityName) is not None and int(
                        city.hotValue) != 0:
                    cityList.append(city)
        # 生成输出信息，用来传入到echarts中
        outputGeoData = []
        for city in cityList:
            if Geo().get_coordinate(name=city.cityName) is not None and int(city.hotValue) != 0:
                outputGeoDataRecord = (city.cityName, int(city.hotValue)*5)
                outputGeoData.append(outputGeoDataRecord)
        print(outputGeoData)
    return outputGeoData


def geo_base(data) -> Geo:
    c = (
        # 初始化地理热点图
        Geo()
        .add_schema(maptype='china')
        .add('2019国庆旅游热力图', data, ChartType.HEATMAP)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title='2019国庆旅游热力图'),
        )
    )
    c.render()
    return c


if __name__ == '__main__':
    geo_base(load_file())
