import numpy as np
import pickle
import pandas as pd
from azureml.core.workspace import Workspace
from azureml.core.experiment import Experiment
from azureml.train.automl import AutoMLConfig
import logging
from azureml.automl.core.forecasting_parameters import ForecastingParameters

class Runner:
    def __init__(self,train_df_path,date_var,hr_vars,freq,holiday_feature,target_var):
        self.df = pd.read_csv('train.csv')
        self.freq = freq
        self.target_var = target_var
        self.date_time_var = date_var
        self.df[date_var] = pd.to_datetime(self.df[date_var])
        self.hr_vars = hr_vars
        self.holiday = holiday_feature
        self.suggestion = {}
        for x in self.hr_vars:
            self.suggestion[x] = list(self.df[x].unique())
            
        self.job_cache={}

    def _get_suggestions(self):
        return self.suggestion

    def _create_job(self,config_list,test_df_path):
        self.config_list = config_list

        key_val = "_"
        for x in config_list:
            key_val = key_val+"_"+x[0]+"_"+str(x[1])
            
        
        
        print("Check if Key Exists in Job Cache")
        if key_val in self.job_cache.keys():
            
            return key_val
        
        else:
            #Perform Slicing
            final_df = self.df
            for x in config_list:
                final_df = final_df[final_df[x[0]]==x[1]]
            self.final_df = final_df
            path = key_val+".csv"
            final_df.to_csv(path)
            train_data = pd.read_csv(path)
            
            forecasting_parameters = ForecastingParameters(time_column_name=self.date_time_var, 
                                               forecast_horizon=50,
                                               country_or_region_for_holidays='US',
                                               
                                               freq=self.freq,
                                               target_lags='auto',
                                               target_rolling_window_size=10)
            
            automl_config = AutoMLConfig(task='forecasting',
                             primary_metric='normalized_root_mean_squared_error',
                             experiment_timeout_minutes=15,
                             enable_early_stopping=True,
                             training_data=train_data,
                             label_column_name=self.target_var,
                             n_cross_validations=5,
                             enable_ensembling=False,
                             verbosity=logging.INFO,
                             forecasting_parameters = forecasting_parameters)
            ws = Workspace.from_config()
            experiment = Experiment(ws, "local-Delta")
            local_run = experiment.submit(automl_config, show_output=True)
            print("Training Job Complete")
            best_run, fitted_model = local_run.get_output()
            print("Making Predictions")
            self.job_cache[key_val] = fitted_model
            print("Finish")
            return key_val

    def _predict(self,test_df_path,key_val):
        test_df = pd.read_csv(test_df_path)
        fitted_model = self.job_cache[key_val]
        print("Slicing Test Data")
        for x in self.config_list:
            test_df = test_df[test_df[x[0]]==x[1]]
        final_test_df = test_df
        test_path = key_val+"test_df"+".csv"
        final_test_df.to_csv(test_path)
        print("Test Data Slicing Finish")
        test_data = pd.read_csv(test_path)
        test_labels = test_data[self.config_list[0][0]].to_numpy()
        label_query = test_labels.copy().astype(np.float)
        print("Creating Query")
        label_query.fill(np.nan)
        fitted_model.quantiles = [0.05,0.5, 0.9,0.75]
        result=fitted_model.forecast_quantiles(test_data,label_query,ignore_data_errors=True)
        print("Finish")
        return result






            
            


