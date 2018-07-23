from IPython.core.display import display, HTML
import base64
from lending_club.facets.facets_overview.python.generic_feature_statistics_generator import \
    GenericFeatureStatisticsGenerator


def make_facet(df, name):
    """

    Args:
        df: Data frame to visualize with Google Facets
        name: The name of the data frame to use as a label in the visualization

    Returns:
        None and renders the Facet HTML in the output

    """
    gfsg = GenericFeatureStatisticsGenerator()
    proto = gfsg.ProtoFromDataFrames([{'name': name, 'table': df}])
    protostr = base64.b64encode(proto.SerializeToString()).decode("utf-8")

    HTML_TEMPLATE = """
    <link rel="import" href="/nbextensions/facets-dist/facets-jupyter.html" >
    <facets-overview id="elem"></facets-overview>
    <script>
      document.querySelector("#elem").protoInput = "{protostr}";
    </script>
        """

    html = HTML_TEMPLATE.format(protostr=protostr)
    #display(HTML(html))
    return html
