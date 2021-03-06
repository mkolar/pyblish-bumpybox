import hou
import pyblish.api


@pyblish.api.log
class SelectFlipbookNodes(pyblish.api.Selector):
    """Selects all flipbook nodes"""

    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, context):

        renderNode = hou.node("/out")
        render_nodes = renderNode.children()

        for node in list(render_nodes):

            if 'flipbook' in node.type().name():
                instance = context.create_instance(name=node.name())
                instance.set_data('family', value='review')

                instance.add(node)
                instance.data["families"] = ['review']

                output = instance[0].parm('outputV').eval()

                # ftrack data
                components = {'review': {'path': output,
                                         'reviewable': True,
                                          }}
                instance.set_data('ftrackComponents', value=components)

                # instance.set_data('ftrackAssetName', value='quicktime')
                # instance.set_data('ftrackAssetType', value='mov')
