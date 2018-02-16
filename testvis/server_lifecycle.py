import shutil
import os


def on_server_loaded(server_context):
    ''' If present, this function is called when the server first starts. '''
    pass

def on_server_unloaded(server_context):
    ''' If present, this function is called when the server shuts down. '''
    pass

def on_session_created(session_context):
    ''' If present, this function is called when a session is created.
    '''
    pass

def on_session_destroyed(session_context):
    ''' If present, this function is called when a session is closed. '''
    # Try to read the filepath.
    try:
        # Get the filepath of the generated json files for this vis instance.
        args = session_context.request.arguments
        filepath = args.get('J')[0].decode("utf-8")
        filepath = os.path.join('data', filepath)
        # # Remove the folder and all its contents.
        shutil.rmtree(filepath)
        print(f'I REMOVED THE FOLDER {filepath} AND ALL ITS CONTENTS.')

    except:
        # TODO: Use better form on this exception. At least throw or log
        # the error that occurs.
        pass
