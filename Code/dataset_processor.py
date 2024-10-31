from ludwig.automl import auto_train

class DatasetProcessor:
    def __init__(self, train_data, test_data, target, classes_number):
        """
        Initialize the DatasetProcessor class.
        """
        self.train_data = train_data
        self.test_data = test_data
        self.target = target
        self.classes_number = classes_number
        self.model = None

    def auto_train(self, seed):
        """
        Apply Ludwig AutoML (auto_train) on the given train dataset.
        """

        if self.classes_number == 2:
            # Perform auto_train with Ludwig
            auto_train_results = auto_train(
                dataset=self.train_data,
                target=self.target,
                output_directory='results/',
                time_limit_s=7200, # Set a time limit for the AutoML process (in seconds)
                random_seed = seed,
                user_config={'trainer':{'validation_field':f"{self.target}", 'validation_metric': 'roc_auc'},
                             'hyperopt': {'goal': 'maximize', 'metric': 'roc_auc', 'output_feature': f"{self.target}"},
                             'preprocessing': {'missing_value_strategy':'drop_row'}}
            )
        elif self.classes_number in [3, 4]:
            # Perform auto_train with Ludwig
            auto_train_results = auto_train(
                dataset=self.train_data,
                target=self.target,
                output_directory='results/',
                time_limit_s=7200, # Set a time limit for the AutoML process (in seconds)
                random_seed = seed,
                user_config={'trainer':{'validation_field':f"{self.target}", 'validation_metric': 'accuracy'},
                             'hyperopt': {'goal': 'maximize', 'metric': 'accuracy', 'output_feature': f"{self.target}"},
                             'preprocessing': {'missing_value_strategy':'drop_row'}}
            )
        elif self.classes_number > 4:
            # Perform auto_train with Ludwig
            auto_train_results = auto_train(
                dataset=self.train_data,
                target=self.target,
                output_directory='results/',
                time_limit_s=7200, # Set a time limit for the AutoML process (in seconds)
                random_seed = seed,
                user_config={'trainer':{'validation_field':f"{self.target}", 'validation_metric': 'mean_squared_error'},
                             'hyperopt': {'goal': 'minimize', 'metric': 'root_mean_squared_error', 'output_feature': f"{self.target}"},
                             'preprocessing': {'missing_value_strategy':'drop_row'}}
            )
            
        
        self.model = auto_train_results.best_model

    def evaluate(self):
        """
        Evaluate the trained model on the test dataset.
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet. Call auto_train() first.")

        # Evaluate the model using Ludwig's evaluate method
        evaluation_results = self.model.evaluate(dataset=self.test_data, collect_predictions=True)
        
        return evaluation_results