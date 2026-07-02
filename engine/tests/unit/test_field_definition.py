
from engine.src.doc_engine.models.models import FieldDefinition

def raise_error_for_undefined_data_type():
    FieldDefinition(
        data_type = 'undefined',
        label = 'dummy'
    )