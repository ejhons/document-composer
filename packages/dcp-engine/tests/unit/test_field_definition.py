from dcp_engine.language.syntax.fields import InputDefinition


def raise_error_for_undefined_data_type():
    InputDefinition(
        type = 'undefined',
        name = 'dummy'
    )