# TMAP API 모듈

TMAP API를 쉽게 사용할 수 있는 Python 모듈입니다.

## 설치

```bash
# 필요한 패키지 설치
pip install requests
```

프로젝트에 tmap_api 폴더를 복사하여 사용하시면 됩니다.

## 사용 방법

### 기본 사용법

```python
from tmap_api import TmapAPI

# API 키로 클라이언트 초기화
tmap = TmapAPI(app_key="여기에_API_키_입력")

# POI 검색 예시
search_result = tmap.search_poi_keyword("경복궁")
if search_result:
    pois = search_result.get("searchPoiInfo", {}).get("pois", {}).get("poi", [])
    if pois:
        print(f"검색 결과: {len(pois)}개 항목 찾음")
        for i, poi in enumerate(pois[:3]):  # 처음 3개만 출력
            name = poi.get("name", "")
            address = f"{poi.get('upperAddrName', '')} {poi.get('middleAddrName', '')} {poi.get('lowerAddrName', '')}"
            print(f"{i+1}. {name}: {address}")
```

### 지오코딩 (주소 → 좌표)

```python
# 주소로 좌표 찾기 예시
address = "서울특별시 중구 세종대로 110"  # 서울시청 주소
geocoding_result = tmap.geocoding(address)
if geocoding_result:
    coords = geocoding_result.get("coordinateInfo", {}).get("coordinate", [])
    if coords and len(coords) > 0:
        lat = coords[0].get("lat")
        lon = coords[0].get("lon")
        print(f"위도: {lat}, 경도: {lon}")
```

### Full Text 지오코딩 (자유 형식 텍스트 → 좌표)

```python
# 자유 형식 텍스트 주소로 좌표 찾기
free_text = "서울시청"
full_geocoding_result = tmap.full_text_geocoding(free_text)
if full_geocoding_result:
    addresses = full_geocoding_result.get("coordinateInfo", {}).get("coordinate", [])
    if addresses and len(addresses) > 0:
        lat = addresses[0].get("lat")
        lon = addresses[0].get("lon")
        print(f"위도: {lat}, 경도: {lon}")
        
        # 도로명 주소 정보도 함께 제공됨
        new_address = addresses[0].get("newAddressList", {}).get("newAddress", [])
        if new_address and len(new_address) > 0:
            road_address = new_address[0].get("fullAddressRoad", "")
            print(f"도로명 주소: {road_address}")
```

### 역지오코딩 (좌표 → 주소)

```python
# 좌표로 주소 찾기 예시
lat, lon = 37.566826, 126.9786567  # 서울시청 좌표
address_info = tmap.reverse_geocoding(lat, lon)
if address_info:
    print(f"주소: {address_info.get('addressInfo', {}).get('fullAddress', '')}")
```

### 보행자 경로 안내

```python
# 보행자 경로 예시
# 서울시청에서 덕수궁까지의 보행자 경로
start_x, start_y = 126.9786567, 37.566826  # 서울시청
end_x, end_y = 126.9753, 37.5668  # 덕수궁
route_info = tmap.pedestrian_route(start_x, start_y, end_x, end_y)
if route_info:
    total_distance = route_info.get("features", [{}])[0].get("properties", {}).get("totalDistance", 0)
    total_time = route_info.get("features", [{}])[0].get("properties", {}).get("totalTime", 0)
    print(f"거리: {total_distance}m, 예상 소요시간: {total_time//60}분 {total_time%60}초")
```

### 정적 지도 생성

```python
# 경로 정적 지도 생성
tmap.static_map(start_x, start_y, end_x, end_y, "seoul_city_hall_to_deoksugung.png")
```

### 자동차 경로 안내

```python
# 자동차 경로 안내
car_route = tmap.car_route(start_x, start_y, end_x, end_y)
if car_route:
    # 결과 처리
    features = car_route.get("features", [])
    if features:
        properties = features[0].get("properties", {})
        total_distance = properties.get("totalDistance", 0)
        total_time = properties.get("totalTime", 0)
        total_fare = properties.get("totalFare", 0)
        print(f"자동차 경로: 거리 {total_distance}m, 시간 {total_time//60}분, 요금 {total_fare}원")
```

### 타임머신 자동차 경로 안내

지정한 시간(미래 또는 과거)을 기준으로 교통 상황을 예측하여 경로를 안내합니다.

```python
from datetime import datetime, timedelta

# 내일 오전 9시 출발 기준으로 경로 탐색 (한국 시간 KST 기준)
tomorrow = datetime.now() + timedelta(days=1)
departure_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0, 0)

# 서울시청에서 강남역까지 타임머신 경로 요청
start_x, start_y = 126.9786567, 37.566826  # 서울시청
end_x, end_y = 127.0282, 37.4979  # 강남역

time_machine_route = tmap.time_machine_route(
    start_x=start_x, 
    start_y=start_y, 
    end_x=end_x, 
    end_y=end_y, 
    departure_time=departure_time,  # datetime 객체 또는 'YYYY-MM-DD hh:mm:ss' 형식 문자열
    search_option="0",              # 추천 경로
    arrival_option="0",             # 0: 출발 시간 기준, 1: 도착 시간 기준
    use_kst=True                    # 한국 시간대(KST) 사용 여부 (True: 사용, False: 사용 안함)
)

if time_machine_route:
    properties = time_machine_route.get("features", [{}])[0].get("properties", {})
    total_distance = properties.get("totalDistance", 0)
    total_time = properties.get("totalTime", 0)
    print(f"예상 거리: {total_distance}m, 예상 소요시간: {total_time//60}분")
```

