import json
import base64
import hashlib
import re
from urllib.parse import quote, unquote

def format_json(content: str) -> str:
    try:
        obj = json.loads(content)
        return json.dumps(obj, indent=4, ensure_ascii=False)
    except Exception as e:
        return f"Error: {str(e)}"

def base64_encode(content: str) -> str:
    try:
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"

def base64_decode(content: str) -> str:
    try:
        return base64.b64decode(content.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"

def md5_hash(content: str) -> str:
    try:
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"

def case_convert(content: str, mode: str) -> str:
    if mode == "upper":
        return content.upper()
    elif mode == "lower":
        return content.lower()
    elif mode == "title":
        return content.title()
    return content

def text_replace(content: str, old: str, new: str) -> str:
    return content.replace(old, new)

def regex_replace(content: str, pattern: str, replacement: str) -> str:
    try:
        return re.sub(pattern, replacement, content)
    except Exception as e:
        return f"Regex Error: {str(e)}"

def add_prefix(content: str, prefix: str) -> str:
    lines = content.splitlines()
    return "\n".join([prefix + line for line in lines])

def add_suffix(content: str, suffix: str) -> str:
    lines = content.splitlines()
    return "\n".join([line + suffix for line in lines])

def insert_content(content: str, insert_text: str, position: int) -> str:
    return content[:position] + insert_text + content[position:]

def newline_convert(content: str, mode: str) -> str:
    # mode: to_unix (\n), to_windows (\r\n), to_mac (\r)
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    if mode == "windows":
        return content.replace('\n', '\r\n')
    elif mode == "mac":
        return content.replace('\n', '\r')
    return content

def delete_empty_lines(content: str) -> str:
    lines = content.splitlines()
    return "\n".join([line for line in lines if line.strip()])

def delete_chars(content: str, chars: str) -> str:
    for char in chars:
        content = content.replace(char, '')
    return content

def add_line_numbers(content: str) -> str:
    lines = content.splitlines()
    return "\n".join([f"{i+1}. {line}" for i, line in enumerate(lines)])

def remove_line_numbers(content: str) -> str:
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        # Matches numbers followed by a dot or space at the start of a line
        new_line = re.sub(r'^\s*\d+[\.\s]*', '', line)
        new_lines.append(new_line)
    return "\n".join(new_lines)

def deduplicate_lines(content: str) -> str:
    lines = content.splitlines()
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            result.append(line)
            seen.add(line)
    return "\n".join(result)

def trim_lines(content: str) -> str:
    lines = content.splitlines()
    return "\n".join([line.strip() for line in lines])

def repeat_text(content: str, times: int) -> str:
    try:
        return content * int(times)
    except:
        return content

def flip_content(content: str) -> str:
    return content[::-1]

def word_count(content: str) -> dict:
    char_count = len(content)
    # Simple word count (splitting by space)
    words = content.split()
    word_count = len(words)
    return {
        "characters": char_count,
        "words": word_count,
        "lines": content.count('\n') + 1 if content else 0
    }

def url_encode(content: str) -> str:
    return quote(content)

def url_decode(content: str) -> str:
    return unquote(content)
