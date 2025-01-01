from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone, date
from app.config import settings
import jwt
from fastapi import HTTPException
import shutil
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import cv2


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET_KEY
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def encode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="wrong token or token expire")
    

def save_file(file, path):
    with open(path, "bw+") as new_file:
        shutil.copyfileobj(file, new_file)


def create_url_safe_token(data: dict, expiration=3600):
    return serializer.dumps(data)


def decode_url_safe_token(token: str, max_age=3600):
    try:
        token_data = serializer.loads(token, max_age=max_age)
        return token_data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")


def get_primary_color(image_path, n_colors=1):
    # Open the image
    image = Image.open(image_path)

    # Handle GIFs with multiple frames
    if getattr(image, "is_animated", False):
        image.seek(0)  # Process the first frame only

    # Convert to RGB mode to handle palette or alpha issues
    image = image.convert("RGB")

    # Convert the image to a NumPy array
    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3)  # Reshape to list of pixels

    # Use KMeans clustering to find the most dominant colors
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[0]  # Get the most dominant color

    # Return the dominant color as an RGB tuple
    return tuple(map(int, dominant_color))


def extract_first_frame(video_path, output_image_path=None):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not video.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")
    
    # Read the first frame
    success, frame = video.read()
    if not success:
        raise ValueError(f"Cannot read the first frame from {video_path}")
    
    # Save the frame as an image if an output path is provided
    if output_image_path:
        cv2.imwrite(output_image_path, frame)
    
    # Release the video object
    video.release()
    
    # Return the frame as a NumPy array
    return frame