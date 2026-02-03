from fastapi import FastAPI, Response
from datetime import datetime
import textwrap

app = FastAPI()

# 깃허브 raw 파일 기본 주소 완성
BASE_IMAGE_URL = f"https://k-popcorn.github.io/hp"

@app.get("/")
async def root():
    return {"message": "호그와트 인스타 서버 작동 중! /api/insta-post-real 경로를 이용하세요."}

@app.get("/api/insta-post-real")
async def get_insta_post_real(
    filename: str, 
    content: str, 
    user_id: str = "ai_chatbot_kr",  # [추가됨] 사용자 ID 받기
    date_str: str = None, 
    likes: int = 1234, 
    shares: int = 56
):
    full_image_url = f"{BASE_IMAGE_URL}/{filename}"
    
    if date_str is None: 
        date_str = datetime.now().strftime("%Y년 %m월 %d일")

    # -------------------------------------------------------
    # [핵심 수정] 텍스트 줄바꿈 로직 (아이디 길이 고려)
    # -------------------------------------------------------
    # 한 줄에 들어갈 대략적인 글자 수 (약 40자)
    MAX_WIDTH = 40
    
    # 1. 아이디 길이를 고려해서 '첫 줄에 남은 공간' 계산
    # (아이디가 길면 첫 줄에 본문이 조금만 들어감)
    id_len = len(user_id)
    first_line_capacity = max(5, MAX_WIDTH - id_len - 2) # 최소 5글자는 보장
    
    # 2. 본문 내용을 첫 줄과 나머지로 분리
    wrapped_lines = textwrap.wrap(content, width=MAX_WIDTH)
    
    # 첫 줄이 너무 길면 강제로 자르기 (아이디 옆에 붙어야 하므로)
    tspans = ""
    
    if wrapped_lines:
        # 첫 번째 줄 처리: x좌표를 지정하지 않음 -> 아이디 바로 뒤에 이어서 출력됨 (dx 사용)
        first_line = wrapped_lines[0]
        tspans += f'<tspan dx="5">{first_line}</tspan>'
        
        # 나머지 줄 처리: x="20"으로 지정 -> 다음 줄부터는 왼쪽 정렬
        # textwrap을 다시 돌려서 나머지 문장 정리
        remaining_text = " ".join(wrapped_lines[1:])
        if remaining_text:
            subsequent_lines = textwrap.wrap(remaining_text, width=MAX_WIDTH)
            for line in subsequent_lines:
                tspans += f'<tspan x="20" dy="18">{line}</tspan>'
    
    # -------------------------------------------------------

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
         <defs>
            <clipPath id="profile-clip">
                <circle cx="16" cy="16" r="16" />
            </clipPath>
         </defs>
         <circle cx="16" cy="16" r="16" fill="#DBDBDB" />
         
         <text x="42" y="21" class="username">{user_id}</text>
         
         <circle cx="355" cy="16" r="1.5" fill="#262626"/>
         <circle cx="360" cy="16" r="1.5" fill="#262626"/>
         <circle cx="350" cy="16" r="1.5" fill="#262626"/>
      </g>

      <image x="0" y="54" width="375" height="375" xlink:href="{full_image_url}" preserveAspectRatio="xMidYMid slice"/>

      <g transform="translate(12, 440)">
        <path d="M16.792 3.904A4.989 4.989 0 0 1 21.5 9.122c0 3.072-2.652 4.956-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 0 1 4.708-5.218 4.21 4.21 0 0 1 3.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 0 1 3.679-1.938m0-2.5c-2.527 0-4.471 1.06-5.285 2.555-1.002-1.636-2.936-2.555-5.003-2.555C3.015 1.35.5 3.968.5 7.172c0 4.636 6 8.36 11.5 13.328 5.5-4.968 11.5-8.692 11.5-13.328 0-3.204-2.515-5.822-6.208-5.822z" fill="#262626"/>
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
