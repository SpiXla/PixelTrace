from PIL import Image

# python3 main.py -m sample_images/image-example-full.jpeg
# Exiftool: https://exiftool.org/

EXIF_IFD_TAG = 0x8769
GPS_INFO_TAG = 0x8825
DATE_TIME_ORIGINAL_TAG = 0x9003
DATE_TIME_DIGITIZED_TAG = 0x9004
DATE_TIME_TAG = 0x0132
MAKE_TAG = 0x010F
MODEL_TAG = 0x0110
SOFTWARE_TAG = 0x0131
NOT_FOUND = "Not found"


def extract_metadata(image_path: str) -> str:
    with Image.open(image_path) as image:
        exif_data = image.getexif()
        width, height = image.size
        latitude, longitude, latitude_ref, longitude_ref = extract_coordinates(exif_data)
        device = extract_device(exif_data)
        capture_date = extract_capture_date(exif_data)
        software = extract_software(exif_data)

        if not latitude or not longitude:
            latitude = longitude = latitude_ref = longitude_ref = NOT_FOUND
        else:
            latitude = f"{latitude} {latitude_ref}"
            longitude = f"{longitude} {longitude_ref}"

        result = (
            f"Latitude: {latitude}\n"
            f"Longitude: {longitude}\n"
            f"Resolution: {width}x{height}\n"
            f"Device: {device}\n"
            f"Software: {software}\n"
            f"Date: {capture_date}"
        )
        return result

def extract_coordinates(exif_data) -> tuple[float | None, float | None]:
    if not exif_data:
        return None, None, None, None

    gps_info = exif_data.get_ifd(GPS_INFO_TAG)
    if not gps_info:
        return None, None, None, None

    latitude = gps_info.get(2)
    latitude_ref = gps_info.get(1)
    longitude = gps_info.get(4)
    longitude_ref = gps_info.get(3)

    if not latitude or not latitude_ref or not longitude or not longitude_ref:
        return None, None, None, None


    return latitude, longitude, latitude_ref, longitude_ref


def extract_device(exif_data) -> str:
    if not exif_data:
        return NOT_FOUND

    make = clean_exif_string(exif_data.get(MAKE_TAG))
    model = clean_exif_string(exif_data.get(MODEL_TAG))

    if make and model:
        return f"{make} {model}"

    if model:
        return model

    if make:
        return make

    return NOT_FOUND


def extract_software(exif_data) -> str:
    if not exif_data:
        return NOT_FOUND

    software = clean_exif_string(exif_data.get(SOFTWARE_TAG))
    return software if software else NOT_FOUND

def extract_capture_date(exif_data) -> str:
    if not exif_data:
        return NOT_FOUND

    exif_ifd = exif_data.get_ifd(EXIF_IFD_TAG)
    capture_date = ""

    if exif_ifd:
        capture_date = clean_exif_string(exif_ifd.get(DATE_TIME_ORIGINAL_TAG))
        if not capture_date:
            capture_date = clean_exif_string(exif_ifd.get(DATE_TIME_DIGITIZED_TAG))

    if not capture_date:
        capture_date = clean_exif_string(exif_data.get(DATE_TIME_TAG))

    if not capture_date:
        return NOT_FOUND

    return normalize_exif_date(capture_date)


def clean_exif_string(value) -> str:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="ignore")

    if value is None:
        return ""

    return str(value).strip()


def normalize_exif_date(value: str) -> str:
    return value.replace(":", "-", 2)