#### 타임머신 경로 안내 시간대 설정

타임머신 경로 안내 기능은 기본적으로 한국 시간대(KST, UTC+9)를 사용합니다. 시간대 처리에 대한 상세 설명:

- `use_kst=True` (기본값): 입력한 datetime 객체를 한국 시간(KST)으로 간주하여 처리합니다.
- `use_kst=False`: 입력한 datetime 객체를 로컬 시간으로 간주합니다.
- 시간대 정보가 있는 datetime 객체를 전달하면, 자동으로 적절한 변환이 이루어집니다.
- 문자열로 시간을 입력할 경우 'YYYY-MM-DD hh:mm:ss' 형식을 사용하세요. 이 경우 시간대 변환이 적용되지 않습니다.

### Puzzle 장소 혼잡도 조회

TMAP의 Puzzle API를 사용하여 특정 장소 또는 주변 지역의 실시간 혼잡도를 조회할 수 있습니다.

#### 1. 키워드로 장소 혼잡도 검색

```python
# 키워드로 장소 혼잡도 검색
result = tmap.poi_congestion_by_keyword(
    keyword="명동",            # 검색 키워드
    lat=37.5637,              # 중심 위도 (선택적)
    lon=126.9838,             # 중심 경도 (선택적)
    radius=1000,              # 검색 반경 (미터)
    count=5                   # 검색 결과 최대 개수
)

if result:
    places = result.get("places", [])
    if places:
        for place in places:
            name = place.get("name", "")
            congestion_level = place.get("congestionLevel", "")  # 혼잡도 레벨 (1~4)
            congestion_text = place.get("congestionText", "")    # 혼잡도 텍스트 (여유, 보통, 약간 혼잡, 매우 혼잡)
            address = place.get("address", "")
            print(f"{name} - 혼잡도: {congestion_text}({congestion_level})")
            print(f"주소: {address}")
```

#### 2. 좌표 기반 주변 장소 혼잡도 검색

```python
# 좌표 주변 장소 혼잡도 검색
nearby_result = tmap.poi_congestion_by_coordinates(
    lat=37.566826,            # 위도
    lon=126.9786567,          # 경도
    radius=500                # 검색 반경 (미터)
)

if nearby_result:
    places = nearby_result.get("places", [])
    if places:
        for place in places:
            name = place.get("name", "")
            congestion_level = place.get("congestionLevel", "")
            congestion_text = place.get("congestionText", "")
            distance = place.get("distance", 0)  # 중심 좌표로부터의 거리 (미터)
            print(f"{name} - 혼잡도: {congestion_text}({congestion_level}), 거리: {distance}m")
```

#### 3. 특정 장소 ID로 혼잡도 조회

```python
# 특정 장소 ID로 혼잡도 조회
# POI ID는 POI 검색 결과에서 얻거나 TMAP API 개발자 포털에서 확인 가능
poi_congestion = tmap.realtime_place_congestion(
    poi_id="1000",            # 장소 ID (POI ID)
    radius=100                # 주변 장소 검색 반경 (미터), 0이면 주변 장소 검색 안함
)

if poi_congestion:
    place = poi_congestion.get("place", {})
    if place:
        name = place.get("name", "")
        congestion_level = place.get("congestionLevel", "")
        congestion_text = place.get("congestionText", "")
        print(f"{name} - 혼잡도: {congestion_text}({congestion_level})")
        
        # 주변 장소 정보
        nearby_places = poi_congestion.get("nearbyPlaces", [])
        if nearby_places:
            print(f"주변 {len(nearby_places)}개 장소 혼잡도:")
            for nearby in nearby_places:
                nearby_name = nearby.get("name", "")
                nearby_level = nearby.get("congestionLevel", "")
                nearby_text = nearby.get("congestionText", "")
                distance = nearby.get("distance", 0)
                print(f"  {nearby_name} - 혼잡도: {nearby_text}({nearby_level}), 거리: {distance}m")
```

## 제공 기능

- POI(장소) 검색
- 지오코딩 (주소 → 좌표)
- Full Text 지오코딩 (자유 형식 텍스트 → 좌표)
- 역지오코딩 (좌표 → 주소)
- 보행자 경로 안내
- 자동차 경로 안내
- 타임머신 자동차 경로 안내 (미래/과거 시간 기준, KST 지원)
- 정적 지도 이미지 생성
- Puzzle 장소 혼잡도 조회 (실시간 혼잡도, 키워드 검색, 좌표 기반 검색)

## 참고 문서

- [TMAP API 공식 문서](https://tmapapi.tmapmobility.com/main.html) 