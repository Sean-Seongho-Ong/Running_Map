"""
Test Data Seeding Script

테스트용 샘플 코스 데이터를 데이터베이스에 삽입합니다.
MockLoopGenerator를 사용하여 더미 코스를 생성하고 저장합니다.
"""

import asyncio
import logging
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from domain.entities.course import Course, CourseMetadata
from interface.mock_loop_generator import MockLoopGenerator
from application.use_cases.generate_course import GenerateCourseUseCase
from application.use_cases.save_course import SaveCourseUseCase
from application.dto.course_dto import (
    CourseGenerationRequestDTO,
    CoordinateDTO,
    CourseSaveRequestDTO,
)
from infrastructure.database.repositories.course_repository import CourseRepositoryImpl
from infrastructure.database.session import AsyncSessionLocal, init_db

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 테스트 데이터 정의
TEST_COURSES = [
    {
        "name": "서울 한강공원 3km",
        "location": (37.5665, 126.9780),  # 서울시청
        "distance": 3.0,
    },
    {
        "name": "서울 한강공원 5km",
        "location": (37.5665, 126.9780),
        "distance": 5.0,
    },
    {
        "name": "서울 한강공원 10km",
        "location": (37.5665, 126.9780),
        "distance": 10.0,
    },
    {
        "name": "부산 해운대 3km",
        "location": (35.1587, 129.1604),  # 부산 해운대
        "distance": 3.0,
    },
    {
        "name": "부산 해운대 5km",
        "location": (35.1587, 129.1604),
        "distance": 5.0,
    },
    {
        "name": "제주시 5km",
        "location": (33.4996, 126.5312),  # 제주시
        "distance": 5.0,
    },
    {
        "name": "제주시 10km",
        "location": (33.4996, 126.5312),
        "distance": 10.0,
    },
    {
        "name": "대전 유성구 3km",
        "location": (36.3628, 127.3845),  # 대전 유성구
        "distance": 3.0,
    },
    {
        "name": "대전 유성구 5km",
        "location": (36.3628, 127.3845),
        "distance": 5.0,
    },
]


async def seed_test_data(clear_existing: bool = False):
    """
    테스트용 샘플 코스 데이터를 데이터베이스에 삽입합니다.
    
    Args:
        clear_existing: 기존 데이터를 삭제할지 여부
    """
    # 데이터베이스 초기화
    await init_db()
    logger.info("데이터베이스 초기화 완료")
    
    # MockLoopGenerator 및 UseCase 생성
    loop_generator = MockLoopGenerator()
    generate_use_case = GenerateCourseUseCase(loop_generator=loop_generator)
    
    async with AsyncSessionLocal() as session:
        course_repository = CourseRepositoryImpl(session)
        save_use_case = SaveCourseUseCase(course_repository=course_repository)
        
        # 기존 데이터 삭제 (선택사항)
        if clear_existing:
            logger.info("기존 코스 데이터 삭제 중...")
            # 모든 코스 조회 후 삭제
            courses = await course_repository.list(limit=1000)
            for course in courses:
                await course_repository.delete(course.id)
            await session.commit()
            logger.info(f"{len(courses)}개의 기존 코스 삭제 완료")
        
        # 테스트 코스 생성 및 저장
        created_count = 0
        failed_count = 0
        
        for test_course in TEST_COURSES:
            try:
                logger.info(
                    f"코스 생성 중: {test_course['name']} "
                    f"({test_course['location'][0]}, {test_course['location'][1]}) "
                    f"{test_course['distance']}km"
                )
                
                # 1. 코스 생성
                generation_request = CourseGenerationRequestDTO(
                    start_point=CoordinateDTO(
                        latitude=test_course['location'][0],
                        longitude=test_course['location'][1]
                    ),
                    target_distance=test_course['distance'],
                )
                
                generation_response = await generate_use_case.execute(generation_request)
                
                if not generation_response.course:
                    logger.error(f"코스 생성 실패: {test_course['name']}")
                    failed_count += 1
                    continue
                
                # 2. 코스 저장
                save_request = CourseSaveRequestDTO(
                    name=test_course['name'],
                    polyline=generation_response.course.polyline,  # 이미 CoordinateDTO 리스트
                    distance=generation_response.course.distance,
                    is_public=True,
                )
                
                saved_course = await save_use_case.execute(save_request)
                await session.commit()
                
                logger.info(
                    f"코스 저장 완료: {saved_course.name} "
                    f"(ID: {saved_course.id}, 거리: {generation_response.course.distance:.2f}km)"
                )
                created_count += 1
                
            except Exception as e:
                logger.error(f"코스 생성/저장 중 오류 발생: {test_course['name']} - {e}", exc_info=True)
                await session.rollback()
                failed_count += 1
        
        logger.info(
            f"\n{'='*60}\n"
            f"데이터 삽입 완료\n"
            f"성공: {created_count}개\n"
            f"실패: {failed_count}개\n"
            f"{'='*60}"
        )


async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='테스트용 샘플 코스 데이터 삽입')
    parser.add_argument(
        '--clear',
        action='store_true',
        help='기존 데이터를 삭제하고 새로 삽입'
    )
    
    args = parser.parse_args()
    
    try:
        await seed_test_data(clear_existing=args.clear)
    except Exception as e:
        logger.error(f"스크립트 실행 중 오류 발생: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

