import warnings
warnings.filterwarnings("ignore", message="Pandas requires version '1.3.6' or newer of 'bottleneck'")
import pandas as pd
import glob
import os
os.environ['USE_BOTTLENECK'] = '0'  # 禁用bottleneck加速

# 合并所有赛季数据
files = glob.glob('c:/Users/22154/Desktop/kpl/kpl_matches_*.csv')
dfs = [pd.read_csv(f) for f in files]
all_data = pd.concat(dfs)

# 数据清洗 - 修正日期解析问题
all_data['date'] = pd.to_datetime(all_data['date'], format='%Y-%m-%d%H:%M')  # 明确指定日期格式
all_data['score_home'] = all_data['score'].str.split(':').str[0].astype(int)
all_data['score_away'] = all_data['score'].str.split(':').str[1].astype(int)

# 计算每场比赛的热度指标
match_metrics = all_data.groupby(['date', 'home_team', 'away_team']).agg({
    'score_home': 'mean',
    'score_away': 'mean',
    'format': lambda x: (x == 'BO7').mean()  # 重要比赛比例
}).reset_index()
import os
os.environ['USE_BOTTLENECK'] = '0'  # 禁用bottleneck加速