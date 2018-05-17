from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers import DirectoryHandler


def main():
    """Create and start a bokeh server with a series of applications.
    """
    # Declare the absolute path to the demo application.
    bokeh_demo = "./NMRDemo"
    test_vis = "./testvis"
    bokehtest = './bokehtest'

    # Declare the dictionary of applications to launch.
    apps = {
        '/bokehDemo': Application(DirectoryHandler(filename=bokeh_demo)),
        # '/testvis': Application(DirectoryHandler(filename=test_vis)),
        '/bokehtest': Application(DirectoryHandler(filename=bokehtest)),

    }

    # Instantiate the Bokeh server.
    # See more about this at the documentation:
    # https://bokeh.pydata.org/en/latest/docs/reference/server/server.html
    server = Server(
        # A mapping from URL paths to Application instances, or a
        # single Application to put at the root URL.
        applications=apps,
        # A list of hosts that can connect to the websocket.
        allow_websocket_origin=["localhost:8001"],
        # The address the server should listen on for HTTP requests.
        # (default: None)
        # address=None,
        # The port number the server should listen on for HTTP requests.
        # (default: 5006)
        # port=5006,
        # prefix='',
        # Any remaining keyword arguments will be passed as-is to BokehTornado.
    )
    server.start()
    server.io_loop.start()


if __name__ == "__main__":
    main()
