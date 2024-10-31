import pandas as pd

class StatisticsCalculator:
    def __init__(self):
        self.df = pd.DataFrame()  # Initialize an empty DataFrame

    def add_results(self, results, seed):
        """Add a new result as a row to the DataFrame."""        
        # If new_dict is a tuple, extract the first element
        if isinstance(results, tuple):
            new_dict = results[0]
        
            # Assume the first element of the dictionary is another dictionary
            first_key = next(iter(new_dict))
            
            # Extract the dictionary associated with the first key
            results_to_add = new_dict[first_key]

            # Add the seed at the begining of the dictionary
            new_new_dict = {'seed': seed}
            new_new_dict.update(results_to_add)
            results_to_add = new_new_dict
            
            # Convert the dictionary to a DataFrame with a single row
            new_row = pd.DataFrame(results_to_add, index=[0])
            
            # Concatenate the new row to the existing DataFrame
            self.df = pd.concat([self.df, new_row], ignore_index=True)
        
            print(self.df)

        else:
            raise ValueError("Results is no a tuple.")
    
    def dataframe_with_stats(self):
        """Return the DataFrame with the statistics."""
        
        # Check if the DataFrame is empty
        if self.df.empty:
            raise ValueError("No data available to calculate statistics.")
        
        # Calculate statistics for the DataFrame: mean, variance, and standard deviation
        stats = {
            'mean': self.df.mean(),         # Compute the mean for each column
            'variance': self.df.var(),      # Compute the variance for each column
            'std_dev': self.df.std(),       # Compute the standard deviation for each column
        }
        
        # Create a new DataFrame from the statistics dictionary
        stats_df = pd.DataFrame(stats)
        
        # Concatenate the original DataFrame with the statistics DataFrame
        # The transpose (T) is used to align the stats with the original DataFrame's structure
        result_df = pd.concat([self.df, stats_df.T], ignore_index=True)
        
        # Return the combined DataFrame containing original data and calculated statistics
        return result_df