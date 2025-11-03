"""
Database models split by entity.

Each file contains ONE model class following Single Responsibility Principle.
Models use the Repository Pattern from database.base.repository.
"""

from .category import CategoryModel
from .organization import OrganizationModel
from .person import PersonModel
from .person_organization import PersonOrganizationModel
from .compensation import CompensationModel
from .contact_info import ContactInfoModel
from .social_media import SocialMediaModel
from .data_source import DataSourceModel

__all__ = [
    'CategoryModel',
    'OrganizationModel',
    'PersonModel',
    'PersonOrganizationModel',
    'CompensationModel',
    'ContactInfoModel',
    'SocialMediaModel',
    'DataSourceModel',
]
