import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取所有赛季数据
df_challenge = pd.read_csv('kpl_matches_2024_challenge.csv')
df_spring = pd.read_csv('kpl_matches_2024_spring.csv')
df_summer = pd.read_csv('kpl_matches_2024_summer.csv')
df_zongjuesai = pd.read_csv('kpl_matches_2024_zongjuesai.csv')
df_spring2025 = pd.read_csv('kpl_matches_2025_spring.csv')

# 合并所有数据
df_all = pd.concat([df_challenge, df_spring, df_summer, df_zongjuesai, df_spring2025], ignore_index=True)

# 数据预处理
def preprocess_data(df):
    # 处理日期时间
    # 修正日期格式问题
    df['date'] = df['date'].str.replace(r'(\d{4}-\d{2}-\d{2})(\d{2}:\d{2})', r'\1 \2', regex=True)
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek  # 周一为0，周日为6
    df['hour'] = pd.to_datetime(df['time']).dt.hour
    
    # 处理比分
    df[['home_score', 'away_score']] = df['score'].str.split(':', expand=True).astype(int)
    df['total_score'] = df['home_score'] + df['away_score']
    df['score_diff'] = abs(df['home_score'] - df['away_score'])
    
    # 判断比赛类型
    df['is_bo3'] = df['format'].str.contains('BO3').astype(int)
    df['is_bo5'] = df['format'].str.contains('BO5').astype(int)
    df['is_bo7'] = df['format'].str.contains('BO7').astype(int)
    df['is_bo9'] = df['format'].str.contains('BO9').astype(int)
    
    # 判断比赛结果类型
    df['is_close'] = (df['score_diff'] <= 1).astype(int)  # 比分接近的比赛
    
    return df

df = preprocess_data(df_all)

