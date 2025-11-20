"""
Custom storage backends for AWS S3
"""
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    """Storage for public media files (recipe images, user uploads)"""
    location = 'media'
    file_overwrite = False
