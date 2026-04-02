import os
from langchain_core.tools import tool

LOADING_MAX_CHAR_COUNT:int = 50000

@tool
def list_files(directory_path:str = ".") -> str:
    """
    列出指定目錄下的所有檔案與資料夾名稱。
    當你需要了解專案結構或尋找特定程式碼檔案（如 .cs, .cpp, .py）時使用此工具。
    """
    try:
        # Ignore the files that contain the sensitive data.
        exclude_dirs = {'.venv', '.git', '__pycache__', 'bin', 'obj'}
        files = [f for f in os.listdir(directory_path) if f not in exclude_dirs]
        return "\n".join(files) if files else "The directory is empty or not exist."
    except Exception as e:
        return f"List directory fail: {str(e)}"

@tool
def read_file_content(file_path:str) -> str:
    """
    讀取並返回指定檔案的文字內容。
    當你需要分析程式碼邏輯、檢查 Bug 或進行 Code Review 時使用此工具。
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if len(content) >= LOADING_MAX_CHAR_COUNT:
                return content[:LOADING_MAX_CHAR_COUNT] + "\n...(interrupt)"
            return content
    except Exception as e:
        return f"Read file fail: {str(e)}"