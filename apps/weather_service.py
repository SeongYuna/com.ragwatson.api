"""Open-Meteo 기반 실시간 날씨 조회 (METEO_API_KEY 사용 시 customer API)."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from matrix.app.keymaker import keymaker

# 서울 기본값
_DEFAULT_LAT = 37.5665
_DEFAULT_LON = 126.9780

_WMO_KO: dict[int, str] = {
    0: "맑음",
    1: "대체로 맑음",
    2: "부분적으로 흐림",
    3: "흐림",
    45: "안개",
    48: "짙은 안개",
    51: "이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    61: "약한 비",
    63: "비",
    65: "강한 비",
    71: "약한 눈",
    73: "눈",
    75: "강한 눈",
    80: "소나기",
    81: "소나기",
    82: "강한 소나기",
    95: "뇌우",
    96: "뇌우와 우박",
    99: "강한 뇌우와 우박",
}


def _wmo_label(code: int | None) -> str:
    if code is None:
        return "알 수 없음"
    return _WMO_KO.get(code, "변화 많음")


def _http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ragwatson/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _forecast_url(latitude: float, longitude: float, api_key: str | None) -> str:
    params: dict[str, str | float] = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "auto",
    }
    if api_key:
        params["apikey"] = api_key
        base = "https://customer-api.open-meteo.com"
    else:
        base = "https://api.open-meteo.com"
    return f"{base}/v1/forecast?{urllib.parse.urlencode(params)}"


def _reverse_place(lat: float, lon: float) -> str:
    try:
        q = urllib.parse.urlencode(
            {"latitude": lat, "longitude": lon, "language": "ko", "count": 1}
        )
        data = _http_get(f"https://geocoding-api.open-meteo.com/v1/reverse?{q}")
        results = data.get("results") or []
        if results:
            r0 = results[0]
            name = r0.get("name") or ""
            admin = r0.get("admin1") or ""
            return f"{name} {admin}".strip() or "현재 위치"
    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        pass
    return "현재 위치"


def fetch_current_weather(lat: float | None = None, lon: float | None = None) -> dict:
    latitude = lat if lat is not None else _DEFAULT_LAT
    longitude = lon if lon is not None else _DEFAULT_LON

    api_key = keymaker.meteo_api_key or None
    try:
        if api_key:
            data = _http_get(_forecast_url(latitude, longitude, api_key))
        else:
            data = _http_get(_forecast_url(latitude, longitude, None))
    except urllib.error.HTTPError:
        # 키가 Open-Meteo commercial용이 아니거나 만료된 경우 무료 API로 대체
        data = _http_get(_forecast_url(latitude, longitude, None))
    current = data.get("current") or {}

    temp = current.get("temperature_2m")
    code = current.get("weather_code")
    humidity = current.get("relative_humidity_2m")
    wind = current.get("wind_speed_10m")

    return {
        "location": _reverse_place(latitude, longitude),
        "temperature": temp,
        "temperature_unit": (data.get("current_units") or {}).get(
            "temperature_2m", "°C"
        ),
        "description": _wmo_label(int(code) if code is not None else None),
        "humidity": humidity,
        "wind_speed": wind,
        "wind_speed_unit": (data.get("current_units") or {}).get(
            "wind_speed_10m", "km/h"
        ),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