# 1. 赛事热度趋势分析
def plot_season_trend(df):
    # 按月份统计比赛数量
    monthly_matches = df.groupby(['year', 'month']).size().reset_index(name='matches')
    monthly_matches['date'] = monthly_matches.apply(lambda x: f"{x['year']}-{x['month']:02d}", axis=1)
    
    plt.figure(figsize=(14, 6))
    plt.plot(monthly_matches['date'], monthly_matches['matches'], marker='o', linestyle='-')
    plt.title('2024-2025赛季KPL每月比赛数量趋势', fontsize=15)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('比赛数量', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    # 按星期统计比赛数量
    weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
    weekday_matches = df['day_of_week'].value_counts().sort_index().rename(index=weekday_map)
    
    plt.figure(figsize=(10, 6))
    weekday_matches.plot(kind='bar', color='skyblue')
    plt.title('KPL比赛按星期分布', fontsize=15)
    plt.xlabel('星期', fontsize=12)
    plt.ylabel('比赛数量', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 按时间段统计比赛数量
    hour_matches = df['hour'].value_counts().sort_index()
    
    plt.figure(figsize=(10, 6))
    hour_matches.plot(kind='bar', color='lightgreen')
    plt.title('KPL比赛按时间段分布', fontsize=15)
    plt.xlabel('小时', fontsize=12)
    plt.ylabel('比赛数量', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()

plot_season_trend(df)

# 2. 战队表现与热度分析
def team_analysis(df):
    # 合并主客场数据，统计每支球队的比赛次数
    home_teams = df['home_team'].value_counts()
    away_teams = df['away_team'].value_counts()
    team_matches = home_teams.add(away_teams, fill_value=0).sort_values(ascending=False)
    
    # 统计战队胜率
    home_wins = df[df['home_score'] > df['away_score']]['home_team'].value_counts()
    away_wins = df[df['away_score'] > df['home_score']]['away_team'].value_counts()
    total_wins = home_wins.add(away_wins, fill_value=0)
    win_rates = (total_wins / team_matches).sort_values(ascending=False)
    
    # 比赛次数最多的10支战队
    plt.figure(figsize=(12, 6))
    team_matches.head(10).plot(kind='bar', color='royalblue')
    plt.title('比赛次数最多的10支战队', fontsize=15)
    plt.xlabel('战队', fontsize=12)
    plt.ylabel('比赛次数', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 胜率最高的10支战队
    plt.figure(figsize=(12, 6))
    win_rates.head(10).plot(kind='bar', color='green')
    plt.title('胜率最高的10支战队', fontsize=15)
    plt.xlabel('战队', fontsize=12)
    plt.ylabel('胜率', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 顶级战队之间的对决分析
    top_teams = team_matches.head(6).index.tolist()
    top_matches = df[(df['home_team'].isin(top_teams)) & (df['away_team'].isin(top_teams))]
    
    # 顶级战队之间的胜负关系
    plt.figure(figsize=(10, 8))
    sns.heatmap (
        pd.crosstab(
            top_matches['home_team'], top_matches['away_team'], 
                values=top_matches['home_score']-top_matches['away_score'], 
                aggfunc='mean'), cmap='coolwarm', center=0)
    plt.title('顶级战队之间平均净胜分', fontsize=15)
    plt.xlabel('客场战队', fontsize=12)
    plt.ylabel('主场战队', fontsize=12)
    plt.tight_layout()
    plt.show()

team_analysis(df)

# 3. 比赛类型与热度分析
def match_format_analysis(df):
    # 比赛类型分布
    format_counts = df['format'].value_counts()
    
    plt.figure(figsize=(10, 6))
    format_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                      colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title('比赛类型分布', fontsize=15)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()
    
    # 不同类型比赛的平均总得分
    format_scores = df.groupby('format')['total_score'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    format_scores.plot(kind='bar', color='orange')
    plt.title('不同类型比赛的平均总得分', fontsize=15)
    plt.xlabel('比赛类型', fontsize=12)
    plt.ylabel('平均总得分', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 不同类型比赛的激烈程度(比分接近的比赛比例)
    close_rate = df.groupby('format')['is_close'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    close_rate.plot(kind='bar', color='purple')
    plt.title('不同类型比赛的比分接近比例', fontsize=15)
    plt.xlabel('比赛类型', fontsize=12)
    plt.ylabel('比分接近比例', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()

match_format_analysis(df)

# 4. 时间因素对比赛热度的影响
def time_impact_analysis(df):
    # 不同时间段的比赛得分分布
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='hour', y='total_score', data=df)
    plt.title('不同时间段的比赛得分分布', fontsize=15)
    plt.xlabel('比赛开始时间(小时)', fontsize=12)
    plt.ylabel('总得分', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 周末和工作日的比赛数量对比
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    weekend_matches = df['is_weekend'].value_counts()
    
    plt.figure(figsize=(8, 6))
    weekend_matches.plot(kind='pie', labels=['工作日', '周末'], autopct='%1.1f%%', 
                        colors=['#66b3ff','#99ff99'], startangle=90)
    plt.title('周末与工作日的比赛分布', fontsize=15)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()
    
    # 不同月份的周末/工作日比赛比例
    month_weekend = df.groupby(['year', 'month', 'is_weekend']).size().unstack()
    month_weekend['weekend_ratio'] = month_weekend[1] / (month_weekend[0] + month_weekend[1])
    month_weekend['date'] = month_weekend.index.map(lambda x: f"{x[0]}-{x[1]:02d}")
    
    plt.figure(figsize=(12, 6))
    plt.plot(month_weekend['date'], month_weekend['weekend_ratio'], marker='o', linestyle='-', color='red')
    plt.title('不同月份的周末比赛比例变化', fontsize=15)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('周末比赛比例', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

time_impact_analysis(df)

# 5. 赛事阶段与热度分析
def season_stage_analysis(df):
    # 定义赛事阶段
    conditions = [
        (df['date'] < pd.to_datetime('2024-03-01')),
        ((df['date'] >= pd.to_datetime('2024-03-01')) & (df['date'] < pd.to_datetime('2024-06-01'))),
        ((df['date'] >= pd.to_datetime('2024-06-01')) & (df['date'] < pd.to_datetime('2024-09-01'))),
        ((df['date'] >= pd.to_datetime('2024-09-01')) & (df['date'] < pd.to_datetime('2024-12-01'))),
        (df['date'] >= pd.to_datetime('2024-12-01'))
    ]
    choices = ['春季赛常规赛', '春季赛季后赛', '夏季赛', '总决赛', '挑战赛']
    df['stage'] = np.select(conditions, choices)
    
    # 各阶段比赛数量
    stage_counts = df['stage'].value_counts()
    
    plt.figure(figsize=(10, 6))
    stage_counts.plot(kind='bar', color='teal')
    plt.title('各赛事阶段的比赛数量', fontsize=15)
    plt.xlabel('赛事阶段', fontsize=12)
    plt.ylabel('比赛数量', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 各阶段比赛类型分布
    stage_format = pd.crosstab(df['stage'], df['format'])
    
    plt.figure(figsize=(12, 6))
    stage_format.plot(kind='bar', stacked=True)
    plt.title('各赛事阶段的比赛类型分布', fontsize=15)
    plt.xlabel('赛事阶段', fontsize=12)
    plt.ylabel('比赛数量', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='比赛类型')
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 各阶段比赛激烈程度
    stage_close = df.groupby('stage')['is_close'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    stage_close.plot(kind='bar', color='darkorange')
    plt.title('各赛事阶段的比赛激烈程度', fontsize=15)
    plt.xlabel('赛事阶段', fontsize=12)
    plt.ylabel('比分接近比例', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()

season_stage_analysis(df)

# 6. 关键比赛分析
def key_matches_analysis(df):
    # 定义关键比赛( postseason, Finals, BO7及以上比赛)
    df['is_key'] = ((df['stage'].isin(['春季赛季后赛', '总决赛'])) | 
                   (df['is_bo7'] == 1) | (df['is_bo9'] == 1)).astype(int)
    
    # 关键比赛的时间分布
    key_time = df[df['is_key'] == 1]['hour'].value_counts().sort_index()
    
    plt.figure(figsize=(10, 6))
    key_time.plot(kind='bar', color='gold')
    plt.title('关键比赛的时间分布', fontsize=15)
    plt.xlabel('小时', fontsize=12)
    plt.ylabel('比赛数量', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 关键比赛与非关键比赛的得分对比
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='is_key', y='total_score', data=df)
    plt.title('关键比赛与非关键比赛的得分对比', fontsize=15)
    plt.xlabel('是否关键比赛', fontsize=12)
    plt.ylabel('总得分', fontsize=12)
    plt.xticks([0, 1], ['非关键比赛', '关键比赛'])
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()
    
    # 关键比赛中最活跃的战队
    key_teams = pd.concat([df[df['is_key'] == 1]['home_team'], 
                          df[df['is_key'] == 1]['away_team']]).value_counts().head(10)
    
    plt.figure(figsize=(12, 6))
    key_teams.plot(kind='bar', color='crimson')
    plt.title('关键比赛中出现次数最多的10支战队', fontsize=15)
    plt.xlabel('战队', fontsize=12)
    plt.ylabel('关键比赛次数', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    plt.tight_layout()
    plt.show()

key_matches_analysis(df)

# 7. 综合热度模型(简化版)
def popularity_model(df):
    # 计算每场比赛的热度得分(简化版)
    # 热度得分 = 基础分 + 比赛类型分 + 时间段分 + 战队热度分
    
    # 基础分
    df['popularity'] = 1
    
    # 比赛类型分
    df['popularity'] += df['is_bo3'] * 0.5
    df['popularity'] += df['is_bo5'] * 1
    df['popularity'] += df['is_bo7'] * 1.5
    df['popularity'] += df['is_bo9'] * 2
    
    # 时间段分(晚上比赛得分更高)
    df['popularity'] += np.where(df['hour'].between(19, 22), 1, 0)
    df['popularity'] += np.where(df['hour'].between(14, 18), 0.5, 0)
    
    # 周末加分
    df['popularity'] += df['is_weekend'] * 0.5
    
    # 关键比赛加分
    df['popularity'] += df['is_key'] * 1.5
    
    # 热门战队加分
    top_teams = pd.concat([df['home_team'], df['away_team']]).value_counts().head(10).index
    df['popularity'] += df['home_team'].isin(top_teams).astype(int) * 0.5
    df['popularity'] += df['away_team'].isin(top_teams).astype(int) * 0.5
    
    # 热门对决加分(两支都是热门战队)
    df['popularity'] += (df['home_team'].isin(top_teams) & 
                        df['away_team'].isin(top_teams)).astype(int) * 1
    
    # 热门月份(节假日月份)
    holiday_months = [1, 2, 5, 10]  # 假设这些月份有节假日
    df['popularity'] += df['month'].isin(holiday_months).astype(int) * 0.5
    
    # 标准化热度得分
    df['popularity'] = (df['popularity'] - df['popularity'].min()) / \
                        (df['popularity'].max() - df['popularity'].min()) * 100
    
    # 热度最高的10场比赛
    top_matches = df.sort_values('popularity', ascending=False).head(10)[
        ['datetime', 'home_team', 'away_team', 'score', 'format', 'popularity']]
    
    print("热度最高的10场比赛:")
    print(top_matches.to_string())  # 替换display()为print()
    
    # 热度随时间变化
    df['month_date'] = df['date'].dt.to_period('M').astype(str)
    month_popularity = df.groupby('month_date')['popularity'].mean()
    
    plt.figure(figsize=(14, 6))
    month_popularity.plot(marker='o', linestyle='-', color='darkviolet')
    plt.title('2024-2025赛季KPL每月平均热度变化', fontsize=15)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('平均热度得分', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

popularity_model(df)