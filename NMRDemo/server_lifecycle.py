def on_server_loaded(server_context):
    ''' If present, this function is called when the server first starts. '''
    print('on_server_loaded')

def on_server_unloaded(server_context):
    ''' If present, this function is called when the server shuts down. '''
    print('on_server_unloaded')

def on_session_created(session_context):
    ''' If present, this function is called when a session is created.
    '''
    print('on_session_created')

def on_session_destroyed(session_context):
    ''' If present, this function is called when a session is closed. '''

    print('on_session_destroyed')
    # Violating good import practice.
    # import shutil
    #
    # # Get the filepath of the generated json files for this vis instance.
    # args = session_context.request.arguments
    #
    # # Try to read the filepath.
    # try:
    #     filepath = args.get('J')[0]
    #
    #     # Remove the folder and all its contents.
    #     shutil.rmtree(filepath)
    #
    # except:
    #     # TODO: Use better form on this exception. At least throw or log
    #     # the error that occurs.
    #     pass
