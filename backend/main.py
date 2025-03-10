from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re

class URLRequest(BaseModel):
    url: str

app = FastAPI()

# 添加 CORS 中间件，允许前端访问
frontend_url = os.environ.get("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items = []

@app.get("/")
def read_root():
    return {"message": "Hello World"}

def extract_video_id(url):
    """从YouTube URL中提取视频ID"""
    # 常规YouTube URL
    youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, url)
    return match.group(1) if match else None

@app.post("/process-url")
def process_url(request: URLRequest):
    url = request.url
    
    # 检查是否是YouTube链接
    video_id = extract_video_id(url)
    if not video_id:
        return {
            "url": url,
            "error": "不是有效的YouTube链接",
            "status": "failed"
        }
    
    try:
        # 获取视频字幕
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # 尝试获取中文字幕，如果没有则获取英文字幕，如果都没有则获取任何可用字幕
        try:
            transcript = transcript_list.find_transcript(['zh-CN', 'zh'])
        except:
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                transcript = transcript_list.find_generated_transcript(['zh-CN', 'zh', 'en'])
        
        # 获取字幕数据
        transcript_data = transcript.fetch()
        
        # 将字幕组合成文本
        full_text = " ".join([item['text'] for item in transcript_data])
        
        return {
            "url": url,
            "video_id": video_id,
            "transcript": full_text,
            "language": transcript.language,
            "status": "processed"
        }
    
    except NoTranscriptFound:
        return {
            "url": url,
            "video_id": video_id,
            "error": "找不到字幕",
            "status": "failed"
        }
    except TranscriptsDisabled:
        return {
            "url": url,
            "video_id": video_id,
            "error": "该视频已禁用字幕",
            "status": "failed"
        }
    except Exception as e:
        return {
            "url": url,
            "video_id": video_id,
            "error": f"处理出错: {str(e)}",
            "status": "failed"
        }

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return {"message": "Item created"}

@app.get("/items")
def get_items():
    return {"items": items}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item": items[item_id]}

# 添加这段代码以便在本地和生产环境都能运行
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 