import json
import os

_default_context = {
    "SMARTY": {
        "auth_id": "f2f1da81-1fe1-9922-ed66-5c5384c16f33",
        "auth_token": "WncHuDYo3WFRhLPvmS3V"
    }
}

def get_context(context_name):
    result = os.environ.get(context_name, None)

    if result is not None:
        try:
            tmp = json.loads(result)
            result = tmp
        except json.JSONDecoderError as je:
            pass
    else:
        result = _default_context[context_name]

    return result