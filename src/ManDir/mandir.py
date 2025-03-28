# Author : Shashank Kanna
import os
import pickle
import csv
from datetime import datetime
import cv2
from loguru import logger

class NoContentGiven(Exception):
    """Custom exception raised when a no content passed to save."""
    def __init__(self, message="No Data Given to write"):
        self.message = message
        super().__init__(self.message)

class DataInvalidError(Exception):
    """Custom exception raised when a content passed to save is invalid."""
    def __init__(self, message="Content Invalid"):
        self.message = message
        super().__init__(self.message)

class ManDir:
    def __init__(self, folder_path: str, limit: int = 15) -> None:
        """
        Initializes a directory management object.
        Creates the folder if it doesn't exist. Raises an exception if it already exists.

        Args:
            folder_path (str): Path to the folder.
            limit (int): Maximum number of files allowed in the folder.
        Return:
            None
        """
        self.folder_path = folder_path
        self.limit: int = limit
        if os.path.exists(folder_path):
            logger.info(f"{folder_path} already exists.")
            pass
        else:
            os.makedirs(folder_path)
            logger.info(f"Created {folder_path}.")

    def save(self, save_with_time: bool = True, txtfile: list[str] = None, picklefile: list[str] =None, csvfile: list[str]=None, imgfile: list[str] = None) -> None:
        """
        Saves a file in the folder with data and extension in index-0, index-1 in list passed respectively. Deletes oldest files if folder exceeds the limit.

        Args:
            save_with_time (bool) = True: Stores the given data in file name given along with time stamp. 

            !! All args below are list of len 2 with index-0 having content to save and index-1 with file name ["Make sure file name is uniques when save_with_time is False"]] !!
            txtfile (list) = None: 
            picklefile (list) = None: 
            csvfile (list) = None:
            imgfile (list) = None:
        Return:
            None
        """
        if save_with_time:
            _neram = datetime.now().strftime("%Y_%m_%d_at_%_I_%M_%S_%p")
        else:
            _neram = ""
        _flag = True

        # Check files in the folder
        files = sorted(
            [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)],
            key=os.path.getctime
        )

        # Remove oldest files if the folder exceeds the limit
        if len(files) >= self.limit:
            logger.info("Folder overflow.")
        while len(files) >= self.limit:
            oldest_file = files.pop(0)
            os.remove(oldest_file)
            logger.info(f"{oldest_file} removed.")

        if txtfile is not None:
            if not isinstance(txtfile, list):
                logger.error("Provided save data invalid.")
                raise DataInvalidError
            if len(txtfile) < 2:
                logger.error("Provided save data invalid.")
                raise DataInvalidError

            name = _neram + txtfile[1]
            loc = os.path.join(self.folder_path, name)
            with open(loc, "w") as f:
                f.write(txtfile[0])
            logger.success(f"TXT file {loc} saved.")
            _flag = False

        if picklefile is not None:
            if not isinstance(picklefile, list):
                logger.error("Provided save data invalid.")
                raise DataInvalidError
            if len(picklefile) < 2:
                logger.error("Provided save data invalid.")
                raise DataInvalidError
                
            name = _neram + picklefile[1]
            loc = os.path.join(self.folder_path, name)
            with open(loc, "wb") as f:
                pickle.dump(picklefile[0], f)
            logger.success(f"Pickle file {loc} saved.")
            _flag = False

        def is_nested_list(obj):
            return isinstance(obj, list) and any(isinstance(item, list) for item in obj)
        
        if csvfile is not None:
            if not isinstance(csvfile, list):
                logger.error("Provided save data invalid.")
                raise DataInvalidError
            
            if len(csvfile) < 2:
                logger.error("Provided save data invalid.")
                raise DataInvalidError
            
            if not is_nested_list(csvfile[0]):
                logger.error("Provided save data invalid.")
                raise DataInvalidError
            
            name = _neram + csvfile[1]
            loc = os.path.join(self.folder_path, name)
            with open(loc, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(csvfile[0])
            logger.success(f"CSV file {loc} saved.")
            _flag = False

        if imgfile is not None:
            if not isinstance(imgfile, list):
                logger.error("Provided save data invalid.")
                raise DataInvalidError
            if len(imgfile) < 2:
                logger.error("Provided save data invalid.")
                raise DataInvalidError
                
            name = _neram + imgfile[1]
            loc = os.path.join(self.folder_path, name)
            try:
                cv2.imwrite(loc, imgfile[0])
            except Exception as e:
                logger.critical(f"External error{e}")
            
            logger.success(f"Image file {loc} saved.")
            _flag = False

        if _flag:
            logger.error("No content given to save")
            raise NoContentGiven
