from task.utils.selector.phantomjs_selector import PhantomJSSelector
from task.utils.selector.request_selector import RequestsSelector


def new_handler(name, debug=False):
    if name == 'request':
        return RequestsSelector(debug)
    elif name == 'phantomjs':
        return PhantomJSSelector(debug)
    else:
        raise Exception()
