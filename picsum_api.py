from __future__ import annotations


class PicsumApi:
    @staticmethod
    def get_picsum_url(width: int = 800, height: int = 500, grayscale: bool = False, blur: int | None = None) -> str:
        params = []
        if grayscale:
            params.append("grayscale")
        if blur is not None:
            params.append(f"blur={blur}")
        query = ""
        if params:
            query = "?" + "&".join(params)
        return f"https://picsum.photos/{width}/{height}{query}"


def get_picsum_url(width: int = 800, height: int = 500, grayscale: bool = False, blur: int | None = None) -> str:
    return PicsumApi.get_picsum_url(width, height, grayscale=grayscale, blur=blur)