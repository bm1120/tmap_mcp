# tmap_mcp
Tmap REST API 기반 MCP(Model Context Protocol) 서버 구축

## 개요
이 프로젝트는 T맵 REST API를 MCP(Model Context Protocol) 서버로 제공하여 Cursor 편집기와 같은 AI 도구에서 직접 T맵 API 기능을 호출할 수 있도록 합니다. pymcp 라이브러리를 사용하여 구현되었습니다.

## 주요 기능
- 위치 검색 (POI 검색, 주소 검색)
- 지오코딩 및 역지오코딩
- 보행자 경로 안내
- 자동차 경로 안내
- 실시간 혼잡도 조회
- 타임머신 경로 안내
- 대중교통 경로 안내
- 대중교통 경로 요약 정보
- 기타 T맵 API 기능들

## 설치 및 설정

### 필수 요구사항
- Python 3.6 이상
- T맵 API 앱 키
- Cursor 편집기 (AI 기능 사용 시)

### 패키지 설치
```bash
pip install pymcp requests
```

### T맵 API 키 설정
Windows에서는 다음 명령어로 환경 변수를 설정할 수 있습니다:
```bash
set TMAP_APP_KEY=your_tmap_api_key
```

영구적으로 설정하려면 시스템 환경 변수에 추가하세요.

## 사용 방법

### 1. MCP 서버 실행
```bash
run_mcp_server.bat
```
실행 시 T맵 API 키가 환경 변수로 설정되어 있지 않으면 입력 프롬프트가 표시됩니다.

### 2. Cursor 편집기와 연결 (선택 사항)
Cursor 편집기에서 MCP 서버를 통해 T맵 API를 사용하려면 다음 단계를 따르세요:

1. 설정 스크립트 실행:
```bash
run_setup_cursor.bat
```

2. Cursor 편집기를 재시작합니다.

3. Cursor 편집기의 AI 패널에서 'tmap-api' 서버를 선택합니다.

## 기능 설명

### 위치 검색
- `search_poi_keyword`: 키워드로 POI(관심 지점) 검색
- `search_address_keyword`: 키워드로 주소 검색
- `search_coord_keyword`: 키워드로 좌표 검색

### 지오코딩
- `geocoding`: 주소를 좌표로 변환
- `full_text_geocoding`: 자유 형식 텍스트 주소를 좌표로 변환
- `reverse_geocoding`: 좌표를 주소로 변환

### 경로 안내
- `pedestrian_route_detail`: 보행자 경로 상세 정보 조회
- `pedestrian_route_summary`: 보행자 경로 요약 정보 조회
- `car_route`: 자동차 경로 안내
- `time_machine_route`: 타임머신 자동차 경로 안내
- `public_transit_route`: 대중교통 경로 안내
- `get_subway_congestion`: 지하철 열차 혼잡도 조회

### 장소 정보
- `get_poi_detail`: POI 상세 정보 검색
- `realtime_place_congestion`: 실시간 장소 혼잡도 조회

### 지하철 정보
- `get_subway_congestion`: 지하철 열차 혼잡도 조회
- `get_subway_station_congestion`: 지하철 칸별 혼잡도 조회
- `get_subway_exit_ratio`: 지하철 칸별 하차 비율 조회

## 파일 구조
- `mcp_server.py` - MCP 서버 구현
- `run_mcp_server.bat` - Windows에서 서버를 실행하는 배치 파일
- `setup_cursor.py` - Cursor 편집기 설정 스크립트
- `run_setup_cursor.bat` - 설정 스크립트 실행 배치 파일
- `tmap_api/` - T맵 API 패키지
  - `tmap_api.py` - T맵 API 클래스

## 참고 자료
- [T맵 API 문서](https://tmapapi.sktelecom.com/main.html#)
- [pymcp GitHub](https://github.com/tsdata/pymcp)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
