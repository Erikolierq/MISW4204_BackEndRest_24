from dataclasses import dataclass
from typing import Tuple
from ..modelos import User, Video, Vote, VideoLeaderboard,db

@dataclass
class ResultadoBuscarVideo:
    video: Video = None
    error: Tuple = ()

def buscar_video(video_id: int, current_user_id: int) -> ResultadoBuscarVideo:
    resultado_buscar_video = ResultadoBuscarVideo()
    video = Video.query.filter_by(Video.id==video_id, user_id=current_user_id).first()
    if not video:
        resultado_buscar_video.error = ({'mensaje': 'Video no encontrado o no tienes permiso para acceder a este video.'}, 404)
    resultado_buscar_video.video = video
    return resultado_buscar_video