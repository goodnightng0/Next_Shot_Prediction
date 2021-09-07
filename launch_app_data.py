"""## Load dataset in FiftyOne

FiftyOne is designed to make it as easy as possible to [load and visualize your image and video datasets](https://voxel51.com/docs/fiftyone/user_guide/dataset_creation/index.html) even with complex label types like detections and segmentations.
"""

def start_app_session():
    import fiftyone as fo

    name = "next-shot-subset"
    dataset_dir = "./videos/train"

    # Create the dataset
    dataset = fo.Dataset.from_dir(
        dataset_dir, fo.types.VideoClassificationDirectoryTree, name=name
    )

    # Launch the App and view the dataset we loaded
    # Hover over or click on the samples to play the videos.
    session = fo.launch_app(dataset)

    session.freeze()