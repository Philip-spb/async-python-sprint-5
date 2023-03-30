from models.general import PersonalFile as PersonalFileModel
from schemas.personal_file import PersonalFileCreate, PersonalFileUpdate
from services.base import RepositoryDB


class RepositoryPersonalFile(
    RepositoryDB[
        PersonalFileModel,
        PersonalFileCreate,
        PersonalFileUpdate]
):
    pass


personal_file_crud = RepositoryPersonalFile(PersonalFileModel)
