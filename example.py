import asyncio
import random
from PIL import Image
from numpy import asarray
import httpx
from qqddm import AnimeConverter, InvalidQQDDMApiResponseException, IllegalPictureQQDDMApiResponseException

PROXYFORMAT = ['http://user:pass@ip:port']
USERAGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"


def imagecrop(namefile: str):
    image = Image.open(namefile).convert('RGB')
    x = asarray(image)
    lens1 = len(x)
    lens = len(x[0])
    if lens > lens1:
        image = image.crop((0, 0, lens, lens1 - 177))
    else:
        image = image.crop((0, 0, lens, lens1 - 185))
    image.save(namefile)
    return f'{namefile}'


async def get_pic_using_api(picture_filename, PROXY):
    PROXY = random.choice(PROXY)
    if picture_filename.startswith("http"):
        async with httpx.AsyncClient(headers={"User-Agent": USERAGENT}) as client:
            r = await client.get(url=picture_filename)
        r.raise_for_status()
        picture_bytes = r.content
    else:
        with open(picture_filename, "rb") as f:
            picture_bytes = f.read()

    # Initialize the AnimeConverter class. Optional settings can be used for customizing the requesting behaviour.
    converter = AnimeConverter(
        global_useragents=[USERAGENT],
        generate_proxy=PROXY,
    )

    # Result is returned as an `AnimeResult` object
    try:
        result = await converter.convert(picture_bytes)
    except IllegalPictureQQDDMApiResponseException:
        # The API may forbid converting images with sensible content
        print("The image provided is forbidden, try with another picture")
        return 0
    except InvalidQQDDMApiResponseException as ex:
        # If the API returned any other error, show the response body
        print(f"API returned error ({ex}); response body: {ex.response_body}")
        return 1
    except Exception as _EX:
        print(f'API returned {_EX} exception. check it up!')
        return 2


    pic = await converter.download_one(result.pictures_urls[0])
    with open(picture_filename, 'wb') as file:
        file.write(pic)
    naming = imagecrop(picture_filename)
    return naming


if __name__ == '__main__':
    asyncio.run(get_pic_using_api('1.jpg', ["http://"]))
