#!/usr/bin/env python3
"""CLI helper to download Lerobot datasets."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from data_analyzer.data import download_lerobot_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Lerobot dataset snapshots from Hugging Face."
    )
    parser.add_argument(
        "--repo-id",
        required=True,
        help="Hugging Face dataset repo id, e.g. lerobot/pusht",
    )
    parser.add_argument(
        "--revision",
        default=None,
        help="Optional git revision; defaults to the repo's default branch.",
    )
    parser.add_argument(
        "--target-dir",
        default="data/raw",
        help="Base directory where the dataset will be stored.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HF_TOKEN"),
        help="Hugging Face token (falls back to HF_TOKEN env).",
    )
    parser.add_argument(
        "--allow",
        action="append",
        dest="allow_patterns",
        help="Glob pattern(s) to whitelist (can repeat).",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        dest="ignore_patterns",
        help="Glob pattern(s) to blacklist (can repeat).",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Re-download files even if they exist locally.",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Disable resume for partially downloaded files.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, ...).",
    )
    return parser.parse_args()


def main() -> int:
    # CLI 인자를 파싱하고 로깅 레벨을 설정한다.
    args = parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s %(name)s: %(message)s",
    )

    # 파싱한 값을 그대로 downloader 헬퍼에 넘겨 실제 다운로드를 수행한다.
    snapshot_path = download_lerobot_dataset(
        repo_id=args.repo_id,
        revision=args.revision,
        target_dir=Path(args.target_dir),
        allow_patterns=args.allow_patterns,
        ignore_patterns=args.ignore_patterns,
        token=args.token,
        force_download=args.force_download,
        resume_download=not args.no_resume,
    )

    # 완료 경로를 남긴 뒤 종료 코드를 반환한다.
    logging.info("Done. Snapshot stored at %s", snapshot_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
