from base64 import b64decode

from config import logger

def decode_b64(data: str):
    decoded_bytes = b64decode(data)
    decoded_text = decoded_bytes.decode('utf-8')
    logger.debug(decoded_text[:200] + "\n..." if len(decoded_text) > 200 else decoded_text)
    return decoded_text