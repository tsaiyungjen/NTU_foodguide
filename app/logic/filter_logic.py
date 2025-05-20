import pandas as pd
import numpy as np
import re
from datetime import datetime
class RestaurantFilter:
    def __init__(self, data_path):
        # 讀取CSV檔案
        try:
            self.df = pd.read_csv(data_path)
            # 將空值替換為None
            self.df = self.df.replace({pd.NA: None})
        except FileNotFoundError:
            raise FileNotFoundError("找不到資料檔案，請確認路徑是否正確")
        except Exception as e:
            raise Exception(f"載入資料時發生問題: {str(e)}")
        
        # 確保必要的欄位存在
        required_columns = ['name', 'address', 'rating', 'user_ratings_total', 
                          'lat', 'lng', 'price_level', 'location_label', 
                          'category_tag', 'opening_hours', 'map_url']
        for col in required_columns:
            if col not in self.df.columns:
                self.df[col] = None

    def filter_by_price(self, price_level):
        """根據價位篩選"""
        if not price_level:
            return self.df
        return self.df[self.df['price_level'].isin(price_level)]
    
    def filter_by_location(self, locations):
        """根據地區篩選"""
        if not locations:
            return self.df
        return self.df[self.df['location_label'].isin(locations)]
    
    def filter_by_type(self, types):
        """根據餐廳類型篩選"""
        if not types:
            return self.df
        return self.df[self.df['category_tag'].isin(types)]
    
    def filter_by_mood(self, mood):
        """根據心情模式篩選"""
        if not mood:
            return self.df
        
        mood_filters = {
            '吃點罪惡的': ['美式', '韓式', '炸物', '義式', '甜點', '港式'],
            '低熱量清爽健康': ['健康'],
            '趕時間吃快點': ['平價快食','便當'],
            '天氣很熱': ['冰店'],
            '天氣很冷': ['鍋物', '麵食'],
            '半夜肚子餓': ['宵夜', '炸物','甜點'],
            '聚餐': ['精緻聚餐', '咖啡廳', '早午餐', '打卡店'],
            '讀書辦公': ['咖啡廳'],
            '異國料理探險':['日式','美式', '韓式', '泰式', '印度料理', '義式', '越式料理', '港式'],
            '下午茶時光':['咖啡廳', '飲料','甜點']
        }
        
        types_to_filter = mood_filters.get(mood, [])
        mask = False
        for t in types_to_filter:
            mask = mask | (self.df['category_tag'].str.contains(t, na=False)) | (self.df['name'].str.contains(t, na=False))
        return self.df[mask]
    
    def parse_opening_hours(self, opening_hours_str):
        """解析營業時間字符串"""
        if not opening_hours_str or pd.isna(opening_hours_str):
            return None
        
        # 將營業時間按行分割
        lines = [line.strip() for line in opening_hours_str.split('\n') if line.strip()]
        schedule = {}
        
        for line in lines:
            # 使用正則表達式解析時間
            match = re.match(r'(\w+)\s*：\s*(\d{1,2}:\d{2})\s*-\s*(\w+)\s*(\d{1,2}:\d{2})', line)
            if match:
                day_start = match.group(1)
                time_start = match.group(2)
                day_end = match.group(3)
                time_end = match.group(4)
                
                # 轉換為時間對象
                try:
                    start_time = datetime.strptime(time_start, '%H:%M').time()
                    end_time = datetime.strptime(time_end, '%H:%M').time()
                    
                    # 處理跨日營業 (如 22:00 - 02:00)
                    if day_start != day_end:
                        end_time = datetime.strptime('23:59', '%H:%M').time()
                    
                    schedule[day_start] = (start_time, end_time)
                except:
                    continue
        
        return schedule
    
    def is_restaurant_open(self, restaurant, check_time=None):
        """檢查餐廳在指定時間是否營業"""
        if check_time is None:
            check_time = datetime.now().time()
        
        opening_hours = restaurant['opening_hours']
        if not opening_hours or pd.isna(opening_hours):
            return False
        
        # 獲取當前星期幾 (中文)
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekday_num = datetime.now().weekday()
        current_weekday = weekdays[weekday_num]
        
        # 解析營業時間
        schedule = self.parse_opening_hours(opening_hours)
        if not schedule or current_weekday not in schedule:
            return False
        
        start_time, end_time = schedule[current_weekday]
        
        # 檢查時間是否在營業時間內
        if start_time <= end_time:
            return start_time <= check_time <= end_time
        else:
            # 處理跨日營業 (如 22:00 - 02:00)
            return check_time >= start_time or check_time <= end_time
    
    def filter_by_opening_hours(self, df, check_time=None):
        """篩選營業中的餐廳"""
        if df.empty:
            return df
        
        mask = df.apply(lambda x: self.is_restaurant_open(x, check_time), axis=1)
        return df[mask]
    
    def sort_by_rating(self, df, ascending=False):
        """根據評分排序"""
        return df.sort_values('rating', ascending=ascending)
    
    def sort_by_popularity(self, df, ascending=False):
        """根據評分數量和評分綜合排序"""
        df = df.copy()
        # 將欄位轉為數字型別，若無法轉換則變為 NaN
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df['user_ratings_total'] = pd.to_numeric(df['user_ratings_total'], errors='coerce')
        
        # 填補缺漏資料，或將 NaN 改為 0 或其他預設值
        df['rating'] = df['rating'].fillna(0)
        df['user_ratings_total'] = df['user_ratings_total'].fillna(0)

        df['popularity_score'] = df['rating'] * np.log1p(df['user_ratings_total'])
        return df.sort_values('popularity_score', ascending=ascending)
    
    def get_random_restaurant(self, filters=None, mood=None, check_time=None):
        """隨機抽選一家餐廳"""
        if mood:
            filtered = self.filter_by_mood(mood)
        elif filters:
            filtered = self.apply_filters(filters)
        else:
            filtered = self.df
        
        if check_time is not None:
            filtered = self.filter_by_opening_hours(filtered, check_time)
        
        if len(filtered) == 0:
            return None
        return filtered.sample(1).iloc[0]
    
    def apply_filters(self, filters, check_time=None):
        """應用普通篩選條件"""
        filtered = self.df.copy()
        if 'price_level' in filters:
            filtered = self.filter_by_price(filters['price_level'])
        if 'location' in filters:
            filtered = self.filter_by_location(filters['location'])
        if 'type' in filters:
            filtered = self.filter_by_type(filters['type'])
        if check_time is not None:
            filtered = self.filter_by_opening_hours(filtered, check_time)
        return filtered
    
    def get_top_restaurants(self, n=10, filters=None, mood=None, check_time=None):
        """獲取熱門餐廳排行榜"""
        if mood:
            filtered = self.filter_by_mood(mood)
        elif filters:
            filtered = self.apply_filters(filters)
        else:
            filtered = self.df.copy()
        
        if check_time is not None:
            filtered = self.filter_by_opening_hours(filtered, check_time)
        
        return self.sort_by_popularity(filtered).head(n)
    
