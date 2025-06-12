import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.fnscore.cn/league/kog-168.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'https://www.fnscore.cn/'
}

def get_match_data():
    data = []
    try:
        # 增加超时和重试机制
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        match_items = soup.select('.match-panel-item.match-table-item')
        
        for item in match_items:
            try:
                # 提取比赛时间
                time_ele = item.select_one('.time-txt')
                date = time_ele.text.split()[0]
                time_ = time_ele.select_one('.time-hour-txt').text
                
                # 提取战队信息
                home_team = item.select_one('.home-team .team-name').text.strip()
                away_team = item.select_one('.away-team .team-name').text.strip()
                
                # 提取比分
                score = item.select_one('.score').text.strip().replace(' ', '')
                
                # 提取赛制
                format_ = item.select_one('p[style="color: #9a9a9a;"]').text.strip()
                
                data.append({
                    'date': date,
                    'time': time_,
                    'home_team': home_team,
                    'away_team': away_team,
                    'score': score,
                    'format': format_
                })
                
                time.sleep(1)  # 增加延迟防止被封
                
            except Exception as e:
                print(f"解析单场比赛出错: {str(e)}")
                continue
                
    except requests.exceptions.RequestException as e:
        print(f"网络请求出错: {str(e)}")
    except Exception as e:
        print(f"其他错误: {str(e)}")
    
    return data

def save_to_csv(data):
    with open('kpl_matches_2024_challenge.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'date', 'time', 'home_team', 'away_team', 'score', 'format'
        ])
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    match_data = get_match_data()
    save_to_csv(match_data)
    print(f"成功保存{len(match_data)}条比赛数据")