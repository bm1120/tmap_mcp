import requests
import json
from typing import Dict, Any, Optional, Union, Tuple
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

class TmapAPI:
    """
    TMAP API 접근을 위한 클래스
    다양한 TMAP 서비스를 사용할 수 있는 메서드를 제공합니다.
    """
    
    def __init__(self, app_key: str):
        """
        TMAP API 클라이언트 초기화
        
        Args:
            app_key: TMAP API 인증 키
        """
        self.app_key = app_key
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "appKey": self.app_key
        }
        self.base_url = "https://apis.openapi.sk.com"
        self.tmap_url = f"{self.base_url}/tmap"
        self.transit_url = f"{self.base_url}/transit"
    
    def search_poi_keyword(self, keyword: str, search_type: str = "all", count: int = 20) -> Optional[Dict[str, Any]]:
        """
        키워드로 POI(관심 지점) 검색
        
        Args:
            keyword: 검색할 키워드
            search_type: 검색 유형 (all, name, telno)
            count: 검색 결과 최대 개수
            
        Returns:
            검색 결과 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/pois"
        
        params = {
            "version": "1",
            "searchKeyword": keyword,  # URL 인코딩 제거
            "searchType": search_type,
            "count": str(count),
            "appKey": self.app_key
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                result = response.json()
                return result
            elif response.status_code == 204:
                print(f"'{keyword}'에 대한 검색 결과가 없습니다.")
                return None
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
        
    def search_address_keyword(self, keyword: str, search_type: str = "all") -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        키워드로 주소 검색
        
        Args:
            keyword: 검색할 키워드
            search_type: 검색 유형 (all, name, telno)
            
        Returns:
            (시도, 시군구, 읍면동) 튜플 또는 실패시 (None, None, None)
        """
        poi_result = self.search_poi_keyword(keyword, search_type, 1)
        if poi_result:
            poi_list = poi_result['searchPoiInfo']['pois']['poi']
            if poi_list:
                poi = poi_list[0]
                return poi['upperAddrName'], poi['middleAddrName'], poi['lowerAddrName']
        return None, None, None
    
    def search_coord_keyword(self, keyword: str, search_type: str = "all") -> Tuple[Optional[float], Optional[float]]:
        """
        키워드로 좌표 검색
        
        Args:
            keyword: 검색할 키워드
            search_type: 검색 유형 (all, name, telno)
            
        Returns:
            (위도, 경도) 튜플 또는 실패시 (None, None)
        """
        poi_result = self.search_poi_keyword(keyword, search_type, 1)
        if poi_result:
            poi_list = poi_result['searchPoiInfo']['pois']['poi']
            if poi_list:
                poi = poi_list[0]
                return poi['frontLat'], poi['frontLon']
        return None, None
        
    def geocoding(self, city_do: str, gu_gun: str, dong: str,  coord_type: str = "WGS84GEO") -> Optional[Dict[str, Any]]:
        """
        주소를 좌표로 변환 (지오코딩)
        
        Args:
            address: 변환할 주소
            coord_type: 응답 좌표계 유형 (WGS84GEO, EPSG3857 등)
            
        Returns:
            좌표 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/geo/geocoding"
        
        params = {
            "version": "1",
            "appKey": self.app_key,
            "city_do": quote(city_do, encoding='utf-8'),
            "gu_gun": quote(gu_gun, encoding='utf-8'),
            "dong": quote(dong, encoding='utf-8'),
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def full_text_geocoding(self, address: str, coord_type: str = "WGS84GEO", 
                           search_count: int = 10) -> Optional[Dict[str, Any]]:
        """
        자유 형식 텍스트 주소를 좌표로 변환 (Full Text 지오코딩)
        
        Args:
            address: 변환할 주소 (자유 형식 텍스트)
            coord_type: 응답 좌표계 유형 (WGS84GEO, EPSG3857 등)
            search_count: 검색 결과 수
            
        Returns:
            좌표 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/geo/fullAddrGeo"
        
        params = {
            "version": "1",
            "appKey": self.app_key,
            "coordType": coord_type,
            "fullAddr": quote(address, encoding='utf-8'),
            "searchCount": str(search_count)
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def reverse_geocoding(self, lat: float, lon: float, address_type: str = "A10") -> Optional[Dict[str, Any]]:
        """
        좌표를 주소로 변환 (역지오코딩)
        
        Args:
            lat: 위도
            lon: 경도
            address_type: 주소 유형 (A10: 행정동+법정동, A02: 행정동, A03: 법정동)
            
        Returns:
            주소 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/geo/reversegeocoding"
        
        params = {
            "version": "1",
            "lat": str(lat),
            "lon": str(lon),
            "coordType": "WGS84GEO",
            "addressType": address_type,
            "appKey": self.app_key
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def pedestrian_route_detail(self, start_x: float, start_y: float, end_x: float, end_y: float, startName: str, endName: str,
                        search_option: str = "0") -> Optional[Dict[str, Any]]:
        """
        보행자 경로 상세 정보 조회
        
        Args:
            start_x: 출발지 경도
            start_y: 출발지 위도
            end_x: 도착지 경도
            end_y: 도착지 위도
            startName: 출발지 이름
            endName: 도착지 이름
            search_option: 경로 검색 옵션 (0: 추천경로, 4: 추천 최단, 10: 최단경로)
            
        Returns:
            경로 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/routes/pedestrian"
        
        payload = {
            "startX": str(start_x),
            "startY": str(start_y),
            "endX": str(end_x),   
            "endY": str(end_y),
            "startName": startName,  # URL 인코딩은 requests 라이브러리가 자동으로 처리
            "endName": endName,      # URL 인코딩은 requests 라이브러리가 자동으로 처리
            "searchOption": search_option
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
        
    def pedestrian_route_summary(self, start_x: float, start_y: float, end_x: float, end_y: float, startName: str, endName: str,
                        search_option: str = "0") -> Optional[Dict[str, Any]]:
        """
        보행자 경로 요약 정보 조회
        
        Args:
            start_x: 출발지 경도
            start_y: 출발지 위도
            end_x: 도착지 경도
            end_y: 도착지 위도
            startName: 출발지 이름
            endName: 도착지 이름
            search_option: 경로 검색 옵션 (0: 추천경로, 4: 추천 최단, 10: 최단경로)
            
        Returns:
            경로 정보 데이터 또는 실패시 None
        """
        routes = self.pedestrian_route_detail(start_x, start_y, end_x, end_y, startName, endName, search_option)
        if routes:
            features = routes['features'][0]
            properties = features['properties']
            total_distance = properties['totalDistance']
            total_time = properties['totalTime']
            return {'total_distance': total_distance, 'total_time': total_time}
        return None
    
    def static_map(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                  file_path: str = "route_map.png") -> bool:
        """
        경로 정적 지도 이미지 생성
        
        Args:
            start_x: 출발지 경도
            start_y: 출발지 위도
            end_x: 도착지 경도
            end_y: 도착지 위도
            file_path: 저장할 이미지 파일 경로
            
        Returns:
            성공 여부
        """
        url = f"{self.tmap_url}/routeStaticMap"
        
        params = {
            "version": "1",
            "startX": str(start_x),
            "startY": str(start_y),
            "endX": str(end_x),
            "endY": str(end_y),
            "appKey": self.app_key
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"경로 지도 이미지가 {file_path}에 저장되었습니다.")
                return True
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return False
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return False
    
    def car_route(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                 search_option: str = "0") -> Optional[Dict[str, Any]]:
        """
        자동차 경로 안내
        
        Args:
            start_x: 출발지 경도
            start_y: 출발지 위도
            end_x: 도착지 경도
            end_y: 도착지 위도
            search_option: 경로 검색 옵션 (0: 추천경로, 1: 교통최적, 2: 최단거리 등)
            
        Returns:
            경로 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/routes"
        
        payload = {
            "startX": str(start_x),
            "startY": str(start_y),
            "endX": str(end_x),   
            "endY": str(end_y),
            "startName": "출발지",
            "endName": "도착지",
            "searchOption": search_option,
            "appKey": self.app_key
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def time_machine_route(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                          departure_time: Union[datetime, str], search_option: str = "0", 
                          arrival_option: str = "0", via_points: Optional[list] = None,
                          use_kst: bool = True) -> Optional[Dict[str, Any]]:
        """
        타임머신 자동차 길 안내 (미래/과거 시간 기준 경로 안내)
        
        Args:
            start_x: 출발지 경도
            start_y: 출발지 위도
            end_x: 도착지 경도
            end_y: 도착지 위도
            departure_time: 출발 시간 (datetime 객체 또는 'YYYY-MM-DD hh:mm:ss' 형식의 문자열)
            search_option: 경로 검색 옵션 (0: 추천경로, 1: 교통최적, 2: 최단거리 등)
            arrival_option: 도착 옵션 (0: 출발시간, 1: 도착시간)
            via_points: 경유지 목록 (선택적, 경도/위도 쌍의 리스트)
            use_kst: 한국 시간대(KST, UTC+9) 사용 여부 (기본값: True)
            
        Returns:
            경로 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/routes/prediction"
        
        # datetime 객체 처리
        if isinstance(departure_time, datetime):
            # 입력된 datetime이 naive(시간대 정보 없음)인 경우
            if departure_time.tzinfo is None:
                if use_kst:
                    # 입력된 시간을 KST로 간주하고 UTC로 변환
                    kst = timezone(timedelta(hours=9))
                    departure_time = departure_time.replace(tzinfo=kst)
                    # 서버에 보낼 때는 UTC 기준 시간 사용
                    departure_time_utc = departure_time.astimezone(timezone.utc)
                else:
                    # 시간대 정보가 없으면 로컬 시간으로 간주
                    departure_time_utc = departure_time
            else:
                # 이미 시간대 정보가 있으면 UTC로 변환
                departure_time_utc = departure_time.astimezone(timezone.utc)
            
            # 'YYYY-MM-DD hh:mm:ss' 형식으로 변환
            departure_time_str = departure_time_utc.strftime("%Y-%m-%d %H:%M:%S")
        else:
            # 이미 문자열인 경우는 그대로 사용
            departure_time_str = departure_time
        
        payload = {
            "startX": str(start_x),
            "startY": str(start_y),
            "endX": str(end_x),   
            "endY": str(end_y),
            "startName": "출발지",
            "endName": "도착지",
            "searchOption": search_option,
            "departureTime": departure_time_str,  # 출발/도착 시간 (YYYY-MM-DD hh:mm:ss)
            "arrivalOption": arrival_option,  # 0: 출발시간, 1: 도착시간
            "appKey": self.app_key
        }
        
        # 경유지가 있는 경우 추가
        if via_points:
            payload["passList"] = via_points
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def get_poi_detail(self, poi_id: str) -> Optional[Dict[str, Any]]:
        """
        POI 상세 정보 검색
        
        Args:
            poi_id: POI ID 또는 POI 식별자
            
        Returns:
            POI 상세 정보 데이터 또는 실패시 None
        """
        url = f"{self.tmap_url}/pois/{poi_id}"
        
        params = {
            "version": "1",
            "appKey": self.app_key
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"POI 상세 정보 조회 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None

    def realtime_place_congestion(self, poi_id: str, lat: Optional[float] = None, lng: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        실시간 장소 혼잡도 조회
        
        Args:
            poi_id: POI ID 또는 POI 식별자
            lat: 주변 혼잡도를 구할 중심 위도값 (WGS84 경위도 좌표계)
            lng: 주변 혼잡도를 구할 중심 경도값 (WGS84 경위도 좌표계)
            
        Returns:
            혼잡도 정보 데이터 또는 실패시 None
            응답 데이터 구조:
            {
                "status": {
                    "code": "00",
                    "message": "success",
                    "totalCount": 1
                },
                "contents": {
                    "poiId": "10067845",
                    "poiName": "더현대서울",
                    "rltm": {
                        "type": 1,  # 1: 장소 혼잡도, 2: 주변 혼잡도
                        "congestion": 0.03895,  # 단위 면적당 평균 혼잡도 (명/㎡)
                        "congestionLevel": 1,   # 혼잡도 레벨 (1: 여유, 2: 보통, 3: 혼잡, 4: 매우 혼잡)
                        "datetime": "20220822124000"  # YYYYMMDDHHmmss 형식
                    }
                }
            }
        """
        # 먼저 POI 상세 정보 조회
        poi_detail = self.get_poi_detail(poi_id)
        if not poi_detail:
            print(f"POI ID {poi_id}에 대한 상세 정보를 찾을 수 없습니다.")
            return None
            
        url = f"{self.tmap_url}/puzzle/pois/{poi_id}"
        
        params = {
            "version": "1",
            "appKey": self.app_key
        }
        
        # 선택적 파라미터 추가
        if lat is not None:
            params["lat"] = str(lat)
        if lng is not None:
            params["lng"] = str(lng)
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def public_transit_route(self, 
                           start_x: str,
                           start_y: str,
                           end_x: str,
                           end_y: str,
                           lang: int = 0,
                           format: str = "json",
                           count: int = 10,
                           search_dttm: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        대중교통 경로 탐색 API
        출발지/목적지에 대한 대중교통 경로탐색 정보와 전체 보행자 이동 경로를 제공

        Args:
            start_x: 출발지 X좌표(경도) - WGS84
            start_y: 출발지 Y좌표(위도) - WGS84
            end_x: 도착지 X좌표(경도) - WGS84
            end_y: 도착지 Y좌표(위도) - WGS84
            lang: 언어 선택 (0: 국문(기본값), 1: 영문)
            format: 출력포맷 (json, xml)
            count: 최대 응답 결과 개수 (1~10, 기본값 10)
            search_dttm: 타임머신 기능 검색 날짜(yyyymmddhhmi)

        Returns:
            대중교통 경로 정보 또는 실패시 None
            응답 예시:
            {
                "metaData": {
                    "requestParameters": {
                        "busCount": 3,
                        "expressbusCount": 0,
                        "subwayCount": 3,
                        "airplaneCount": 0,
                        "locale": "ko",
                        "endY": "37.564436",
                        "endX": "127.029281",
                        "startY": "37.555162",
                        "startX": "126.936928",
                        "reqDttm": "20240130163831"
                    },
                    "plan": {
                        "itineraries": [
                            {
                                "fare": {
                                    "regular": {
                                        "totalFare": 1400,
                                        "currency": {
                                            "symbol": "￦",
                                            "currency": "원",
                                            "currencyCode": "KRW"
                                        }
                                    }
                                },
                                "totalTime": 1229,
                                "legs": [
                                    {
                                        "mode": "WALK",
                                        "sectionTime": 114,
                                        "distance": 128,
                                        "start": {
                                            "name": "출발지",
                                            "lon": 126.936928,
                                            "lat": 37.555162
                                        },
                                        "end": {
                                            "name": "신촌",
                                            "lon": 126.93700277777778,
                                            "lat": 37.555169444444445
                                        },
                                        "steps": [
                                            {
                                                "streetName": "",
                                                "distance": 48,
                                                "description": "48m 이동",
                                                "linestring": "126.93693,37.555172..."
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        """
        url = f"{self.transit_url}/routes"
        
        payload = {
            "startX": start_x,
            "startY": start_y,
            "endX": end_x,
            "endY": end_y,
            "lang": lang,
            "format": format,
            "count": count
        }
        
        # 타임머신 검색 시간이 제공된 경우 추가
        if search_dttm:
            payload["searchDttm"] = search_dttm
            
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"대중교통 경로 검색 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def public_transit_route_summary(self, 
                                   start_x: str,
                                   start_y: str,
                                   end_x: str,
                                   end_y: str,
                                   format: str = "json",
                                   count: int = 10,
                                   search_dttm: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        대중교통 경로 요약정보 API
        출발지/목적지에 대한 대중교통 경로탐색 요약정보를 제공

        Args:
            start_x: 출발지 X좌표(경도) - WGS84
            start_y: 출발지 Y좌표(위도) - WGS84
            end_x: 도착지 X좌표(경도) - WGS84
            end_y: 도착지 Y좌표(위도) - WGS84
            format: 출력포맷 (json, xml)
            count: 최대 응답 결과 개수 (1~10, 기본값 10)
            search_dttm: 타임머신 기능 검색 날짜(yyyymmddhhmi)

        Returns:
            대중교통 경로 요약정보 또는 실패시 None
            응답 예시:
            {
                "metaData": {
                    "requestParameters": {
                        "endY": "37.564436",
                        "endX": "127.029281",
                        "startY": "37.555162",
                        "startX": "126.936928",
                        "reqDttm": "20240130144449"
                    },
                    "plan": {
                        "itineraries": [
                            {
                                "fare": {
                                    "regular": {
                                        "totalFare": 1400,
                                        "currency": {
                                            "symbol": "￦",
                                            "currency": "원",
                                            "currencyCode": "KRW"
                                        }
                                    }
                                },
                                "totalTime": 1280,        # 총 소요시간(초)
                                "totalWalkTime": 202,     # 총 도보 시간(초)
                                "pathType": 1,            # 경로 유형(1:지하철, 2:버스, 3:버스+지하철)
                                "transferCount": 0,       # 환승 횟수
                                "totalDistance": 8467,    # 총 이동거리(m)
                                "totalWalkDistance": 217  # 총 도보 거리(m)
                            }
                        ]
                    }
                }
            }
        """
        url = f"{self.transit_url}/routes/sub"
        
        payload = {
            "startX": start_x,
            "startY": start_y,
            "endX": end_x,
            "endY": end_y,
            "format": format,
            "count": count
        }
        
        # 타임머신 검색 시간이 제공된 경우 추가
        if search_dttm:
            payload["searchDttm"] = search_dttm
            
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"대중교통 경로 요약정보 검색 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def get_subway_congestion(self, 
                            route_nm: str,
                            station_nm: str,
                            dow: Optional[str] = None,
                            hh: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        지하철 진입 역 기준 열차 혼잡도 조회 API
        지정한 운행 시간대(05:30 ~ 23:50)에 특정 역으로 진입하는 일반/급행 열차에 대한 혼잡도 데이터를 10분 간격으로 제공

        Args:
            route_nm: 지하철 노선 명칭 (예: "1호선")
            station_nm: 지하철 역 명칭 (예: "서울역")
            dow: 검색 기준 요일 (MON, TUE, WED, THU, FRI, SAT, SUN)
                미입력시 현재 요일 기준 데이터 반환
            hh: 검색 기준 시간 (05~23)
                미입력시 현재 시간대 기준 데이터 반환

        Returns:
            열차 혼잡도 정보 또는 실패시 None
            응답 예시:
            {
                "status": {
                    "code": "00",
                    "message": "success",
                    "totalCount": 1
                },
                "contents": {
                    "subwayLine": "1호선",
                    "stationName": "서울역",
                    "stationCode": "133",
                    "stat": [
                        {
                            "startStationCode": "100",
                            "startStationName": "소요산역",
                            "endStationCode": "141",
                            "endStationName": "구로역",
                            "prevStationCode": "132",
                            "prevStationName": "시청역",
                            "updnLine": 1,  # 0: 상행선/외선, 1: 하행선/내선
                            "directAt": 0,  # 0: 일반열차, 1: 급행열차
                            "data": [
                                {
                                    "dow": "MON",
                                    "hh": "08",
                                    "mm": "00",
                                    "congestionTrain": 0  # 혼잡도 (단위: %)
                                }
                            ]
                        }
                    ],
                    "statStartDate": "20220515",  # 통계 시작 일자 (YYYYMMDD)
                    "statEndDate": "20220814"     # 통계 종료 일자 (YYYYMMDD)
                }
            }
        """
        url = f"{self.transit_url}/puzzle/subway/congestion/stat/train"
        
        params = {
            "routeNm": route_nm,
            "stationNm": station_nm
        }
        
        # 선택적 파라미터 추가
        if dow:
            params["dow"] = dow
        if hh:
            params["hh"] = hh
            
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"지하철 혼잡도 조회 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def get_subway_car_congestion(self, 
                                route_nm: str,
                                station_nm: str,
                                dow: Optional[str] = None,
                                hh: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        지하철 진입 역 기준 칸별 혼잡도 조회 API
        지정한 운행 시간대(05:30 ~ 23:50)에 특정 역으로 진입하는 일반/급행 열차에 대한 칸별 혼잡도 데이터를 10분 간격으로 제공

        Args:
            route_nm: 지하철 노선 명칭 (예: "1호선")
            station_nm: 지하철 역 명칭 (예: "서울역")
            dow: 검색 기준 요일 (MON, TUE, WED, THU, FRI, SAT, SUN)
                미입력시 현재 요일 기준 데이터 반환
            hh: 검색 기준 시간 (05~23)
                미입력시 현재 시간대 기준 데이터 반환

        Returns:
            칸별 혼잡도 정보 또는 실패시 None
            응답 예시:
            {
                "status": {
                    "code": "00",
                    "message": "success",
                    "totalCount": 1
                },
                "contents": {
                    "subwayLine": "1호선",
                    "stationName": "서울역",
                    "stationCode": "133",
                    "stat": [
                        {
                            "startStationCode": "100",
                            "startStationName": "소요산역",
                            "endStationCode": "141",
                            "endStationName": "구로역",
                            "prevStationCode": "132",
                            "prevStationName": "시청역",
                            "updnLine": 1,  # 0: 상행선/외선, 1: 하행선/내선
                            "directAt": 0,  # 0: 일반열차, 1: 급행열차
                            "data": [
                                {
                                    "dow": "TUE",
                                    "hh": "08",
                                    "mm": "00",
                                    "congestionCar": [  # 각 칸별 혼잡도 (단위: %)
                                        63, 67, 71, 81, 80, 88, 85, 80, 91, 85
                                    ]
                                }
                            ]
                        }
                    ],
                    "statStartDate": "20220516",  # 통계 시작 일자 (YYYYMMDD)
                    "statEndDate": "20220815"     # 통계 종료 일자 (YYYYMMDD)
                }
            }
        """
        url = f"{self.transit_url}/puzzle/subway/congestion/stat/car"
        
        params = {
            "routeNm": route_nm,
            "stationNm": station_nm
        }
        
        # 선택적 파라미터 추가
        if dow:
            params["dow"] = dow
        if hh:
            params["hh"] = hh
            
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"지하철 칸별 혼잡도 조회 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            return None
    
    def get_subway_car_getoff_rate(self, 
                                 route_nm: str,
                                 station_nm: str,
                                 dow: Optional[str] = None,
                                 hh: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        지하철 진입 역 기준 칸별 하차 비율 조회 API
        지정한 운행 시간대(05:30 ~ 23:50)에 특정 역으로 진입하는 일반/급행 열차에 대한 칸별 하차 비율 데이터를 10분 간격으로 제공

        Args:
            route_nm: 지하철 노선 명칭 (예: "1호선")
            station_nm: 지하철 역 명칭 (예: "서울역")
            dow: 검색 기준 요일 (MON, TUE, WED, THU, FRI, SAT, SUN)
                미입력시 현재 요일 기준 데이터 반환
            hh: 검색 기준 시간 (05~23)
                미입력시 현재 시간대 기준 데이터 반환

        Returns:
            칸별 하차 비율 정보 또는 실패시 None
            응답 예시:
            {
                "status": {
                    "code": "00",
                    "message": "success",
                    "totalCount": 1
                },
                "contents": {
                    "subwayLine": "1호선",
                    "stationName": "서울역",
                    "stationCode": "133",
                    "stat": [
                        {
                            "startStationCode": "100",
                            "startStationName": "소요산역",
                            "endStationCode": "141",
                            "endStationName": "구로역",
                            "prevStationCode": "132",
                            "prevStationName": "시청역",
                            "updnLine": 1,  # 0: 상행선/외선, 1: 하행선/내선
                            "directAt": 0,  # 0: 일반열차, 1: 급행열차
                            "data": [
                                {
                                    "dow": "MON",
                                    "hh": "08",
                                    "mm": "00",
                                    "getOffCarRate": [  # 각 칸별 하차 비율 (단위: %, 총합 100%)
                                        13, 17, 9, 14, 6, 7, 6, 8, 7, 13
                                    ]
                                }
                            ]
                        }
                    ],
                    "statStartDate": "20220516",  # 통계 시작 일자 (YYYYMMDD)
                    "statEndDate": "20220815"     # 통계 종료 일자 (YYYYMMDD)
                }
            }
        """
        url = f"{self.transit_url}/puzzle/subway/congestion/stat/get-off"
        
        params = {
            "routeNm": route_nm,
            "stationNm": station_nm
        }
        
        # 선택적 파라미터 추가
        if dow:
            params["dow"] = dow
        if hh:
            params["hh"] = hh
            
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"지하철 칸별 하차 비율 조회 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
        except Exception as e:
            print(f"에러 발생: {str(e)}")
    