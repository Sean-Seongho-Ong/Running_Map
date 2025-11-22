"""
최종 통합 테스트 실행 및 워닝 확인 스크립트

Docker 실행 후 통합 테스트를 실행하고 워닝을 확인합니다.
"""

import subprocess
import sys
import re
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_tests():
    """통합 테스트 실행 및 워닝 확인"""
    logger.info("=" * 70)
    logger.info("통합 테스트 실행 및 워닝 확인")
    logger.info("=" * 70)
    
    # 1. 데이터베이스 통합 테스트
    logger.info("\n[1/4] 데이터베이스 통합 테스트 실행 중...")
    logger.info("-" * 70)
    result_db = subprocess.run(
        [sys.executable, "-m", "pytest", 
         "tests/infrastructure/integration/test_database_integration.py", 
         "-v", "--tb=line"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    # 결과 분석
    db_passed = len(re.findall(r'PASSED', result_db.stdout))
    db_failed = len(re.findall(r'FAILED', result_db.stdout))
    db_errors = len(re.findall(r'ERROR', result_db.stdout))
    
    logger.info(f"통과: {db_passed}, 실패: {db_failed}, 오류: {db_errors}")
    if db_failed > 0 or db_errors > 0:
        logger.error("\n실패/오류 상세:")
        for line in result_db.stdout.split('\n'):
            if 'FAILED' in line or 'ERROR' in line or 'Error' in line:
                logger.error(f"  {line[:100]}")
    
    # 2. Redis 통합 테스트
    logger.info("\n[2/4] Redis 통합 테스트 실행 중...")
    logger.info("-" * 70)
    result_redis = subprocess.run(
        [sys.executable, "-m", "pytest", 
         "tests/infrastructure/integration/test_redis_integration.py", 
         "-v", "--tb=line"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    # 결과 분석
    redis_passed = len(re.findall(r'PASSED', result_redis.stdout))
    redis_failed = len(re.findall(r'FAILED', result_redis.stdout))
    redis_errors = len(re.findall(r'ERROR', result_redis.stdout))
    
    logger.info(f"통과: {redis_passed}, 실패: {redis_failed}, 오류: {redis_errors}")
    if redis_failed > 0 or redis_errors > 0:
        logger.error("\n실패/오류 상세:")
        for line in result_redis.stdout.split('\n'):
            if 'FAILED' in line or 'ERROR' in line or 'Error' in line:
                logger.error(f"  {line[:100]}")
    
    # 3. Interface 테스트 워닝 확인
    logger.info("\n[3/4] Interface 테스트 워닝 확인 중...")
    logger.info("-" * 70)
    result_interface = subprocess.run(
        [sys.executable, "-m", "pytest", 
         "tests/interface/api/v1/", "-v"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    # 워닝 추출
    warnings = []
    for line in result_interface.stdout.split('\n'):
        if 'warning' in line.lower() or 'Warning' in line or 'WARNING' in line:
            warnings.append(line.strip())
    
    if warnings:
        logger.warning(f"⚠️ 발견된 워닝: {len(warnings)}개")
        for i, warning in enumerate(warnings[:10], 1):
            logger.warning(f"  {i}. {warning}")
    else:
        logger.info("✅ 워닝 없음")
    
    # 4. 전체 테스트 요약
    logger.info("\n[4/4] 전체 테스트 요약")
    logger.info("-" * 70)
    logger.info(f"데이터베이스 테스트: 통과 {db_passed}, 실패 {db_failed}, 오류 {db_errors}")
    logger.info(f"Redis 테스트: 통과 {redis_passed}, 실패 {redis_failed}, 오류 {redis_errors}")
    logger.info(f"Interface 테스트 워닝: {len(warnings)}개")
    
    total_passed = db_passed + redis_passed
    total_failed = db_failed + redis_failed + db_errors + redis_errors
    
    logger.info(f"\n총계: 통과 {total_passed}, 실패/오류 {total_failed}")
    
    if total_failed == 0 and len(warnings) == 0:
        logger.info("\n✅ 모든 테스트 통과, 워닝 없음!")
    elif total_failed == 0:
        logger.info(f"\n✅ 모든 테스트 통과 (워닝 {len(warnings)}개)")
    else:
        logger.warning(f"\n⚠️ 일부 테스트 실패 (실패 {total_failed}개, 워닝 {len(warnings)}개)")
    
    logger.info("\n" + "=" * 70)
    logger.info("테스트 완료")
    logger.info("=" * 70)
    
    return {
        'db_passed': db_passed,
        'db_failed': db_failed,
        'redis_passed': redis_passed,
        'redis_failed': redis_failed,
        'warnings': len(warnings)
    }

if __name__ == "__main__":
    try:
        results = run_tests()
        sys.exit(0 if results['db_failed'] == 0 and results['redis_failed'] == 0 else 1)
    except Exception as e:
        logger.error(f"\n❌ 오류 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
