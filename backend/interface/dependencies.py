"""
Dependency Injection

FastAPI 의존성 주입 설정입니다.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.session import get_db
from infrastructure.database.repositories.course_repository import CourseRepositoryImpl
from infrastructure.database.repositories.running_session_repository import RunningSessionRepositoryImpl
from domain.repositories.course_repository import CourseRepository
from domain.repositories.running_session_repository import RunningSessionRepository
from domain.services.loop_generator import LoopGenerator
from application.use_cases.generate_course import GenerateCourseUseCase
from application.use_cases.save_course import SaveCourseUseCase
from application.use_cases.list_courses import ListCoursesUseCase
from application.use_cases.get_course import GetCourseUseCase
from application.use_cases.delete_course import DeleteCourseUseCase
from application.use_cases.start_running import StartRunningUseCase
from application.use_cases.update_running import UpdateRunningUseCase
from application.use_cases.update_location import UpdateLocationUseCase
from application.use_cases.finish_running import FinishRunningUseCase


# 데이터베이스 세션 의존성
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


# Repository 의존성
def get_course_repository(db: DatabaseSession) -> CourseRepository:
    """CourseRepository 의존성"""
    return CourseRepositoryImpl(db)


def get_running_session_repository(db: DatabaseSession) -> RunningSessionRepository:
    """RunningSessionRepository 의존성"""
    return RunningSessionRepositoryImpl(db)


CourseRepositoryDep = Annotated[CourseRepository, Depends(get_course_repository)]
RunningSessionRepositoryDep = Annotated[
    RunningSessionRepository, Depends(get_running_session_repository)
]


# LoopGenerator 의존성 (현재는 Mock 사용, 향후 실제 구현체로 교체)
def get_loop_generator() -> LoopGenerator:
    """
    LoopGenerator 의존성
    
    현재는 Mock 구현체를 반환합니다.
    향후 DistanceConstrainedLoopGenerator 구현 시 교체 필요.
    """
    from interface.mock_loop_generator import MockLoopGenerator
    
    return MockLoopGenerator()


LoopGeneratorDep = Annotated[LoopGenerator, Depends(get_loop_generator)]


# Use Case 의존성
def get_generate_course_use_case(
    loop_generator: LoopGeneratorDep,
) -> GenerateCourseUseCase:
    """GenerateCourseUseCase 의존성"""
    return GenerateCourseUseCase(loop_generator=loop_generator)


def get_save_course_use_case(
    course_repository: CourseRepositoryDep,
) -> SaveCourseUseCase:
    """SaveCourseUseCase 의존성"""
    return SaveCourseUseCase(course_repository=course_repository)


def get_list_courses_use_case(
    course_repository: CourseRepositoryDep,
) -> ListCoursesUseCase:
    """ListCoursesUseCase 의존성"""
    return ListCoursesUseCase(course_repository=course_repository)


def get_get_course_use_case(
    course_repository: CourseRepositoryDep,
) -> GetCourseUseCase:
    """GetCourseUseCase 의존성"""
    return GetCourseUseCase(course_repository=course_repository)


def get_delete_course_use_case(
    course_repository: CourseRepositoryDep,
) -> DeleteCourseUseCase:
    """DeleteCourseUseCase 의존성"""
    return DeleteCourseUseCase(course_repository=course_repository)


def get_start_running_use_case(
    running_session_repository: RunningSessionRepositoryDep,
    course_repository: CourseRepositoryDep,
) -> StartRunningUseCase:
    """StartRunningUseCase 의존성"""
    return StartRunningUseCase(
        running_session_repository=running_session_repository,
        course_repository=course_repository,
    )


def get_update_running_use_case(
    running_session_repository: RunningSessionRepositoryDep,
) -> UpdateRunningUseCase:
    """UpdateRunningUseCase 의존성"""
    return UpdateRunningUseCase(running_session_repository=running_session_repository)


def get_update_location_use_case(
    running_session_repository: RunningSessionRepositoryDep,
) -> UpdateLocationUseCase:
    """UpdateLocationUseCase 의존성"""
    return UpdateLocationUseCase(running_session_repository=running_session_repository)


def get_finish_running_use_case(
    running_session_repository: RunningSessionRepositoryDep,
) -> FinishRunningUseCase:
    """FinishRunningUseCase 의존성"""
    return FinishRunningUseCase(running_session_repository=running_session_repository)


# Use Case 의존성 타입 별칭
GenerateCourseUseCaseDep = Annotated[
    GenerateCourseUseCase, Depends(get_generate_course_use_case)
]
SaveCourseUseCaseDep = Annotated[SaveCourseUseCase, Depends(get_save_course_use_case)]
ListCoursesUseCaseDep = Annotated[
    ListCoursesUseCase, Depends(get_list_courses_use_case)
]
GetCourseUseCaseDep = Annotated[GetCourseUseCase, Depends(get_get_course_use_case)]
DeleteCourseUseCaseDep = Annotated[
    DeleteCourseUseCase, Depends(get_delete_course_use_case)
]
StartRunningUseCaseDep = Annotated[
    StartRunningUseCase, Depends(get_start_running_use_case)
]
UpdateRunningUseCaseDep = Annotated[
    UpdateRunningUseCase, Depends(get_update_running_use_case)
]
UpdateLocationUseCaseDep = Annotated[
    UpdateLocationUseCase, Depends(get_update_location_use_case)
]
FinishRunningUseCaseDep = Annotated[
    FinishRunningUseCase, Depends(get_finish_running_use_case)
]

