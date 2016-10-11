import os
import mimetypes
import sys
import django
import requests
import logging
import json
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()
from fileApp import models

#Points to folder of documents used for demo
file_fixtures = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), r'fixtures\data')
TOP_DIRs = [file_fixtures]


PDF = {"pdf": "application/pdf"}
ODT = {"odt": "application/vnd.oasis.opendocument.text"}
ODS = {"ods": "application/vnd.oasis.opendocument.spreadsheet"}
ODP = {"odp": "application/vnd.oasis.opendocument.presentation"}
MSDOC = {"doc": "application/msword"}
MSDOCX = {"docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
EXCEL1 = {"xls": "application/vnd.ms-excel"}
EXCEL2 = {"xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
TEXT = {"txt": "text/plain"}
CSV = {"csv": "text/csv"}
PNG = {"png": "image/png"}
JPEG = {"jpg": "image/jpeg"}
TIFF = {"tiff": "image/tiff"}
DWG = {"dwg": "image/vnd.dwg"}
LYR = {"lyr": "application/octet-stream"}
MPK = {"mpk": "application/octet-stream"}
MXD = {"mxd": "application/octet-stream"}

FILE_TYPE_CHOICES = {
    "PDF": PDF,
    "OPEN OFFICE DOC": ODT,
    "OPEN OFFICE SHEET": ODS,
    "OPEN OFFICE PRESENTATION": ODP,
    "MS Word doc": MSDOC,
    "MS Word docx": MSDOCX,
    "TEXT": TEXT,
    "MS Excel xls": EXCEL1,
    "MS Excel xlsx": EXCEL2,
    "CSV Spreadsheet": CSV,
    "PNG Image": PNG,
    "JPEG Image": JPEG,
    "TIFF Image": TIFF,
    "AutoCad dwg": DWG,
    "ESRI Layer File": LYR,
    "ESRI Map Package": MPK,
    "ESRI Map Document": MXD
}

DOC_VIEWER_TYPES = ['docx', 'doc', 'txt']

TABLE_VIEWER_TYPES = ['xls', 'xlsx', 'ods']

IMAGE_VIEWER_TYPES = ['tiff', 'jpg', 'png']


def __init__(self):
    self.FILE_TYPE_CHOICES = FILE_TYPE_CHOICES
    self.TOP_DIRs = TOP_DIRs
    return


class Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def convert_size(in_bytes):
    mb = in_bytes / 1048576.0
    kb = in_bytes / 1024.0
    gb = in_bytes / 1073741824.0

    if kb <= 612.0:
        d = "{} kB".format(int(kb))
    elif gb >= 1.0:
        d = "{} GB".format(int(gb))
    else:
        d = "{} MB".format(int(mb))
    return d


def check_file_type(types, ext):
    try:
        for k, v in iter(types.items()):
            # solves bug where some file extensions are uppercase
            if ext.lower() in v:
                d = k
                return d

    except Exception as e:
        logging.error("Unable to locate fileType from the supplied variables")
        print(e)


class FileStoreBuilder:
    def __init__(self):
        self.top_dirs = TOP_DIRs
        pass

    def build_store(self):
        try:
            top_dirs = self.top_dirs
            for top_dir in top_dirs:
                for root, dirs, files in os.walk(top_dir):
                    for _file in files:
                        # solves bug where file extensions are uppercase
                        extension = _file.split(".")[-1].lower()
                        for mapping in iter(FILE_TYPE_CHOICES.values()):
                            # there is only one key for each mapping dict so testing
                            # if the extension is IN the dict as a value is good enough
                            if extension in mapping:
                                file_path = os.path.join(root, _file)
                                base_name = os.path.basename(file_path)
                                file_type = check_file_type(FILE_TYPE_CHOICES, extension)
                                mime = mimetypes.guess_type(file_path)[0]
                                if mime is None:
                                    mime = FILE_TYPE_CHOICES[file_type][extension]
                                    # print mime
                                size = convert_size(os.path.getsize(file_path))

                                filtered = models.FileModel.objects.filter(file_path=file_path)
                                if len(filtered) == 0:
                                    # File has not been added to the database
                                    new_obj = models.FileModel.objects.create(
                                            file_path=file_path,
                                            base_name=base_name,
                                            file_type=file_type,
                                            mime=mime,
                                            size=size
                                    )
                                    new_obj.save()

                                elif len(filtered) == 1:
                                    # The File Exists in the Database and will be updated
                                    _object = filtered[0]
                                    _object.base_name = base_name
                                    _object.file_type = file_type
                                    _object.mime = mime
                                    _object.size = size
                                    _object.save()

        except Exception as e:
            logging.warning(e)

        return

    def clean_store(self):
        """Remove paths that don't exist;
        Remove directories;
        remove paths that don't match with TOP_DIRs;"""
        def check_roots(in_path, roots):
            d = False
            for x in roots:
                d = d
                if in_path.startswith(x):
                    if os.path.exists(in_path):
                        if not os.path.isdir(in_path):
                            d = True
            return d

        try:
            file_paths = []
            for _file in models.FileModel.objects.all():
                path = _file.file_path
                if not check_roots(path, self.top_dirs):
                    _file.delete()

                else:
                    if path not in file_paths:
                        file_paths.append(path)
                    else:
                        raise Error("Duplicate file objects with path {}".format(path))
                        # TODO - if two files are the same path, merge their grid cell assignments
                        pass

        except Exception as e:
            print(e)


class GridCellBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build_store():
        # send query request to esri rest api
        login_params = {
            'f': 'json',
            'client_id': 'Yer7Ki5IEHLbDzqv',
            'client_secret': 'a6b5f07dbd6d4228a0cb334cdad8d575',
            'grant_type': 'client_credentials',
            'expiration': '1440',
        }

        token = requests.post('https://www.arcgis.com/sharing/rest/oauth2/token/',
                              params=login_params)
        access_token = token.json()['access_token']

        query_url = r'https://services1.arcgis.com/Apy6bpbM5OoW9DX4/arcgis/rest/services/MapGrid_StatePlane/FeatureServer/0/query'
        query_params = {
            'f': 'json',
            'token': access_token,
            'returnM': 'false',
            'returnZ': 'false',
            'returnDistinctValues': 'true',
            'returnGeometry': 'false',
            'outFields': 'GRID',
            'where': "Id LIKE '%'"
        }

        feature_service = requests.post(query_url, params=query_params)

        features = feature_service.json()['features']
        for feature in features:

            grid = feature['attributes']['GRID']
            name = '{}'.format(grid)
            try:
                filtered = models.GridCell.objects.filter(name=name)
                if len(filtered) == 0:
                    x = models.GridCell.objects.create(name=name)
                    x.save()
                else:
                    pass

            except Exception as e:
                logging.error("Error populating the Grid Model {}".format(name))
                print(e)


class AssignmentManager:
    def __init__(self):
        pass

    def clear(self, data):
        pass