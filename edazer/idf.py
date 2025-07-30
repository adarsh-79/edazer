
def interactive_df(activate: bool= True, maxsize: str= "1MB"):
    """
    Activates interactive dataframe by enabling itables in the notebook.

    Parameters:
        activate (bool): Whether to activate interactive mode.
        maxsize (str or int): Maximum size of the DataFrames (in bytes like '1MB') for interactively displaying all of it without downsizing.
    """
    from itables import show, init_notebook_mode
    import itables.options as opt
    
    if activate:
        opt.maxBytes = maxsize
        
        # Setting PyCharm-like styling and behavior    
        opt.classes = "display compact cell-border stripe hover"
        opt.lengthMenu = [5, 10, 25, 50, 100]
        opt.pageLength = 10
        opt.scrollX = True
        opt.columnDefs = [{"className": "dt-center", "targets": "_all"}]        
    
    #enables itables
    init_notebook_mode(all_interactive= activate)


        


