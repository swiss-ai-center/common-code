import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from common_code.service.models import services


router = APIRouter()


@router.get("/status", summary="Get service availability")
async def get_availability():
    return JSONResponse(status_code=200, content={"status": "Service is available"})


@router.get(
    "/health_check/",
    summary="Tests the service",
    responses={
        200: {"detail": "Tests failed"},
        204: {"detail": "Tests passed"},
        500: {"detail": "Internal Server error"},
    },
    status_code=204,
    tags=["Service"],
)
async def health_check():
    my_service = services[0]()
    loop = asyncio.get_event_loop()
    test_result_future = loop.run_in_executor(None, my_service.main_test)
    test_result_list = await test_result_future
    if not test_result_list["tests_passed"]:
        raise HTTPException(status_code=200, detail=test_result_list["results"])


@router.get(
    "/download_test_data/",
    summary="Download test data",
    responses={
        200: {"detail": "Test data downloaded"},
        500: {"detail": "Internal Server error"},
        404: {"detail": "Data not found"},
    },
    status_code=200,
    tags=["Service"],
)
async def download_test_data():
    my_service = services[0]()
    return my_service.download_test_data()
