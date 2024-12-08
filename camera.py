import cv2


class Camera:
    """
    A class to handle video capture from a camera.
    """

    def __init__(self, url: str | int = 0) -> None:
        """
        Initialize the camera.

        :param camera_index: Index of the camera to use.
        """
        self.cap = cv2.VideoCapture(url)

    def get_frame(self) -> bytes:
        ret, frame = self.cap.read()
        cv2.imshow("img", frame)
        if not ret:
            return b""

        ret, jpeg = cv2.imencode(".jpg", frame)
        if not ret:
            return b""

        return jpeg.tobytes()

    def release(self) -> None:
        """
        Release the camera resource.
        """
        if self.cap.isOpened():
            self.cap.release()


if __name__ == "__main__":
    camera = Camera()

    while True:
        camera.get_frame()

        if cv2.waitKey(1) & 0xFF == ord("q"):  # 1 is the time in ms
            break

    camera.release()
    cv2.destroyAllWindows()
