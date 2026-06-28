from fastapi import FastAPI, HTTPException
from instagrapi import Client
import os

app = FastAPI(title="Instagrapi API", version="1.0.0")

cl = Client()
logged_in = False

def get_client():
    global logged_in
    if not logged_in:
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        proxy = os.getenv("PROXY_URL", "")
        if not username or not password:
            raise HTTPException(status_code=500, detail="INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD não configurados")
        if proxy:
            cl.set_proxy(proxy)
        cl.login(username, password)
        logged_in = True
    return cl

@app.get("/")
def root():
    return {"status": "ok", "message": "Instagrapi API running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/profile/{username}")
def get_profile(username: str):
    client = get_client()
    try:
        user = client.user_info_by_username(username)
        return {
            "username": user.username,
            "full_name": user.full_name,
            "biography": user.biography,
            "followers": user.follower_count,
            "following": user.following_count,
            "posts": user.media_count,
            "profile_pic": str(user.profile_pic_url),
            "is_private": user.is_private,
            "is_verified": user.is_verified,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profile/{username}/posts")
def get_user_posts(username: str, amount: int = 12):
    client = get_client()
    try:
        user_id = client.user_id_from_username(username)
        medias = client.user_medias(user_id, amount=amount)
        posts = []
        for m in medias:
            posts.append({
                "id": str(m.id),
                "type": m.media_type,
                "caption": m.caption_text if m.caption_text else "",
                "likes": m.like_count,
                "comments": m.comment_count,
                "url": str(m.thumbnail_url or (m.resources[0].thumbnail_url if m.resources else "")),
                "taken_at": str(m.taken_at),
                "link": f"https://www.instagram.com/p/{m.code}/"
            })
        return {"username": username, "total": len(posts), "posts": posts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
