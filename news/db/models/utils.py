def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)

    return default_function
