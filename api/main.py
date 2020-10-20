from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from auth import check_authentication_header
from core import pipeline, NoFaceException, MultiFaceException, EncodeException

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

allowed_extensions = ["jpg", "png", "jpeg"]


class Item(BaseModel):
    face_one: str
    face_two: str

    @validator("face_one", "face_two")
    def check_file_type(cls, v):
        try:
            meta, data = v.split(',')

        except ValueError:
            raise HTTPException(
                status_code=422,
                detail=f"Excepted base64",
            )

        if data == "":
            raise HTTPException(
                status_code=422,
                detail=f"Base64 Image Corrupt",
            )

        # meta can be -> data:image/png;base64
        img_type = meta.split("/")[-1].split(";")[0]

        if img_type not in allowed_extensions:
            raise HTTPException(
                status_code=422,
                detail=f"Please use images of file types in  {allowed_extensions}",
            )

        return v


class PredictResponse(BaseModel):
    FaceMatch: int
    Msg: str


@app.post("/faceMatch", response_model=PredictResponse)
async def main(input: Item,  key: Item = Depends(check_authentication_header)):
    try:
        face_match = pipeline(input.face_one, input.face_two)
    except MultiFaceException:
        return PredictResponse(FaceMatch=0,
                               Msg="MultiFace_ERR")
    except NoFaceException:
        return PredictResponse(FaceMatch=0,
                               Msg="NoFace_ERR")
    except EncodeException:
        return PredictResponse(FaceMatch=0,
                               Msg="Encode_ERR")
    except Exception as e:
        return PredictResponse(FaceMatch=0,
                               Msg="FAILED")
    else:
        return PredictResponse(FaceMatch=face_match,
                               Msg="SUCCESS")
