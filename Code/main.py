import os
import pandas as pd
import random
import sys

from directory_explorer import DirectoryExplorer
from dataset_loader import DatasetLoader
from dataset_processor import DatasetProcessor
from statistics_calculator import StatisticsCalculator

class MainApp:
    def __init__(self, base_directory, reps, stats_file, seeds):
        """
        Main class responsible for managing the application.
        """
        self.base_directory = base_directory
        self.directory_explorer = DirectoryExplorer(base_directory)
        self.dataset_loader = DatasetLoader()
        self.dataset_processor = None
        self.statistics_calculator = None
        self.reps = reps
        self.stats_file = stats_file
        self.seeds = seeds

    def write_to_csv(self, df, file_name):
        with open(file_name, 'a') as f:
            f.write("")
            df.to_csv(f, mode="a",sep=";", header=True, index=True, encoding='utf-8')
        df.to_csv(file_name, mode="a",sep=";", header=True, index=True, encoding='utf-8')

    def random_number_generator(self):
        random_number = random.randint(1, 1000000)
        return random_number

    def run(self):
        """
        Main method that loads and processes the datasets.
        """
        # Shell output
        with open('shell_output.txt', 'w') as out:
            sys.stdout = out
            sys.stderr = out

            if os.path.exists(self.stats_file):
                    # Remove file if it exists
                    os.remove(f"{self.stats_file}")

            # Load and process datasets
            for directory_path, train_file, test_file in self.directory_explorer.find_datasets():
                train_data = self.dataset_loader.load_dataset(train_file)
                test_data = self.dataset_loader.load_dataset(test_file)
                
                # Perform your ML tasks here
                print("----------------------------------------------------------------------------------------------------")
                print(f"Directory: {directory_path}")
                print(f"Train data: {train_data.shape}")
                print(f"Test data: {test_data.shape}")
                print("----------------------------------------------------------------------------------------------------")

                # Initialize the DatasetProcessor class
                columns = train_data.columns.tolist()
                target = columns[-1]
                
                classes_number = len(train_data[target].unique())

                self.dataset_processor = DatasetProcessor(train_data, test_data, target, classes_number)
                self.statistics_calculator = StatisticsCalculator()
                
                for seed in self.seeds:
                    #seed = self.random_number_generator()
                    self.dataset_processor.auto_train(seed)
                    evaluation_results = self.dataset_processor.evaluate()
                    self.statistics_calculator.add_results(evaluation_results, seed)

                df_stats = pd.DataFrame()
                df_stats = self.statistics_calculator.dataframe_with_stats()

                with open(self.stats_file, 'a') as f:
                    f.write(f"Directory: {directory_path}")
                    f.write("\n")
                    df_stats.to_csv(f, mode="a",sep=",", header=True, index=False, encoding='utf-8')
                    f.write("\n")

                print("----------------------------------------------------------------------------------------------------")
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

# Usage
if __name__ == '__main__':
    base_directory = '/home/diegotxe/Visual-Studio/HAMELIN/Datasets' # <------- Replace with your base directory
    reps = 20 # <------- Number of repetitions for each dataset
    stats_file = "stats.csv" # <------- Name of output file with results
    seeds = [744186, 569605, 317850, 317280, 309735, 261288, 795218, 783451, 84707, 12143, 911610, 335832, 563564, 478409, 498050, 457776, 713220, 487820, 540677, 839543]
    manager = MainApp(base_directory, reps, stats_file, seeds)
    manager.run()