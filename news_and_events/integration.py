from arkestra_utilities.navigation_pool import BaseNavigator, navigation_pool

class Navigator(BaseNavigator):
    """docstring for ContactsAndPeopleNavigator"""
    kind="news_and_events"
    menu_dict = {
        "auto_page_attribute": "auto_news_page",
        "title_attribute": "news_page_menu_title",
        "url_attribute": "news-and-events",
        "sub_menus": False,

        "lister_module": "news_and_events.lister",
        "lister_name": "NewsAndEventsMenuLister",
        }

def register():
    navigation_pool.register_navigator(Navigator)
