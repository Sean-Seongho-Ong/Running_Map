"""
TestClient 디버깅 스크립트

TestClient 오류를 재현하고 원인을 확인합니다.
"""

from starlette.testclient import TestClient
from main import app

print("=" * 60)
print("TestClient 디버깅")
print("=" * 60)

print("\n1. TestClient 생성 시도...")
try:
    client = TestClient(app)
    print("✅ SUCCESS: TestClient가 정상적으로 생성되었습니다.")
    print(f"   Client type: {type(client)}")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
    print(f"   Error details: {str(e)}")
    
    # 추가 정보
    import traceback
    print("\n   Full traceback:")
    traceback.print_exc()

print("\n2. 패키지 버전 확인...")
try:
    import fastapi
    import starlette
    import httpx
    print(f"   FastAPI: {fastapi.__version__}")
    print(f"   Starlette: {starlette.__version__}")
    print(f"   httpx: {httpx.__version__}")
except Exception as e:
    print(f"   Version check failed: {e}")

print("\n3. TestClient.__init__ 시그니처 확인...")
try:
    import inspect
    sig = inspect.signature(TestClient.__init__)
    print(f"   TestClient.__init__ signature:")
    print(f"   {sig}")
except Exception as e:
    print(f"   Signature check failed: {e}")

print("\n4. httpx.Client.__init__ 시그니처 확인...")
try:
    from httpx import Client
    import inspect
    sig = inspect.signature(Client.__init__)
    params = list(sig.parameters.keys())[:10]
    print(f"   httpx.Client.__init__ first 10 parameters:")
    print(f"   {params}")
except Exception as e:
    print(f"   Client signature check failed: {e}")

print("\n" + "=" * 60)

