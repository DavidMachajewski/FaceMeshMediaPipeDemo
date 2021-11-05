from face_mesh import FaceMeshing
from args import Arguments


if __name__ == '__main__':
    args = Arguments().get_args()
    live_meshing = FaceMeshing(args).init_stream()