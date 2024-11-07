import os

class DirectoryExplorer:
    def __init__(self, base_directory):
        """
        Class responsible for traversing directories and finding _train and _test files iteratively.
        """
        self.base_directory = base_directory

    def find_datasets(self):
        """
        Generator function to iteratively yield pairs of _train and _test datasets.
        :yield: Tuple with train and test file paths.
        """
        # Walk through all directories and subdirectories
        for root, dirs, files in os.walk(self.base_directory):
            train_file = None
            test_file = None

            # Search for _train and _test files in the current directory
            for file in files:
                if '_train' in file:
                    train_file = os.path.join(root, file)
                elif '_test' in file:
                    test_file = os.path.join(root, file)
                
                # If both train and test files are found, yield their paths
                if train_file and test_file:
                    yield root, train_file, test_file
                    # Reset train and test to search for more pairs in the same or other directories
                    train_file = None
                    test_file = None