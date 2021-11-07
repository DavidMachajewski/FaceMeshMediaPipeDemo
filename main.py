from face_mesh import FaceMeshing
from args import Arguments

if __name__ == '__main__':
    args = Arguments().get_args()
    live_meshing = FaceMeshing(args)
    live_meshing.init_stream()
    # print(type(live_meshing.landmarks))
    print(live_meshing.get_landmarks_list())
