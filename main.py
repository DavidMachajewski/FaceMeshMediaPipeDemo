from face_mesh import FaceMeshing
from args import Arguments

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = Arguments().get_args()
    live_meshing = FaceMeshing(args).init_stream()