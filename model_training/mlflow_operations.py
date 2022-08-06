from datetime import datetime
from os import environ

from mlflow import log_metric, log_param, set_experiment, set_tracking_uri
from mlflow.sklearn import log_model

from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class MLFlow_Operation:
    """
    Description :    This class shall be used for handling all the mlflow operations
    Version     :   1.2

    Revisions   :   Moved to setup to cloud
    """

    def __init__(self, log_file):
        self.config = read_params()

        self.log_writer = App_Logger()

        self.log_file = log_file

        self.mlflow_config = self.config["mlflow_config"]

        self.current_date = f"{datetime.now().strftime('%Y-%m-%d')}"

    def set_mlflow_experiment(self, exp_name):
        """
        Method Name :   set_mlflow_experiment
        Description :   This method sets the mlflow experiment with the particular experiment name

        Output      :   An experiment with experiment name will be created in mlflow server
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.set_mlflow_experiment.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            set_experiment(self.mlflow_config[exp_name])

            self.log_writer.log(
                f"Set mlflow experiment with name as {exp_name}", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def set_mlflow_tracking_uri(self):
        """
        Method Name :   set_mlflow_tracking_uri
        Description :   This method sets the mlflow tracking uri in mlflow server

        Output      :   MLFLow server will set the particular uri to communicate with code
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.set_mlflow_tracking_uri.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            set_tracking_uri(environ["MLFLOW_TRACKING_URI"])

            self.log_writer.log("Set mlflow tracking uri", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def log_sklearn_model(self, model, model_name):
        """
        Method Name :   log_sklearn_model
        Description :   This method logs the model to mlflow server

        Output      :   A model is logged to the mlflow server
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.log_sklearn_model.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            log_model(
                sk_model=model,
                serialization_format=self.mlflow_config["serialization_format"],
                registered_model_name=model_name,
                artifact_path=model_name,
            )

            self.log_writer.log(f"Logged {model_name} model in mlflow", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def log_model_metric(self, model_name, metric):
        """
        Method Name :   log_model_metric
        Description :   This method logs the model metric to mlflow server

        Output      :   A model metric is logged to mlflow server
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.log_model_metric.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            model_score_name = f"{model_name}-best_score"

            log_metric(model_score_name, metric)

            self.log_writer.log(f"{model_score_name} logged in mlflow", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def log_model_param(self, model, model_name, param):
        """
        Method Name :   log_model_param
        Description :   This method logs the model param to mlflow server

        Output      :   A model param is logged to mlflow server
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.log_model_param.__name__,
            __file__,
            self.log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            model_param_name = model_name + f"-{param}"

            log_param(model_param_name, model.__dict__[param])

            self.log_writer.log(f"{model_param_name} logged in mlflow", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def log_all_for_model(self, model, model_score, idx):
        """
        Method Name :   log_all_for_model
        Description :   This method logs model,model params and model score to mlflow server

        Output      :   Model,model parameters and model score are logged to mlflow server
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.log_all_for_model.__name__,
            __file__,
            self.log_file,
        )

        try:
            self.log_writer.start_log("start", **log_dic)

            base_model_name = model.__class__.__name__

            model_name = self.current_date + "-" + base_model_name + str(idx)

            self.log_writer.log(f"Got the model name as {base_model_name}", **log_dic)

            model_params_list = list(self.config["train_model"][base_model_name].keys())

            self.log_writer.log(
                f"Created a list of params based on {model_name}", **log_dic
            )

            [
                self.log_model_param(model, model_name, param)
                for param in model_params_list
            ]

            self.log_sklearn_model(model, model_name)

            self.log_model_metric(model_name, float(model_score))

            self.log_writer.log(
                f"Logged model,metrics and parameters for {model_name} to mlflow",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
