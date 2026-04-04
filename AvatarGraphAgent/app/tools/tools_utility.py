import functools

def tool_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError:
            return f"❌ Permission error: The system refused the to execte the command. {func.__name__}"
        except FileNotFoundError:
            return f"❌ Error: The specified path or file could not be found."
        except UnicodeDecodeError:
            return f"❌ Error: Unsupported file encoding. Please try to using a plain txt file."
        except Exception as e:
            return f"❌ An excepted error occurred while executing {func.__name__} : {str(e)}"
    return wrapper 