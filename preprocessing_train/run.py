from data_loader_train import Data_Getter_Train
from preprocessing import Preprocessor
from utils.logger import App_Logger
from utils.main_utils import Main_Utils
from utils.read_params import get_log_dic


class Run:
    """
    Description :   This class is used for running the data transformation prediction pipeline
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.utils = Main_Utils()

        self.preprocessor = Preprocessor("preprocess")

        self.data_getter_train = Data_Getter_Train("preprocess")

        self.log_writer = App_Logger()

    def run_preprocess(self):
        """
        Method Name :   run_preprocess
        Description :   This method applies the preprocessing functions on the training data 
        
        Output      :   The preprocessing functions is applied on training data and artifacts are stored in s3 buckets
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.run_preprocess.__name__,
            __file__,
            "preprocess",
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            data = self.data_getter_train.get_data()

            data = self.preprocessor.remove_columns(data, ["Wafer"])

            X, Y = self.preprocessor.separate_label_feature(data)

            is_null_present = self.preprocessor.is_null_present(X)

            if is_null_present:
                X = self.preprocessor.impute_missing_values(X)

            cols_to_drop = self.preprocessor.get_columns_with_zero_std_deviation(X)

            X = self.preprocessor.remove_columns(X, cols_to_drop)

            Y = self.preprocessor.encode_target_col(Y)

            self.utils.upload_data_to_feature_store(
                X, "wafer_features", log_dic["log_file"]
            )

            self.utils.upload_data_to_feature_store(
                Y, "wafer_targets", log_dic["log_file"]
            )

            self.log_writer.log("Completed preprocessing on training data", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)


if __name__ == "__main__":
    try:
        run = Run()

        run.run_preprocess()

    except Exception as e:
        raise e

    finally:
        utils = Main_Utils()

        utils.upload_logs()
