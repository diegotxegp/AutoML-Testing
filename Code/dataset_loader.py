import os
import pandas as pd

class DatasetLoader:
    """
    Class responsible for loading datasets based on their file type.
    """
    def load_dataset(self, filepath):
        """
        Loads the dataset based on its file extension.
        :param filepath: Path to the dataset file.
        :return: pandas DataFrame with the dataset content.
        """
        _, ext = os.path.splitext(filepath)
        
        if ext == '.csv':
            delimiter = self.detect_delimiter(filepath)
            return pd.read_csv(filepath , delimiter=delimiter)
        elif ext in ['.xls', '.xlsx']:
            return pd.read_excel(filepath)
        elif ext == '.ods':
            return pd.read_excel(filepath, engine='odf')
        elif ext == '.txt':
            return pd.read_csv(filepath, delimiter=',')
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
    def detect_delimiter(self, filepath):
        """
        Detects the delimiter used in a CSV file by checking the first few lines.
        :param filepath: Path to the CSV file.
        :return: The detected delimiter (either ',' or ';').
        """
        with open(filepath, 'r') as file:
            first_line = file.readline()
            # Count occurrences of different delimiters
            comma_count = first_line.count(',')
            semicolon_count = first_line.count(';')
            
            # Determine which delimiter is used
            if comma_count > semicolon_count:
                return ','
            elif semicolon_count > comma_count:
                return ';'
            else:
                raise ValueError("Could not determine the delimiter; counts are equal or both are zero.")