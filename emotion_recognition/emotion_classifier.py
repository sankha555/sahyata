from fer import FER

import face_capture


def classify_face_emotion():
    """
    Classifies the emotion in the latest face captured
    :return: detected emotion, confidence of detection
    """
    image = None
    if image is not None:
        image = face_capture.get_snapshot()
        emo_detector = FER(mtcnn=True)

        return emo_detector.top_emotion(image)
    return None, None
