from fastapi import FastAPI, Response
from datetime import datetime
import textwrap
import httpx
import base64

app = FastAPI()

# 깃허브 raw 파일 기본 주소 완성
BASE_IMAGE_URL = f"https://k-popcorn.github.io/hp"

@app.get("/")
async def root():
    return {"message": "서버 정상 작동 중!"}

# [기능 추가] 이미지를 다운받아 Base64 코드로 변환하는 함수
async def get_image_base64(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                # 바이너리 데이터를 base64 문자열로 변환
                encoded_string = base64.b64encode(response.content).decode("utf-8")
                return f"data:image/png;base64,{encoded_string}"
            else:
                return None # 이미지 다운 실패 시
        except:
            return None

@app.get("/api/insta-post-real")
async def get_insta_post_real(
    filename: str, 
    content: str, 
    user_id: str = "ai_chatbot_kr",  # [추가됨] 사용자 ID 받기
    date_str: str = None, 
    likes: int = 1234, 
    shares: int = 56
):
    target_url = f"{BASE_IMAGE_URL}/{filename}"
    base64_image = await get_image_base64(target_url)
    # 만약 이미지를 못 불러오면 회색 박스로 대체
    if base64_image is None:
        image_href = "" # 빈 값
        placeholder = '<rect x="0" y="54" width="375" height="375" fill="#eeeeee"/><text x="187" y="240" text-anchor="middle" fill="#aaaaaa">Image Not Found</text>'
    else:
        image_href = base64_image
        placeholder = ""
    
    if date_str is None: 
        date_str = datetime.now().strftime("%Y년 %m월 %d일")

    # -------------------------------------------------------
    # [핵심 수정] 텍스트 줄바꿈 로직 (아이디 길이 고려)
    # -------------------------------------------------------
    # 한 줄에 들어갈 대략적인 글자 수 (약 40자)
    # 3. 텍스트 줄바꿈 로직 (이전과 동일하게 완벽 적용)
    MAX_WIDTH = 40
    id_len = len(user_id)
    wrapped_lines = textwrap.wrap(content, width=MAX_WIDTH)
    
    tspans = ""
    if wrapped_lines:
        first_line = wrapped_lines[0]
        tspans += f'<tspan dx="5">{first_line}</tspan>'
        remaining_text = " ".join(wrapped_lines[1:])
        if remaining_text:
            subsequent_lines = textwrap.wrap(remaining_text, width=MAX_WIDTH)
            for line in subsequent_lines:
                tspans += f'<tspan x="20" dy="18">{line}</tspan>'

    # 4. SVG 템플릿
    svg_template = f"""
    <svg width="375" height="550" viewBox="0 0 375 550" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <style>
        text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        .username {{ font-weight: 600; font-size: 14px; fill: #262626; }}
        .meta {{ font-size: 11px; fill: #8E8E8E; }}
        .likes {{ font-weight: 600; font-size: 14px; fill: #262626; }}
        .caption {{ font-size: 14px; fill: #262626; }}
      </style>
      
      <rect width="375" height="550" fill="#ffffff" />

      <g transform="translate(10, 10)">
         <clipPath id="profile-clip"><circle cx="16" cy="16" r="16" /></clipPath>
         <circle cx="16" cy="16" r="16" fill="#DBDBDB" />
         <text x="42" y="21" class="username">{user_id}</text>
         <circle cx="355" cy="16" r="1.5" fill="#262626"/>
         <circle cx="360" cy="16" r="1.5" fill="#262626"/>
         <circle cx="350" cy="16" r="1.5" fill="#262626"/>
      </g>

      {placeholder}
      <image x="0" y="54" width="375" height="375" xlink:href="{image_href}" preserveAspectRatio="xMidYMid slice"/>

      <g transform="translate(12, 440)">
        <path d="M16.792 3.904A4.989 4.989 0 0 1 21.5 9.122c0 3.072-2.652 4.956-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 0 1 4.7-5.218 4.21 4.21 0 0 1 3.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 0 1 3.679-1.938m0-2.5c-2.527 0-4.471 1.06-5.285 2.555-1.002-1.636-2.936-2.555-5.003-2.555C3.015 1.35.5 3.968.5 7.172c0 4.636 6 8.36 11.5 13.328 5.5-4.968 11.5-8.692 11.5-13.328 0-3.204-2.515-5.822-6.208-5.822z" fill="#262626"/>
        <path d="M20.656 17.008a9.993 9.993 0 1 0-3.59 3.615L22 22z" fill="none" stroke="#262626" stroke-linejoin="round" stroke-width="2" transform="translate(28, -2) scale(0.9)"/>
        <path d="M21.5 2L14 22l-4-9-9-4z" fill="none" stroke="#262626" stroke-linejoin="round" stroke-width="2" transform="translate(62, -2) scale(0.9)"/>
        <path d="M20 21l-8-6.5L4 21V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" fill="none" stroke="#262626" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" transform="translate(325, -2) scale(0.9)"/>
      </g>

      <g transform="translate(15, 480)">
         <text class="likes">좋아요 {likes:,}개</text>
         <text y="24" class="caption">
           <tspan font-weight="600">{user_id}</tspan>
           {tspans}
         </text>
         <text y="60" class="meta">{date_str}</text>
      </g>
    </svg>
    """
    
    return Response(content=svg_template, media_type="image/svg+xml")
