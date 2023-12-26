from pytube import YouTube


def mega_filter(title: str) -> str:
    title1 = title.replace(".", "")
    title2 = title1.replace(" ", "")
    title3 = title2.replace("/", "")
    title_end = title3.replace(":", "")
    return title_end


def download_youtube_video(video_url: str, rs: str):
    # Створення об'єкта YouTube
    yt = YouTube(video_url)
    title = "".join(c for c in yt.title if c.isalpha())
    output_path = f"C:/Users/DELL/PycharmProjects/Швейцарський ніж/services/temp_videos"  # Виведення інформації про відео
    streams = yt.streams
    video_stream = streams.filter(res=rs).desc().first()
    # Завантаження відео
    video_stream.download(output_path, title + ".mp4")


def printVideo_res(link):
    yt = YouTube(link)
    resolutions = sorted(
        set(stream.resolution for stream in yt.streams.filter(type='video')),
        key=lambda s: int(s.split('p')[0])
    )
    return resolutions
