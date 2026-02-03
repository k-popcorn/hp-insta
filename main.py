from fastapi import FastAPI, Response
from datetime import datetime
import textwrap

app = FastAPI()

# 깃허브 raw 파일 기본 주소 완성
BASE_IMAGE_URL = f"https://k-popcorn.github.io/hp"

def wrap_text_to_tspans(text, width, x_pos, line_height):
    # (이전과 동일한 줄바꿈 함수)
    lines = textwrap.wrap(text, width=35)
    tspans = ""
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        tspans += f'<tspan x="{x_pos}" dy="{dy}">{line}</tspan>'
    return tspans

@app.get("/api/insta-post-real")
async def get_insta_post_real(
    filename: str, content: str, date_str: str = None, 
    likes: int = 1234, shares: int = 56
):
    full_image_url = f"{BASE_IMAGE_URL}/{filename}"
    if date_str is None: date_str = datetime.now().strftime("%Y년 %m월 %d일")
    
    # 텍스트 줄바꿈 (이전과 동일)
    wrapped_content = wrap_text_to_tspans(content, 40, 15, 18)

    # ★ 핵심 변경점: 인스타 실제 아이콘 Path & 정확한 색상 적용
    svg_template = f"""
    <svg width="375" height="550" viewBox="0 0 375 550" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
      <style>
        /* 폰트를 최대한 모바일과 비슷하게 설정 */
        text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        .username {{ font-weight: 600; font-size: 14px; fill: #262626; }}
        .meta {{ font-size: 11px; fill: #8E8E8E; }}
        .likes {{ font-weight: 600; font-size: 14px; fill: #262626; }}
      </style>
      
      <rect width="375" height="550" fill="#ffffff" />

      <g transform="translate(10, 10)">
         <defs>
            <clipPath id="profile-clip">
                <circle cx="16" cy="16" r="16" />
            </clipPath>
         </defs>
         <circle cx="16" cy="16" r="16" fill="#DBDBDB" />
         <text x="42" y="21" class="username">ai_chatbot_kr</text>
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
         
         <text y="24" font-size="14" fill="#262626" font-family="-apple-system, sans-serif">
           <tspan font-weight="600">ai_chatbot_kr</tspan>
           <tspan dx="5"> </tspan>
           {wrapped_content}
         </text>
         
         <text y="60" class="meta">{date_str}</text>
      </g>
    </svg>
    """
    return Response(content=svg_template, media_type="image/svg+xml")
