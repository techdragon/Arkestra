from django.conf import settings
from importlib import import_module


class BaseNavigator(object):
    pass


class NavigationPool(object):
    """
    Contains the set of adjusters that can provide Arkestra with hints about the widths (or other attributes) of placeholders and their contents
    """
    def __init__(self):
        self.navigators = {}
        self.discovered = False

    def discover_modifers(self):
        """
        Looks for navigator that need to be registered
        """
        # if we have already looped over applications, then we have already
        # discovered all navigators
        if self.discovered:
            return

        for app in settings.INSTALLED_APPS:
            try:
                i = import_module("%s.integration" % app)
                print "dir(i)", dir(i)
                print i.Navigator
                i.register()
            except ImportError:
                pass
        self.discovered = True

    def register_navigator(self, navigator_class):
        print "registering", navigator_class
        assert issubclass(navigator_class, BaseNavigator)
        print "  it's a Navigator"
        # should we check if it's already registered?
        self.navigators.setdefault(
            navigator_class.kind, []
            ).append(navigator_class)
        print "registered navigators", self.navigators

navigation_pool = NavigationPool()
navigation_pool.discover_modifers()