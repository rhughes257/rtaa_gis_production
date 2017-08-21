from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import GridCell, EngineeringAssignment, EngineeringFileModel
from .utils import function_definitions
import mimetypes
import os

engineering_discipline_choices = [
                ('MISC', 'Miscellaneous'),
                ('CIVIL', 'Civil'),
                ('ARCH', 'Architectural'),
                ('STRUCTURAL', 'Structural'),
                ('LANDSCAPING', 'Landscaping'),
                ('MECHANICAL(HVAC)', 'Mechanical (HVAC)'),
                ('PLUMBING', 'Plumbing'),
                ('ELECTRICAL', 'Electrical')
            ]
engineering_sheet_types = [
                ('DETAILS', 'Details'),
                ('PLAN', 'Plan'),
                ('TITLE', 'Title'),
                ('KEY', 'Key'),
                ('INDEX', 'Index'),
                ('ELEVATIONS', 'Elevations'),
                ('NOTES', 'Notes'),
                ('SECTIONS', 'Sections'),
                ('SYMBOLS', 'Symbols')
            ]


class FileTypes:
    """the type of files that we are interested in are defined here"""

    def __init__(self):
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

        self.FILE_TYPE_CHOICES = {
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

        self.DOC_VIEWER_TYPES = ['docx', 'doc', 'txt']

        self.TABLE_VIEWER_TYPES = ['xls', 'xlsx', 'ods']

        self.IMAGE_VIEWER_TYPES = ['tiff', 'jpg', 'png']

        self.engineering_discipline_choices = engineering_discipline_choices

        self.engineering_sheet_types = engineering_sheet_types

        return


class GridSerializer(serializers.ModelSerializer):

    class Meta:
        model = GridCell
        fields = ('name',)
        read_only_fields = ('name',)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class EngFileHyperLinkedRelatedField(serializers.HyperlinkedRelatedField):
    queryset = EngineeringFileModel.objects.all()
    view_name = 'engineeringfilemodel-detail'
    lookup_field = 'pk'
    many = True

    def display_value(self, instance):
        return instance.file_path


class GridPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    queryset = GridCell.objects.all()
    many = True
    pk_field = 'Name'

    def display_value(self, instance):
        return '%s' % instance.name


class EngineeringDisciplinesField(serializers.MultipleChoiceField):
    choices = engineering_discipline_choices
    allow_blank = True


class EngineeringSheetTypesField(serializers.MultipleChoiceField):
    choices = engineering_sheet_types
    allow_blank = True


class EngAssignmentSerializer(serializers.ModelSerializer):

    grid_cell = GridPrimaryKeyRelatedField()

    file = EngFileHyperLinkedRelatedField()

    class Meta:
        model = EngineeringAssignment
        fields = ('pk', 'grid_cell', 'file', 'base_name', 'comment', 'date_assigned')
        depth = 1
        read_only_fields = ('base_name', 'date_assigned')

    def create(self, validated_data):
        base_name = validated_data['file'].base_name
        return EngineeringAssignment.objects.create(base_name=base_name, **validated_data)

    def update(self, instance, validated_data):
        instance.grid_cell = validated_data.get('grid_cell', instance.grid_cell)
        instance.file = validated_data.get('file', instance.file)
        instance.base_name = os.path.basename(instance.file.file_path)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class EngSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngineeringFileModel
        fields = ('pk', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'sheet_title', 'sheet_type',
                  'project_title', 'project_description', 'project_date', 'sheet_description', 'vendor', 'discipline',
                  'airport', 'funding_type', 'grant_number', 'file_path')
        depth = 1
        read_only_fields = ('pk', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'mime')

    grid_cells = serializers.SerializerMethodField()

    sheet_type = EngineeringSheetTypesField

    discipline = EngineeringDisciplinesField

    @staticmethod
    def sys_atts(file_path):
        file_types = FileTypes()
        extension = file_path.split(".")[-1].lower()
        if os.path.exists(file_path):
            base_name = os.path.basename(file_path)
            file_type = function_definitions.check_file_type(file_types.FILE_TYPE_CHOICES, extension)
            size = function_definitions.convert_size(os.path.getsize(file_path))
            mime = None
            for mapping in iter(file_types.FILE_TYPE_CHOICES.values()):
                if extension in mapping:
                    mime = file_types.FILE_TYPE_CHOICES[file_type][extension]

            if mime is None:
                mime = mimetypes.guess_type(file_path)[0]
        else:
            base_name = file_path.split("\\")[-1]
            file_type = base_name.split(".")[-1]
            size = ''
            mime = ''

        return {
            "base_name": base_name,
            "file_type": file_type,
            "size": size,
            "mime": mime
        }

    @staticmethod
    def get_grid_cells(self):
        base_name = self.base_name
        file_path = self.file_path
        assigns = EngineeringAssignment.objects.filter(base_name=base_name)
        grids = []
        for entry in assigns:
            _file = entry.file
            path = _file.file_path
            if path == file_path:
                _grid = entry.grid_cell
                if _grid.name not in grids:
                    grids.append(_grid.name)
        grids.sort()
        cells = ", ".join(grids)
        return cells

    def create(self, validated_data):
        try:
            file_path = validated_data['file_path']

            atts_dict = self.sys_atts(file_path)

            base_name = atts_dict["base_name"]
            file_type = atts_dict["file_type"]
            size = atts_dict["size"]
            mime = atts_dict["mime"]

            validated_data["file_path"] = file_path
            validated_data["lower_file_path"] = file_path.lower()
            validated_data["base_name"] = base_name
            validated_data["file_type"] = file_type
            validated_data["size"] = size
            validated_data["mime"] = mime

            _file = EngineeringFileModel.objects.create(**validated_data)
            _file.save()
            return _file
        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        instance.file_path = validated_data.get('file_path', instance.file_path)
        instance.lower_file_path = instance.file_path.lower()

        instance.base_name = instance.base_name
        instance.file_type = instance.file_type
        instance.size = instance.size
        instance.mime = instance.mime

        instance.comment = validated_data.get('comment', instance.comment)

        # These variables are brought in from the Access Database of Tiffany
        instance.sheet_type = validated_data.get("sheet_type", instance.sheet_type)
        instance.project_title = validated_data.get("project_title", instance.project_title)
        instance.sheet_description = validated_data.get("sheet_description", instance.sheet_description)
        instance.sheet_title = validated_data.get("sheet_title", instance.sheet_title)
        instance.project_date = validated_data.get("project_date", instance.project_date)
        instance.vendor = validated_data.get("vendor", instance.vendor)
        instance.airport = validated_data.get("airport", instance.airport)
        instance.project_description = validated_data.get("project_description", instance.project_description)
        instance.funding_type = validated_data.get("funding_type", instance.funding_type)
        instance.grant_number = validated_data.get("grant_number", instance.grant_number)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance
