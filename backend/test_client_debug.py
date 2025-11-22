"""
TestClient 디버깅 스크립트

TestClient 오류를 재현하고 원인을 확인합니다.
"""

import logging
from starlette.testclient import TestClient
from main import app

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("TestClient 디버깅")
logger.info("=" * 60)

logger.info("\n1. TestClient 생성 시도...")
try:
    client = TestClient(app)
    logger.info("✅ SUCCESS: TestClient가 정상적으로 생성되었습니다.")
    logger.info(f"   Client type: {type(client)}")
except Exception as e:
    logger.error(f"❌ ERROR: {type(e).__name__}: {e}")
    logger.error(f"   Error details: {str(e)}")
    
    # 추가 정보
    import traceback
    logger.error("\n   Full traceback:")
    logger.error(traceback.format_exc())

logger.info("\n2. 패키지 버전 확인...")
try:
    import fastapi
    import starlette
    import httpx
    logger.info(f"   FastAPI: {fastapi.__version__}")
    logger.info(f"   Starlette: {starlette.__version__}")
    logger.info(f"   httpx: {httpx.__version__}")
except Exception as e:
    logger.error(f"   Version check failed: {e}")

logger.info("\n3. TestClient.__init__ 시그니처 확인...")
try:
    import inspect
    sig = inspect.signature(TestClient.__init__)
    logger.info(f"   TestClient.__init__ signature:")
    logger.info(f"   {sig}")
except Exception as e:
    logger.error(f"   Signature check failed: {e}")

logger.info("\n4. httpx.Client.__init__ 시그니처 확인...")
try:
    from httpx import Client
    import inspect
    sig = inspect.signature(Client.__init__)
    params = list(sig.parameters.keys())[:10]
    logger.info(f"   httpx.Client.__init__ first 10 parameters:")
    logger.info(f"   {params}")
except Exception as e:
    logger.error(f"   Client signature check failed: {e}")

logger.info("\n" + "=" * 60)

