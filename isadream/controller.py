

class Controller:

    def __init__(self):
        pass

    @staticmethod
    def build_frames(nodes, **kwargs):
        frames = [node.build_frames(**kwargs)
                  for node in self.nodes]
        return filter(None, frames)

    @staticmethod
    def combine_frames(frames):
        pass
