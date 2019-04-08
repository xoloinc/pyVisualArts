import os
class getPaths:
    def get_image_paths(input_dir='.'):
        paths = []
        for root, dirs, files in os.walk(input_dir, topdown=True):
            for file in sorted(files):
                if file.endswith(('jpg', 'png', 'gif','mp4')):
                    path = os.path.abspath(os.path.join(root, file))
                    paths.append(path)
        return paths