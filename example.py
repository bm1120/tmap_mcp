from tmap_api import TmapAPI
from datetime import datetime, timedelta

def main():
    # 인증 키 설정 (실제 사용 시 자신의 API 키로 교체 필요)
    app_key = "여기에_API_키_입력"
    
    # TMAP API 클라이언트 초기화
    tmap = TmapAPI(app_key=app_key)
    
    print("=== TMAP API 사용 예제 ===")
    
    # 1. POI 검색 예시
    print("\n1. POI 검색 - '경복궁' 검색 결과:")
    search_result = tmap.search_poi_keyword("경복궁")
    if search_result:
        pois = search_result.get("searchPoiInfo", {}).get("pois", {}).get("poi", [])
        if pois:
            print(f"  총 {len(pois)}개의 결과를 찾았습니다.")
            for i, poi in enumerate(pois[:3]):  # 처음 3개만 출력
                name = poi.get("name", "")
                address = f"{poi.get('upperAddrName', '')} {poi.get('middleAddrName', '')} {poi.get('lowerAddrName', '')}"
                print(f"  {i+1}. {name}: {address}")
    
    # 2. 지오코딩 예시 (주소 → 좌표)
    print("\n2. 지오코딩 - 주소를 좌표로 변환:")
    address = "서울특별시 중구 세종대로 110"
    geocoding_result = tmap.geocoding(address)
    if geocoding_result:
        coords = geocoding_result.get("coordinateInfo", {}).get("coordinate", [])
        if coords and len(coords) > 0:
            lat = coords[0].get("lat")
            lon = coords[0].get("lon")
            print(f"  주소: {address}")
            print(f"  좌표: 위도 {lat}, 경도 {lon}")
    
    # 3. Full Text 지오코딩 예시
    print("\n3. Full Text 지오코딩 - 자유 형식 주소를 좌표로 변환:")
    free_text_address = "서울시청"
    full_geocoding_result = tmap.full_text_geocoding(free_text_address)
    if full_geocoding_result:
        addresses = full_geocoding_result.get("coordinateInfo", {}).get("coordinate", [])
        if addresses and len(addresses) > 0:
            lat = addresses[0].get("lat")
            lon = addresses[0].get("lon")
            new_address = addresses[0].get("newAddressList", {}).get("newAddress", [])
            if new_address and len(new_address) > 0:
                full_addr = new_address[0].get("fullAddressRoad", "")
                print(f"  검색어: {free_text_address}")
                print(f"  도로명 주소: {full_addr}")
                print(f"  좌표: 위도 {lat}, 경도 {lon}")
    
    # 4. 역지오코딩 예시
    print("\n4. 역지오코딩 - 서울시청 좌표로 주소 찾기:")
    lat, lon = 37.566826, 126.9786567  # 서울시청 좌표
    address_info = tmap.reverse_geocoding(lat, lon)
    if address_info:
        full_address = address_info.get("addressInfo", {}).get("fullAddress", "")
        print(f"  주소: {full_address}")
    
    # 5. 보행자 경로 안내 예시
    print("\n5. 보행자 경로 - 서울시청에서 덕수궁까지:")
    start_x, start_y = 126.9786567, 37.566826  # 서울시청
    end_x, end_y = 126.9753, 37.5668  # 덕수궁
    route_info = tmap.pedestrian_route(start_x, start_y, end_x, end_y)
    if route_info:
        properties = route_info.get("features", [{}])[0].get("properties", {})
        total_distance = properties.get("totalDistance", 0)
        total_time = properties.get("totalTime", 0)
        print(f"  거리: {total_distance}m, 예상 소요시간: {total_time//60}분 {total_time%60}초")
    
    # 6. 자동차 경로 안내 예시
    print("\n6. 자동차 경로 - 서울시청에서 덕수궁까지:")
    car_route = tmap.car_route(start_x, start_y, end_x, end_y)
    if car_route:
        features = car_route.get("features", [])
        if features:
            properties = features[0].get("properties", {})
            total_distance = properties.get("totalDistance", 0)
            total_time = properties.get("totalTime", 0)
            total_fare = properties.get("totalFare", 0)
            print(f"  자동차 경로: 거리 {total_distance}m, 시간 {total_time//60}분, 요금 {total_fare}원")
    
    # 7. 정적 지도 생성 예시
    print("\n7. 정적 지도 생성 - 서울시청에서 덕수궁까지의 경로:")
    file_path = "seoul_city_hall_to_deoksugung.png"
    result = tmap.static_map(start_x, start_y, end_x, end_y, file_path)
    if result:
        print(f"  지도 이미지가 '{file_path}' 파일로 저장되었습니다.")
    
    # 8. 타임머신 자동차 경로 안내 예시 (KST 적용)
    print("\n8. 타임머신 자동차 경로 - 서울시청에서 강남역까지 (내일 오전 9시 출발, KST 적용):")
    
    # 서울시청 좌표
    start_x, start_y = 126.9786567, 37.566826
    
    # 강남역 좌표
    end_x, end_y = 127.0282, 37.4979
    
    # 내일 오전 9시 (KST 기준)
    tomorrow = datetime.now() + timedelta(days=1)
    departure_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0, 0)
    
    # 타임머신 경로 요청 (KST 적용)
    time_machine_route = tmap.time_machine_route(
        start_x=start_x, 
        start_y=start_y, 
        end_x=end_x, 
        end_y=end_y, 
        departure_time=departure_time,
        search_option="0",    # 추천 경로
        arrival_option="0",   # 출발 시간 기준
        use_kst=True          # KST 시간대 사용 (한국 시간 기준)
    )
    
    if time_machine_route:
        features = time_machine_route.get("features", [])
        if features:
            properties = features[0].get("properties", {})
            total_distance = properties.get("totalDistance", 0)
            total_time = properties.get("totalTime", 0)
            total_fare = properties.get("totalFare", 0)
            departure_time_str = departure_time.strftime("%Y-%m-%d %H:%M")
            print(f"  출발 시간(KST): {departure_time_str}")
            print(f"  자동차 경로: 거리 {total_distance}m, 예상 소요시간 {total_time//60}분, 요금 {total_fare}원")
    
    # 9. 키워드 기반 장소 혼잡도 검색 예시
    print("\n9. 키워드 기반 장소 혼잡도 - '명동' 주변 혼잡도 검색:")
    
    # 서울 명동 좌표
    myeongdong_lat, myeongdong_lon = 37.5637, 126.9838
    
    congestion_result = tmap.poi_congestion_by_keyword(
        keyword="명동",
        lat=myeongdong_lat,
        lon=myeongdong_lon,
        radius=1000,  # 1km 반경
        count=5       # 상위 5개 결과
    )
    
    if congestion_result:
        places = congestion_result.get("places", [])
        if places:
            print(f"  총 {len(places)}개의 장소 혼잡도 정보를 찾았습니다.")
            for i, place in enumerate(places):
                name = place.get("name", "")
                congestion_level = place.get("congestionLevel", "")
                congestion_text = place.get("congestionText", "")
                address = place.get("address", "")
                print(f"  {i+1}. {name} - 혼잡도: {congestion_text}({congestion_level})")
                print(f"     주소: {address}")
    
    # 10. 좌표 기반 주변 장소 혼잡도 검색 예시
    print("\n10. 좌표 기반 주변 장소 혼잡도 - 서울시청 주변 혼잡도:")
    
    nearby_congestion = tmap.poi_congestion_by_coordinates(
        lat=37.566826,  # 서울시청 위도
        lon=126.9786567,  # 서울시청 경도
        radius=500  # 500m 반경
    )
    
    if nearby_congestion:
        places = nearby_congestion.get("places", [])
        if places:
            print(f"  총 {len(places)}개의 주변 장소 혼잡도 정보를 찾았습니다.")
            for i, place in enumerate(places[:3]):  # 처음 3개만 출력
                name = place.get("name", "")
                congestion_level = place.get("congestionLevel", "")
                congestion_text = place.get("congestionText", "")
                distance = place.get("distance", 0)
                print(f"  {i+1}. {name} - 혼잡도: {congestion_text}({congestion_level}), 거리: {distance}m")
    
    # 11. 특정 장소 ID로 혼잡도 조회 예시
    print("\n11. 특정 장소 ID로 혼잡도 조회 (POI ID 필요):")
    # 주의: 실제 POI ID는 POI 검색 결과에서 얻거나 TMAP API 개발자 포털에서 확인해야 함
    poi_id = "1000"  # 예시 POI ID, 실제 사용 시 유효한 ID로 교체 필요
    
    place_congestion = tmap.realtime_place_congestion(
        poi_id=poi_id,
        radius=0  # 주변 장소 검색 안함
    )
    
    if place_congestion:
        place = place_congestion.get("place", {})
        if place:
            name = place.get("name", "")
            congestion_level = place.get("congestionLevel", "")
            congestion_text = place.get("congestionText", "")
            address = place.get("address", "")
            print(f"  장소명: {name}")
            print(f"  혼잡도: {congestion_text}({congestion_level})")
            print(f"  주소: {address}")
            
            # 주변 장소 정보
            nearby_places = place_congestion.get("nearbyPlaces", [])
            if nearby_places:
                print(f"  주변 {len(nearby_places)}개 장소의 혼잡도 정보:")
                for i, nearby in enumerate(nearby_places[:2]):  # 처음 2개만 출력
                    name = nearby.get("name", "")
                    congestion_level = nearby.get("congestionLevel", "")
                    congestion_text = nearby.get("congestionText", "")
                    distance = nearby.get("distance", 0)
                    print(f"    {i+1}. {name} - 혼잡도: {congestion_text}({congestion_level}), 거리: {distance}m")

if __name__ == "__main__":
    main() 