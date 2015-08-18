import pyblish.api

@pyblish.api.log
class ValidateVersionWorkfile(pyblish.api.Validator):
    """Validates whether workFile is versioned and makes sure that version number of write nodes matches version of the
    work file
    """

    families = ['workFile']
    version = (0, 1, 0)
    label = 'File versioned'

    def process(self, context):
gh
        assert context.has_data('version'), 'Your workfile is not versioned!'
