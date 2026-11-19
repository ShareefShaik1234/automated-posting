from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="Publishes a validated short message with a single CTA URL across 5 platforms concurrently.",
    version="1.0.0",
)

posting_service = PostingService()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation failed",
            "details": errors,
        },
    )


@app.post(
    "/posting",
    response_model=PostingResponse,
    status_code=status.HTTP_200_OK,
    summary="Publish message across multiple platforms",
)
async def create_posting(payload: PostingRequest) -> PostingResponse:
    return await posting_service.publish_all(payload.message)
