from __future__ import annotations


class UiAvatarsApi:
    @staticmethod
    def get_avatar_url(name: str, background: str | None = None, size: int | None = None) -> str:
        params = [f"name={name.strip()}"]
        if background:
            params.append(f"background={background.strip()}")
        if size is not None:
            params.append(f"size={size}")
        return "https://ui-avatars.com/api/?" + "&".join(params)


def get_avatar_url(name: str, background: str | None = None, size: int | None = None) -> str:
    return UiAvatarsApi.get_avatar_url(name, background=background, size=size)
