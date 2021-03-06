import os
import pyblish
import pyblish.api
from ftrack_kredenc import ft_utils
reload(ft_utils)
from pyblish_kredenc.actions import actions_os


class RepairPublishPath(pyblish.api.Action):
    label = "Repair"
    on = "failed"
    icon = "wrench"

    def process(self, context):

        path = os.path.dirname(context['publishFile'])

        if not os.path.exists(path):
            os.makedirs(path)


@pyblish.api.log
class ValidatePublishPath(pyblish.api.InstancePlugin):
    """Validates that the publish directory for the workFile exists"""

    order = pyblish.api.ValidatorOrder - 0.1
    label = 'Validate Publish Path'
    families = ['scene']

    actions = [
        RepairPublishPath,
        actions_os.OpenOutputFolder,
        actions_os.OpenOutputFile
        ]

    def process(self, instance):

        version = instance.context.data['version']
        version = 'v' + str(version).zfill(3)
        taskid = instance.context.data('ftrackData')['Task']['id']

        ftrack_data = instance.context.data['ftrackData']

        templates = None

        if 'Asset_Build' in ftrack_data:
            templates = [
                'asset.publish.scene'
            ]
        elif 'Shot' in ftrack_data:
            templates = [
                'shot.publish.scene'
            ]


        assert templates, "Could not recognize entity"

        self.log.debug(templates)

        root = instance.context.data('ftrackData')['Project']['root']
        publishFiles = ft_utils.getPathsYaml(taskid,
                                                 templateList=templates,
                                                 version=version,
                                                 root=root)

        publishFile = publishFiles[0]

        instance.context.data['publishFile'] = publishFile
        instance.context.data['deadlineInput'] = publishFile
        instance.data['outputPath_publish'] = publishFile
        self.log.debug('Setting publishFile: {}'.format(publishFile))
