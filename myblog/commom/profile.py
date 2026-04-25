from pathlib import Path

class Profile:
    __image_path = None

    @staticmethod
    def get_image_path() -> Path:
        home_path = Path(__file__).parent.parent

        image_path = home_path.joinpath("data/images")
        if not image_path.exists():
            image_path.mkdir(parents=True, exist_ok=True)

        return image_path