import os
from pymcp import PyMCP, mcpwrap
from tmap_api.tmap_api import TmapAPI

# Tmap API 클라이언트 초기화
TMAP_APP_KEY = os.environ.get("TMAP_APP_KEY")
if not TMAP_APP_KEY:
    raise ValueError("TMAP_APP_KEY 환경 변수가 설정되지 않았습니다.")

tmap_client = TmapAPI(app_key=TMAP_APP_KEY)

# MCP 서버 생성
tmap_server = PyMCP(
    name="Tmap API Server",
    instructions="A server providing Tmap API functions for location search, geocoding, route planning, and more"
)

# API 함수 정의 및 MCP 서버에 등록
@tmap_server.wrap_function(name="search_poi_keyword")
def search_poi_keyword(keyword: str, search_type: str = "all", count: int = 20):
    """
    Search for Points of Interest (POI) using keywords
    
    Args:
        keyword: Search keyword
        search_type: Search type (all, name, telno)
        count: Maximum number of search results
    
    Returns:
        POI search result data
    """
    return tmap_client.search_poi_keyword(keyword, search_type, count)

@tmap_server.wrap_function(name="search_address_keyword")
def search_address_keyword(keyword: str, search_type: str = "all"):
    """
    Search for address information using keywords
    
    Args:
        keyword: Search keyword
        search_type: Search type (all, name, telno)
    
    Returns:
        Address information in (province, city, district) format
    """
    sido, sigungu, dong = tmap_client.search_address_keyword(keyword, search_type)
    return {"sido": sido, "sigungu": sigungu, "dong": dong}

@tmap_server.wrap_function(name="search_coord_keyword")
def search_coord_keyword(keyword: str, search_type: str = "all"):
    """
    Search for coordinates using keywords
    
    Args:
        keyword: Search keyword
        search_type: Search type (all, name, telno)
    
    Returns:
        Coordinate information in (latitude, longitude) format
    """
    lat, lon = tmap_client.search_coord_keyword(keyword, search_type)
    return {"lat": lat, "lon": lon}

@tmap_server.wrap_function(name="geocoding")
def geocoding(city_do: str, gu_gun: str, dong: str, coord_type: str = "WGS84GEO"):
    """
    Convert address to coordinates (geocoding)
    
    Args:
        city_do: Province/City name
        gu_gun: County/District name
        dong: Neighborhood name
        coord_type: Coordinate system type
    
    Returns:
        Coordinate information
    """
    return tmap_client.geocoding(city_do, gu_gun, dong, coord_type)

@tmap_server.wrap_function(name="full_text_geocoding")
def full_text_geocoding(address: str, coord_type: str = "WGS84GEO", search_count: int = 10):
    """
    Convert free-form text address to coordinates
    
    Args:
        address: Address in free-form text
        coord_type: Coordinate system type
        search_count: Number of search results
    
    Returns:
        Coordinate information
    """
    return tmap_client.full_text_geocoding(address, coord_type, search_count)

@tmap_server.wrap_function(name="reverse_geocoding")
def reverse_geocoding(lat: float, lon: float, address_type: str = "A10"):
    """
    Convert coordinates to address (reverse geocoding)
    
    Args:
        lat: Latitude
        lon: Longitude
        address_type: Address type (A10: administrative+legal, A02: administrative, A03: legal)
    
    Returns:
        Address information
    """
    return tmap_client.reverse_geocoding(lat, lon, address_type)

@tmap_server.wrap_function(name="pedestrian_route_detail")
def pedestrian_route_detail(start_x: float, start_y: float, end_x: float, end_y: float, 
                            startName: str, endName: str, search_option: str = "0"):
    """
    Get detailed pedestrian route information
    
    Args:
        start_x: Starting point longitude
        start_y: Starting point latitude
        end_x: Destination longitude
        end_y: Destination latitude
        startName: Starting point name
        endName: Destination name
        search_option: Route search option (0: recommended, 4: recommended shortest, 10: shortest)
    
    Returns:
        Detailed route information
    """
    return tmap_client.pedestrian_route_detail(
        start_x, start_y, end_x, end_y, 
        startName, endName, search_option
    )

@tmap_server.wrap_function(name="pedestrian_route_summary")
def pedestrian_route_summary(start_x: float, start_y: float, end_x: float, end_y: float, 
                            startName: str, endName: str, search_option: str = "0"):
    """
    Get summary of pedestrian route information
    
    Args:
        start_x: Starting point longitude
        start_y: Starting point latitude
        end_x: Destination longitude
        end_y: Destination latitude
        startName: Starting point name
        endName: Destination name
        search_option: Route search option (0: recommended, 4: recommended shortest, 10: shortest)
    
    Returns:
        Summary route information (total distance, total time)
    """
    return tmap_client.pedestrian_route_summary(
        start_x, start_y, end_x, end_y, 
        startName, endName, search_option
    )

@tmap_server.wrap_function(name="car_route")
def car_route(start_x: float, start_y: float, end_x: float, end_y: float, search_option: str = "0"):
    """
    Get car route guidance
    
    Args:
        start_x: Starting point longitude
        start_y: Starting point latitude
        end_x: Destination longitude
        end_y: Destination latitude
        search_option: Route search option (0: recommended, 1: traffic optimal, 2: shortest distance)
    
    Returns:
        Route information
    """
    return tmap_client.car_route(start_x, start_y, end_x, end_y, search_option)

@tmap_server.wrap_function(name="time_machine_route")
def time_machine_route(start_x: float, start_y: float, end_x: float, end_y: float, 
                       departure_time: str, search_option: str = "0", 
                       arrival_option: str = "0", via_points=None, use_kst: bool = True):
    """
    Get time machine car route guidance (route based on future/past time)
    
    Args:
        start_x: Starting point longitude
        start_y: Starting point latitude
        end_x: Destination longitude
        end_y: Destination latitude
        departure_time: Departure time ('YYYY-MM-DD hh:mm:ss' format)
        search_option: Route search option (0: recommended, 1: traffic optimal, 2: shortest distance)
        arrival_option: Arrival option (0: departure time, 1: arrival time)
        via_points: List of waypoints
        use_kst: Use Korean Standard Time (KST, UTC+9)
    
    Returns:
        Route information
    """
    return tmap_client.time_machine_route(
        start_x, start_y, end_x, end_y, 
        departure_time, search_option, arrival_option, via_points, use_kst
    )

@tmap_server.wrap_function(name="get_poi_detail")
def get_poi_detail(poi_id: str):
    """
    Get detailed POI information
    
    Args:
        poi_id: POI ID or identifier
    
    Returns:
        Detailed POI information
    """
    return tmap_client.get_poi_detail(poi_id)

@tmap_server.wrap_function(name="realtime_place_congestion")
def realtime_place_congestion(poi_id: str, lat=None, lng=None):
    """
    Get real-time place congestion information
    
    Args:
        poi_id: POI ID or identifier
        lat: Center latitude for surrounding congestion (optional)
        lng: Center longitude for surrounding congestion (optional)
    
    Returns:
        Congestion information
    """
    if lat is not None:
        lat = float(lat)
    if lng is not None:
        lng = float(lng)
    return tmap_client.realtime_place_congestion(poi_id, lat, lng)

# 서버 실행 코드
if __name__ == "__main__":
    # 서버 시작
    tmap_server.run() 