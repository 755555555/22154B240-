# KPL赛事数据分析项目

## 项目概述
本项目用于爬取和分析王者荣耀职业联赛(KPL)赛事数据，包括比赛结果、战队表现和赛事热度分析。

## 环境配置
1. Python 3.8+
2. 安装依赖库：
```bash
pip install -r requirements.txt
```

## 文件说明

### 数据爬取
- `kpl_data_crawler.py`: 主爬虫脚本，从蜂鸟竞技网站获取KPL赛事数据
- `kpl_data_crawler[2-5].py`: 爬虫脚本的不同版本迭代

### 数据处理
- `data_analysis.py`: 数据预处理和分析脚本

### 可视化
- `visualization.py`: 数据可视化脚本
- `keshihua.py`: 综合可视化分析脚本

### 数据文件
- `kpl_matches_*.csv`: 各赛季的比赛数据CSV文件

## 使用说明
1. 运行爬虫获取最新数据：
```bash
python kpl_data_crawler.py
```
2. 分析数据：
```bash
python data_analysis.py
```
3. 生成可视化图表：
```bash
python visualization.py
```

