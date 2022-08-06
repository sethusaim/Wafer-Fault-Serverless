from shutil import rmtree

from s3_operations import S3_Operation

from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class Main_Utils:
    """
    Description :   This class is used for main utility functions required in core functions of the service
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3 = S3_Operation()

        self.log_writer = App_Logger()

        self.config = read_params()

        self.dir = self.config["dir"]

        self.log_dir = self.config["dir"]["log"]

        self.file_format = self.config["model_save_format"]

        self.feats_pattern = self.config["feature_pattern"]

    def upload_logs(self):
        """
        Method Name :   upload_logs
        Description :   This method uploads the logs to s3 bucket
        
        Output      :   The logs are uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_logs.__name__, __file__, "upload"
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3.upload_folder(self.log_dir, "logs", log_dic["log_file"])

            self.log_writer.log(f"Uploaded logs to logs s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            self.log_writer.stop_log()

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_model_file(self, key, model_name, log_file):
        """
        Method Name :   get_model_file
        Description :   This method get the model file name from s3 bucket 
        
        Output      :   The model file is retrived from s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_model_file.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            model_file = self.dir[key] + "/" + model_name + self.file_format

            self.log_writer.log(f"Got model file for {key}", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return model_file

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def create_prod_and_stag_dirs(self, bucket, log_file):
        """
        Method Name :   create_prod_and_stag_dirs
        Description :   This method creates folders for production and staging bucket

        Output      :   Folders for production and staging are created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.create_prod_and_stag_dirs.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3.create_folder("prod_model", bucket, log_dic["log_file"])

            self.s3.create_folder("stag_model", bucket, log_dic["log_file"])

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_number_of_clusters(self, log_file):
        """
        Method Name :   get_number_of_cluster
        Description :   This method gets the number of clusters based on training data on which clustering algorithm was used

        Output      :   The number of clusters for the given training data is returned
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_number_of_clusters.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            feat_fnames = self.s3.get_files_from_folder(
                self.feats_pattern, "feature_store", log_dic["log_file"], pattern=True
            )

            self.log_writer.log(
                f"Got features file names from feature store bucket based on feature pattern",
                **log_dic,
            )

            num_clusters = len(feat_fnames)

            self.log_writer.log(
                f"Got the number of clusters as {num_clusters}", **log_dic
            )

            self.log_writer.start_log("exit", **log_dic)

            return num_clusters

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
