from os import listdir, remove
from os.path import join

from boto3 import client, resource
from botocore.exceptions import ClientError

from utils.logger import App_Logger
from utils.read_params import get_log_dic, read_params


class S3_Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Version     :   1.2
    
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.log_writer = App_Logger()

        self.config = read_params()

        self.s3_client = client("s3")

        self.s3_resource = resource("s3")

        self.bucket = self.config["s3_bucket"]

        self.dir = self.config["dir"]

    def create_folder(self, folder_name, bucket, log_file):
        """
        Method Name :   create_folder
        Description :   This method creates a folder in s3 bucket
        
        Output      :   A folder is created in s3 bucket 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.create_folder.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.s3_resource.Object(self.bucket[bucket], self.dir[folder_name]).load()

            self.log_writer.log(f"Folder {folder_name} already exists.", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.log_writer.log(
                    f"{folder_name} folder does not exist,creating new one", **log_dic
                )

                self.s3_client.put_object(
                    Bucket=self.bucket[bucket], Key=(self.dir[folder_name] + "/")
                )

                self.log_writer.log(
                    f"{folder_name} folder created in {bucket} bucket", **log_dic
                )

            else:
                self.log_writer.log(
                    f"Error occured in creating {folder_name} folder", **log_dic
                )

                self.log_writer.exception_log(e, **log_dic)

    def copy_data(self, from_fname, from_bucket, to_fname, to_bucket, log_file):
        """
        Method Name :   copy_data
        Description :   This method copies the data from one bucket to another bucket
        
        Output      :   The data is copied from one bucket to another
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.copy_data.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            copy_source = {"Bucket": self.bucket[from_bucket], "Key": from_fname}

            self.s3_resource.meta.client.copy(
                copy_source, self.bucket[to_bucket], to_fname
            )

            self.log_writer.log(
                f"Copied data from bucket {from_bucket} to bucket {to_bucket}",
                **log_dic,
            )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_file(self, from_fname, to_fname, bucket, log_file, delete=True):
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs

        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_file.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            self.log_writer.log(
                f"Uploading {from_fname} to s3 bucket {bucket}", **log_dic
            )

            self.s3_resource.meta.client.upload_file(
                from_fname, self.bucket[bucket], to_fname
            )

            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {bucket}", **log_dic
            )

            if delete is True:
                self.log_writer.log(
                    f"Option remove is set {delete}..deleting the file", **log_dic
                )

                remove(from_fname)

                self.log_writer.log(
                    f"Removed the local copy of {from_fname}", **log_dic
                )

            else:
                self.log_writer.log(
                    f"Option remove is set {delete}, not deleting the file", **log_dic
                )

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_bucket(self, bucket, log_file):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 
        
        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_bucket.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            bucket = self.s3_resource.Bucket(self.bucket[bucket])

            self.log_writer.log(f"Got {bucket} bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return bucket

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_file_object(self, fname, bucket, log_file, pattern=False):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket
        
        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__, self.get_file_object.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            bucket = self.get_bucket(bucket, log_file)

            if pattern is False:
                lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            else:
                lst_objs = [
                    object for object in bucket.objects.all() if fname in object.key
                ]

            self.log_writer.log(f"Got {fname} from bucket {bucket}", **log_dic)

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.start_log("exit", **log_dic)

            return file_objs

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def get_files_from_folder(self, folder_name, bucket, log_file, pattern=False):
        """
        Method Name :   get_files_from_folder
        Description :   This method gets the files a folder in s3 bucket
        
        Output      :   A list of files is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        log_dic = get_log_dic(
            self.__class__.__name__,
            self.get_files_from_folder.__name__,
            __file__,
            log_file,
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = self.get_file_object(folder_name, bucket, log_file, pattern=pattern)

            list_of_files = [object.key for object in lst]

            self.log_writer.log(f"Got list of files from bucket {bucket}", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

            return list_of_files

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)

    def upload_folder(self, folder, bucket, log_file):
        log_dic = get_log_dic(
            self.__class__.__name__, self.upload_folder.__name__, __file__, log_file
        )

        self.log_writer.start_log("start", **log_dic)

        try:
            lst = listdir(folder)

            self.log_writer.log("Got a list of files from folder", **log_dic)

            for f in lst:
                local_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(local_f, dest_f, bucket, log_file, delete=False)

            self.log_writer.log("Uploaded folder to s3 bucket", **log_dic)

            self.log_writer.start_log("exit", **log_dic)

        except Exception as e:
            self.log_writer.exception_log(e, **log_dic)
