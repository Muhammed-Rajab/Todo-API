"""
    A package to verify image file integrity
        : Checks format of image and convert it to jpg
        : Checks it's maximum size (4MB)
        : Checks it's resolution
        : Checks whether it is broken or not
        : Manages file saving (asynchrnously)
        : Sets default image as profile if no image is passed
"""

from io import BytesIO
import random
import string
from typing import Union
from PIL import Image
from app.core.config import settings



class ProfilePictureHandler:
    def __init__(self, file: Union[bytes, None]) -> None:

        self.saved_file_name = "default.png"
        
        if file == None: return

        self.file = file

        try:
            self.im = Image.open(BytesIO(self.file))
        except:
            return

        if len(self.file) > settings.PROFILE_PICTURE_FILESIZE:
            return
        
        if self.im.format == 'PNG':
            self.saved_file_name = self.save()
    
    def _generate_random_file_name(self) -> str:
        return ''.join(
                        random.choices(
                            string.ascii_uppercase +
                            string.digits, 
                            k = settings.PROFILE_PICTURE_FILENAME_LENGTH))
    
    def save(self) -> str:
        file_name = self._generate_random_file_name()
        file_path = f"{settings.BASE_PATH}/{settings.PROFILEPICTURES_DIR}/{file_name}"+".png"
        with open(file_path, "wb") as file:
            file.write(self.file)
        return file_name+".png"