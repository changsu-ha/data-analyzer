"""Utilities for downloading Lerobot datasets from Hugging Face."""

from __future__ import annotations  # forward references for annotations

import logging  # standard logging for progress info
from pathlib import Path  # filesystem path handling
from typing import Iterable, Optional  # type hint helpers

from huggingface_hub import snapshot_download  # HF utility that pulls repo snapshots

# 모듈 전역 로거: 외부에서 호출해도 동일한 포맷으로 진행 상황을 확인할 수 있다.
LOGGER = logging.getLogger(__name__)


def _sanitize_repo_id(repo_id: str) -> str:
    """Convert repo id (org/name) into a filesystem friendly string."""
    # 슬래시를 폴더명에 안전한 문자열로 치환한다.
    return repo_id.replace("/", "__")


def download_lerobot_dataset(
    repo_id: str,
    *,
    revision: str | None = None,
    target_dir: str | Path = "data/raw",
    allow_patterns: Optional[Iterable[str]] = None,
    ignore_patterns: Optional[Iterable[str]] = None,
    token: Optional[str] = None,
    force_download: bool = False,
    resume_download: bool = True,
) -> Path:
    """
    Download a Lerobot dataset from Hugging Face.

    Parameters
    ----------
    repo_id:
        Hugging Face dataset repo id (e.g. ``lerobot/pusht``).
    revision:
        Optional git revision (branch, tag, or commit SHA). Defaults to
        the repo's default branch when ``None``.
    target_dir:
        Base directory where the dataset will be stored locally.
    allow_patterns / ignore_patterns:
        Optional filtering rules passed to ``snapshot_download`` to limit the
        files that get downloaded (see huggingface_hub docs).
    token:
        Hugging Face token to use when the repo is gated/private.
    force_download:
        If True, re-download files even if they already exist.
    resume_download:
        If True, resume partially downloaded files.

    Returns
    -------
    pathlib.Path
        Path to the local dataset snapshot.
    """

    base_dir = Path(target_dir)  # 루트 저장소를 Path 객체로 변환
    destination = base_dir / _sanitize_repo_id(repo_id)  # repo별 하위 폴더 결정
    destination.parent.mkdir(parents=True, exist_ok=True)  # 상위 폴더가 없다면 생성

    LOGGER.info(
        "Downloading Lerobot dataset '%s' into %s (revision=%s)",
        repo_id,
        destination,
        revision or "default",
    )

    snapshot_path = snapshot_download(
        repo_id=repo_id,  # 허깅페이스 데이터셋 repo 식별자
        repo_type="dataset",  # 데이터셋 스냅샷으로 한정
        revision=revision,  # 특정 브랜치/커밋 요청 가능
        local_dir=destination,  # 로컬 저장 위치
        local_dir_use_symlinks=False,  # 실제 파일 복사로 안전하게 저장
        allow_patterns=allow_patterns,  # 필요한 파일만 선택적으로 받기
        ignore_patterns=ignore_patterns,  # 제외할 패턴 지정
        token=token,  # 보호된 리포 접근 토큰
        force_download=force_download,  # 기존 파일 있어도 다시 받기 여부
        resume_download=resume_download,  # 중단된 다운로드 이어받기
    )

    LOGGER.info("Dataset downloaded to %s", snapshot_path)
    return Path(snapshot_path)  # 호출 측에서 Path API를 계속 쓸 수 있도록 Path로 감싼다
