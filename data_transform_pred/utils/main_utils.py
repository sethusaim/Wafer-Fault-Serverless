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

        self.log_dir = self.config["dir"]["log"]

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

            self.log_writer.log(f"Uploaded logs to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            self.log_writer.stop_log()

            rmtree(self.log_dir)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
