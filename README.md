# data-analyzer

로봇 분야 데이터 EDA와 차원 축소 실험을 위한 코드베이스입니다.  
아래는 Hugging Face에 있는 Lerobot·LIBERO·MetaWorld 데이터셋을 내려받는 기본 흐름 예시입니다.

---

## 1. 환경 준비

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # huggingface_hub 포함
```

> 필요하면 `pip install huggingface_hub`만 별도로 실행해도 됩니다.

허깅페이스 인증이 필요한 리포는 아래 중 하나를 먼저 실행하세요.

```bash
hf auth login         # 인터랙티브 로그인
# 또는
export HF_TOKEN=hf_xxx        # 토큰을 직접 환경 변수에 지정
```

### src 레이아웃 주의

이 프로젝트는 `src/` 레이아웃을 사용합니다. `python scripts/...` 처럼 직접 실행할 때는 Python이 `src`를 검색하도록 `PYTHONPATH`를 지정해야 합니다.

```bash
export PYTHONPATH="$PWD/src"        # 셸 세션마다 1회 설정
# 또는
PYTHONPATH=src python scripts/download_data.py ...
```

`poetry run`, `pip install -e .` 등으로 실행하는 경우엔 도구가 자동으로 경로를 추가하므로 별도 설정이 필요 없습니다.

---

## 2. 데이터 다운로드 예제

기본 구문

```bash
python scripts/download_data.py \
  --repo-id <org>/<dataset> \
  --target-dir data/raw \
  --log-level INFO
```

### 2.1 Lerobot (pusht)

```bash
python scripts/download_data.py \
  --repo-id lerobot/pusht \
  --target-dir data/raw
```

### 2.2 LIBERO (예: libero_spatial)

```bash
python scripts/download_data.py \
  --repo-id Libero/libero_spatial \
  --target-dir data/raw
```

### 2.3 MetaWorld MT50

```bash
python scripts/download_data.py \
  --repo-id metaworld/MT50 \
  --target-dir data/raw
```

---

## 3. 자주 쓰는 옵션

- `--revision main` : 특정 브랜치/태그/커밋을 명시하고 싶을 때
- `--allow "*.hdf5" --allow "*.json"` : 지정한 패턴만 내려받기 (반복 사용 가능)
- `--ignore "videos/*"` : 특정 경로 제외
- `--force-download` : 기존 파일이 있어도 다시 받기
- `--no-resume` : 부분 다운로드된 파일을 이어받지 않음
- `--token "$HF_TOKEN"` : 환경 변수 대신 CLI 인자로 토큰 전달

모든 스냅샷은 `data/raw/<org>__<dataset>/` 아래에 저장됩니다. 이후 EDA/전처리 코드는 `src/`와 `scripts/`에 추가될 예정입니다.
