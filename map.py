exit()
import requests
import time
#location = '43.0618,141.3545'  # 札幌の緯度経度
#location = '35.6938,139.7034'  # 新宿の緯度経度

# 東京23区の主要地点の緯度経度
locations = [
    '35.6895,139.6917',  # 新宿
    '35.7289,139.7105',  # 池袋
    '35.6580,139.7514',  # 六本木
    '35.7074,139.7749',  # 浅草
    '35.6735,139.5703',  # 渋谷
    '35.6997,139.7645',  # 上野
]

radius = 50000  # 検索範囲（最大50,000メートル）
type_place = 'restaurant'
min_reviews = 10  # 最低レビュー件数
n_low_rated = 10  # 取得する低評価店舗数

low_rated_places = []

for location in locations:
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type_place}&key={API_KEY}"

    while True:
        response = requests.get(url)
        places = response.json()

        # 評価があり、レビュー件数が一定以上の店を取得
        filtered_places = [
            (place['name'], place.get('rating', 0), place.get('user_ratings_total', 0))
            for place in places['results']
            if place.get('rating') and place.get('user_ratings_total', 0) >= min_reviews
        ]

        # 集めた結果を追加
        low_rated_places.extend(filtered_places)

        # 次のページトークンがある場合、次のページへ
        next_page_token = places.get('next_page_token')
        if not next_page_token:
            break  # 次のページがなければ終了

        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}"
        time.sleep(2)  # APIのリクエスト制限回避のために少し待つ

# 全ての結果を評価の低い順にソート
low_rated_places.sort(key=lambda x: x[1])

# 低評価の店舗を表示（指定数まで）
for name, rating, reviews in low_rated_places[:n_low_rated]:
    print(f"店名: {name}, 評価: {rating}, レビュー数: {reviews}")