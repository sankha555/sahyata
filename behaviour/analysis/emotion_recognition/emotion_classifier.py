from fer import FER

from syslogs import logs


def classify_face_emotion(image):
    """
    Classifies the emotion in the latest face captured
    :return: detected emotion, confidence of detection
    """

    if image is None:
        logs.print_log("No images captured yet!", "debug")
        return None, None

    try:
        emo_detector = FER(mtcnn=True)

        return emo_detector.top_emotion(image)
    except Exception as e:
        logs.print_log(e, "error")
        return None, None
