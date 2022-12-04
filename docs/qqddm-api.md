# QQ's API spec

## a. Request body

```json
{
  "busiId": "ai_painting_anime_entry",
  "images": [
    "<base64>"
  ],
  "extra": "{\"face_rects\":[],\"version\":2,\"platform\":\"web\",\"data_report\":{\"parent_trace_id\":\"d5c3492b-037b-8dab-34bd-c1d7c85daef2\",\"root_channel\":\"\",\"level\":1}}"
}
```

### a.1. `extra` field (JSON string)

`extra` is not required, but changing the `extra.version` may produce different image results.

### a.2. curl command

```bash
curl 'https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: es,en-US;q=0.7,en;q=0.3' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://h5.tu.qq.com/' -H 'Content-Type: application/json' -H 'Origin: https://h5.tu.qq.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' --data-raw '{"busiId":"ai_painting_anime_entry","images":["<base64>"],"extra":"{\"face_rects\":[],\"version\":2,\"platform\":\"web\",\"data_report\":{\"parent_trace_id\":\"67abd766-8e57-4299-9464-f6e67b90be59\",\"root_channel\":\"\",\"level\":1}}"}'
```

## b. Response body

```json
{
  "code": 0,
  "msg": "",
  "images": [],
  "faces": [],
  "extra": "{\"video_urls\": [\"https://act-artifacts.shadowcv.qq.com/mqq/ai_painting_anime/video/e218cde0accb9b079814c49e91e7c98b_poqay.mp4\", \"https://activity.tu.qq.com/mqq/ai_painting_anime/share/e218cde0accb9b079814c49e91e7c98b_ms4wq.mp4\"], \"img_urls\": [\"https://activity.tu.qq.com/mqq/ai_painting_anime/image/e218cde0accb9b079814c49e91e7c98b_8tvrw.jpg\", \"https://activity.tu.qq.com/mqq/ai_painting_anime/share/e218cde0accb9b079814c49e91e7c98b_yayhn.jpg\", \"https://act-artifacts.shadowcv.qq.com/mqq/ai_painting_anime/res/e218cde0accb9b079814c49e91e7c98b_rpkpt.jpg\", \"https://activity.tu.qq.com/mqq/ai_painting_anime/pagres/e218cde0accb9b079814c49e91e7c98b_b4soo.jpg\"]}",
  "videos": []
}
```

### b.1. `extra` field (JSON string)

This field is a JSON string that contains the resulting images.

```json
{
  "video_urls": [
    "https://act-artifacts.shadowcv.qq.com/mqq/ai_painting_anime/video/e218cde0accb9b079814c49e91e7c98b_poqay.mp4",
    "https://activity.tu.qq.com/mqq/ai_painting_anime/share/e218cde0accb9b079814c49e91e7c98b_ms4wq.mp4"
  ],
  "img_urls": [
    "https://activity.tu.qq.com/mqq/ai_painting_anime/image/e218cde0accb9b079814c49e91e7c98b_8tvrw.jpg",
    "https://activity.tu.qq.com/mqq/ai_painting_anime/share/e218cde0accb9b079814c49e91e7c98b_yayhn.jpg",
    "https://act-artifacts.shadowcv.qq.com/mqq/ai_painting_anime/res/e218cde0accb9b079814c49e91e7c98b_rpkpt.jpg",
    "https://activity.tu.qq.com/mqq/ai_painting_anime/pagres/e218cde0accb9b079814c49e91e7c98b_b4soo.jpg"
  ]
}
```

The returned array of `img_urls` depends on whether the image is vertical or horizontal, and on the `extra.version` specified on the request body.

#### b.1.i. `img_urls` results (vertical)

This is returned when request `extra.version` is not specified or set to `1`; or when set to `2` and the given image is vertical.

1. Vertical with original on bottom-right (png despite the file extension, 720x1280, [Pic example](group1-pic1.png))
2. Two-side vertical comparison (jpg, 1000x930, [Pic example](group1-pic2.jpg))
3. Vertical resulting picture only (jpg, 830x1400, [Pic example](group1-pic3.jpg))
4. Like 1 but (jpg, 720x1462, [Pic example](group1-pic4.jpg))

#### b.1.ii. `img_urls` results (horizontal)

This is returned when request `extra.version = 2` and the given image is horizontal.

1. Two-side horizontal comparison, hard to crop (png despite the file extension, 720x1280, [Pic example](group2-pic1.png))
2. Two-side horizontal comparison, easier to crop than 1 (jpg, 800x1257, [Pic example](group2-pic2.jpg))
3. Horizontal resulting picture only (jpg, 1120x940, [Pic example](group2-pic3.jpg))
4. Like 1 but (jpg, 720x1462, [Pic example](group2-pic4.jpg))

#### b.1.iii. Other result

The API may return the following result, but it's uncommon. Here, the same picture is always returned. Unknown conditions.

```json
{
    "img_urls": [
        "https://activity.tu.qq.com/mqq/ai_painting_anime/share/d8e01394-7283-11ed-9ab0-525400e59797.jpg",
        "https://activity.tu.qq.com/mqq/ai_painting_anime/share/d8e01394-7283-11ed-9ab0-525400e59797.jpg",
        "https://activity.tu.qq.com/mqq/ai_painting_anime/share/d8e01394-7283-11ed-9ab0-525400e59797.jpg",
        "https://activity.tu.qq.com/mqq/ai_painting_anime/share/d8e01394-7283-11ed-9ab0-525400e59797.jpg"
    ],
    "uuid": "d8e01394-7283-11ed-9ab0-525400e59797"
}
```

[Pic example](group3-pic1.jpg)

## b.2. Errors

Response always returns 200. When conversion fails, response only includes `code` and `msg`, where `code != 0`.

Example response body of a failed request:

```json
{
  "code": 2114,
  "msg": "IMG_ILLEGAL"
}
```

### b.2.i. Identified errors

| `code`  | `msg`           | Description                                                                                         |
|---------|-----------------|-----------------------------------------------------------------------------------------------------|
| `2114`  | `IMG_ILLEGAL`   | Not allowed picture (nude, violence, political...)                                                  |
| `2111`  | `VOLUMN_LIMIT`  | Possibly rate limit or image too big (retrying may return successfuly after some retries)           |
| `-2100` | `PARAM_INVALID` | Possibly invalid file or image format (gif, webp and other uncommon formats seem to be unsupported) |