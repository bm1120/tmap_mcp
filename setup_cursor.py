"""
Cursor 편집기에 Tmap MCP 서버를 자동으로 등록하는 스크립트입니다.
"""

import os
import sys
import subprocess
from pathlib import Path
import platform

def get_python_path():
    """현재 실행 중인 Python 인터프리터 경로를 반환합니다."""
    return sys.executable

def get_script_path():
    """스크립트 파일의 절대 경로를 반환합니다."""
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir

def register_mcp_server():
    """pymcp 도구를 사용하여 Cursor 편집기에 MCP 서버를 등록합니다."""
    print("Registering Tmap MCP server with Cursor editor...")
    
    # 현재 스크립트 디렉토리
    script_dir = get_script_path()
    
    # mcp_server.py 파일의 절대 경로 구성
    server_path = os.path.join(script_dir, "mcp_server.py")
    server_path = os.path.normpath(server_path)
    
    # Python 인터프리터 경로
    python_path = get_python_path()
    
    # pymcp 명령어 구성
    cmd = [
        python_path, 
        "-m", 
        "pymcp", 
        "cursor", 
        "add-server", 
        "tmap-api", 
        server_path, 
        "--python", 
        python_path
    ]
    
    # 명령어 실행
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Successfully registered Tmap MCP server with Cursor editor!")
            print(result.stdout)
        else:
            print("Failed to register Tmap MCP server:")
            print(result.stderr)
    except Exception as e:
        print(f"Error registering MCP server: {e}")

def list_registered_servers():
    """현재 Cursor에 등록된 MCP 서버 목록을 출력합니다."""
    print("\nListing registered MCP servers in Cursor:")
    
    python_path = get_python_path()
    
    cmd = [
        python_path,
        "-m",
        "pymcp",
        "cursor",
        "list-servers"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Failed to list MCP servers:")
            print(result.stderr)
    except Exception as e:
        print(f"Error listing MCP servers: {e}")

def show_configuration_path():
    """Cursor MCP 서버 구성 파일 경로를 출력합니다."""
    print("\nCursor MCP configuration path:")
    
    python_path = get_python_path()
    
    cmd = [
        python_path,
        "-m",
        "pymcp",
        "cursor",
        "config-path"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Failed to get configuration path:")
            print(result.stderr)
    except Exception as e:
        print(f"Error getting configuration path: {e}")

def check_prerequisites():
    """필요한 패키지가 설치되어 있는지 확인합니다."""
    try:
        import pymcp
        print("pymcp package is installed.")
    except ImportError:
        print("pymcp package is not installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pymcp"], check=True)
            print("pymcp package installed successfully.")
        except Exception as e:
            print(f"Failed to install pymcp: {e}")
            return False
    return True

def main():
    """메인 함수"""
    print("Tmap MCP Server Setup for Cursor Editor")
    print("="*50)
    
    # 시스템 정보 출력
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Path: {get_python_path()}")
    print(f"Script Directory: {get_script_path()}")
    print("="*50)
    
    # 필수 요구사항 확인
    if not check_prerequisites():
        print("Failed to meet prerequisites. Exiting.")
        return
    
    # MCP 서버 등록
    register_mcp_server()
    
    # 등록된 서버 목록 출력
    list_registered_servers()
    
    # 구성 파일 경로 출력
    show_configuration_path()
    
    print("\nSetup completed!")
    print("Please restart Cursor editor and select 'tmap-api' server in the AI panel.")
    print("Make sure to set the TMAP_APP_KEY environment variable before running the server.")

if __name__ == "__main__":
    main() 