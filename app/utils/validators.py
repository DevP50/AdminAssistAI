from config import BaseConfig
def is_allowed_excel_file(filename):
    if "." not in filename:
        return False
    extension = filename.rsplit(".",1)[1]
    print(extension)
    extension = extension.lower()
    print(extension)
    return extension in BaseConfig.ALLOWED_EXTENSIONS
# BUG: is_allowed_excel_file retourne False pour data.xlsx, vérifier ALLOWED_EXTENSIONS
#Verified and the issue is that the ALLOWED_EXTENSIONS is a set of strings with a leading dot (e.g., ".xlsx"), while the extension extracted from the filename does not include the dot. Therefore, the comparison fails. To fix this, you should modify the function to include the dot when checking against ALLOWED_EXTENSIONS.