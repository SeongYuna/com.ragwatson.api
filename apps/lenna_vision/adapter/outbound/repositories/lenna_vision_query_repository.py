import os

import boto3
from sqlalchemy.ext.asyncio import AsyncSession

from lenna_vision.app.dtos.lenna_vision_dto import (
    LennaImageUploadCommand,
    LennaImageUploadResult,
    LennaVisionIntroduceQuery,
    LennaVisionIntroduceResult,
)
from lenna_vision.app.ports.output.lenna_vision_port import LennaVisionPort

_S3_BUCKET = os.getenv("LENNA_S3_BUCKET")
_S3_REGION = os.getenv("AWS_REGION", "ap-northeast-2")


class LennaVisionQueryRepository(LennaVisionPort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._s3_client = boto3.client("s3", region_name=_S3_REGION)

    async def introduce_myself(self, query: LennaVisionIntroduceQuery) -> LennaVisionIntroduceResult:
        return LennaVisionIntroduceResult(
            id=query.id,
            name=query.name,
            message='LennaVision입니다.',
        )

    async def save_image(self, command: LennaImageUploadCommand) -> LennaImageUploadResult:
        if not _S3_BUCKET:
            raise RuntimeError("LENNA_S3_BUCKET 환경 변수가 설정되지 않았습니다.")

        self._s3_client.put_object(
            Bucket=_S3_BUCKET,
            Key=command.filename,
            Body=command.content,
        )
        url = f"https://{_S3_BUCKET}.s3.{_S3_REGION}.amazonaws.com/{command.filename}"
        return LennaImageUploadResult(
            filename=command.filename,
            size=len(command.content),
            path=url,
        )
