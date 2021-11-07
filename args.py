import argparse


class Arguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def get_args(self):
        self.parser.add_argument("--fx", default=1.2, help="Scale webcam window x")
        self.parser.add_argument("--fy", default=1.2, help="Scale webcam window y")
        self.parser.add_argument("--segmentation", default=1, help="Enable background segmentation.")
        self.parser.add_argument("--meshing", default=1, help="Draw the facial mesh.")
        return self.parser.parse_args()
