# FaceComparison

export API_AUTH_KEY="enter your api key here"

```
uvicorn api:app --reload
```

facematch API

```
/faceMatch


input
 {
     "face_one":"base64",
     "face_two":"base64"
}
```