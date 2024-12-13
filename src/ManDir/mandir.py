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
    def __init__(self, folder_path, limit=15):
        """
        Initializes a directory management object.
        Creates the folder if it doesn't exist. Raises an exception if it already exists.

        Args:
            folder_path (str): Path to the folder.
            limit (int): Maximum number of files allowed in the folder.
        """
        self.folder_path = folder_path
        self.limit = limit
        if os.path.exists(folder_path):
            logger.info(f"{folder_path} already exists.")
            pass
        else:
            os.makedirs(folder_path)
            logger.info(f"Created {folder_path}.")

    def save(self, txtfile: list[str] = None, picklefile: list[str] =None, csvfile: list[str]=None, imgfile: list[str] = None):
        """
        Saves a file in the folder with data and extension. Deletes oldest files if folder exceeds the limit.

        Args:
            txtfile (list): 
            picklefile (list): 
            csvfile (list): 
        """

        _neram = datetime.now().strftime("%Y-%m-%d_at_%-I.%M.%S_%p")
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
            logger.info(f"TXT file {loc} saved.")
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
            logger.info(f"Pickle file {loc} saved.")
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
            logger.info(f"CSV file {loc} saved.")
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
            
            logger.info(f"Image file {loc} saved.")
            _flag = False

        if _flag:
            logger.error("No content given to save")
            raise NoContentGiven
