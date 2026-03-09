from fastapi import FastAPI, Request, Form, HTTPException, Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app import tools
import json
from typing import List, Dict, Any, Optional

app = FastAPI(title="蛙蛙工具 - 仿制版", description="便捷的在线工具网站")

# Setup templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def execute_tool(tool_id: str, content: str, params: Dict[str, Any] = None) -> str:
    params = params or {}
    if tool_id == "json_format":
        return tools.format_json(content)
    elif tool_id == "base64_encode":
        return tools.base64_encode(content)
    elif tool_id == "base64_decode":
        return tools.base64_decode(content)
    elif tool_id == "md5":
        return tools.md5_hash(content)
    elif tool_id == "case_convert":
        return tools.case_convert(content, params.get("mode", "upper"))
    elif tool_id == "text_replace":
        return tools.text_replace(content, params.get("old", ""), params.get("new", ""))
    elif tool_id == "regex_replace":
        return tools.regex_replace(content, params.get("pattern", ""), params.get("replacement", ""))
    elif tool_id == "add_prefix":
        return tools.add_prefix(content, params.get("prefix", ""))
    elif tool_id == "add_suffix":
        return tools.add_suffix(content, params.get("suffix", ""))
    elif tool_id == "insert_content":
        try:
            pos = int(params.get("position", 0))
        except:
            pos = 0
        return tools.insert_content(content, params.get("insert_text", ""), pos)
    elif tool_id == "newline_convert":
        return tools.newline_convert(content, params.get("mode", "unix"))
    elif tool_id == "delete_empty_lines":
        return tools.delete_empty_lines(content)
    elif tool_id == "delete_chars":
        return tools.delete_chars(content, params.get("chars", ""))
    elif tool_id == "add_line_numbers":
        return tools.add_line_numbers(content)
    elif tool_id == "remove_line_numbers":
        return tools.remove_line_numbers(content)
    elif tool_id == "deduplicate_lines":
        return tools.deduplicate_lines(content)
    elif tool_id == "trim_lines":
        return tools.trim_lines(content)
    elif tool_id == "repeat_text":
        try:
            times = int(params.get("times", 1))
        except:
            times = 1
        return tools.repeat_text(content, times)
    elif tool_id == "flip_content":
        return tools.flip_content(content)
    elif tool_id == "word_count":
        return json.dumps(tools.word_count(content))
    elif tool_id == "url_encode":
        return tools.url_encode(content)
    elif tool_id == "url_decode":
        return tools.url_decode(content)
    return content

@app.post("/api/tool/{tool_name}")
async def use_tool(tool_name: str, content: str = Form(...), mode: str = Form(None), old: str = Form(None), new: str = Form(None), pattern: str = Form(None), replacement: str = Form(None), prefix: str = Form(None), suffix: str = Form(None), insert_text: str = Form(None), position: str = Form(None), chars: str = Form(None), times: str = Form(None)):
    params = {
        "mode": mode, "old": old, "new": new, "pattern": pattern, 
        "replacement": replacement, "prefix": prefix, "suffix": suffix,
        "insert_text": insert_text, "position": position, "chars": chars,
        "times": times
    }
    # Filter out None values
    params = {k: v for k, v in params.items() if v is not None}
    
    result = execute_tool(tool_name, content, params)
    
    # Special handling for word_count which returns a JSON string from execute_tool
    if tool_name == "word_count":
        return {"result": json.loads(result)}
        
    return {"result": result}

@app.post("/api/workflow")
async def execute_workflow(data: Dict[str, Any] = Body(...)):
    content = data.get("content", "")
    steps = data.get("steps", [])
    
    current_content = content
    for step in steps:
        tool_id = step.get("id")
        params = step.get("params", {})
        current_content = execute_tool(tool_id, current_content, params)
        
    return {"result": current_content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
