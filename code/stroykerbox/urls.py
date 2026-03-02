from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page

from rest_framework.authtoken import views
from filebrowser.sites import site
from constance import config
from stroykerbox.apps.catalog.views import CatalogFrontpageView, yml_export
from stroykerbox.apps.seo.views import robots_txt
from stroykerbox.apps.catalog import sitemap as catalog_sitemap
from stroykerbox.apps.staticpages import sitemap as staticpages_sitemap
from stroykerbox.apps.articles import sitemap as articles_sitemap
from stroykerbox.apps.news import sitemap as news_sitemap
from stroykerbox.apps.addresses.views import ContactsPageView
from stroykerbox.apps.utils.views import clear_cache, clear_thumbnail_cache
from stroykerbox.apps.search.views import SearchResult
from stroykerbox.apps.common.views import StaffCheckPage, DashboardPage

YML_URL = getattr(config, 'YML_URL', 'catalog_export.yml') or 'catalog_export.yml'

sitemaps = {
    'news': news_sitemap.NewsSitemap,
    'article': articles_sitemap.ArticleSitemap,
    'category': catalog_sitemap.CategorySitemap,
    'category_filter': catalog_sitemap.CategoryFilterSitemap,
    'product': catalog_sitemap.ProductSitemap,
    'staticpage': staticpages_sitemap.PageSitemap,
}

admin.site.site_header = config.ADMIN_SITE_HEADER
admin.site.site_title = config.ADMIN_SITE_META_TITLE

urlpatterns = [
    re_path(r'^$', CatalogFrontpageView.as_view(), name='frontpage'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('admin/clear-cache/', clear_cache, name='clear_cache'),
    path(
        'admin/clear-thumbnail-cache/',
        clear_thumbnail_cache,
        name='clear_thumbnail_cache',
    ),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('catalog/', include('stroykerbox.apps.catalog.urls', namespace='catalog')),
    path('cart/', include('stroykerbox.apps.commerce.cart_urls', namespace='cart')),
    path('news/', include('stroykerbox.apps.news.urls', namespace='news')),
    path('crm/', include('stroykerbox.apps.crm.urls', namespace='crm')),
    path('articles/', include('stroykerbox.apps.articles.urls', namespace='articles')),
    path('user/', include('stroykerbox.apps.users.urls', namespace='users')),
    path('account/', include('stroykerbox.apps.users.auth_urls')),
    path('bnrs/', include('stroykerbox.apps.banners.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('stroykerbox.apps.api.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path(
        'sitemap.xml',
        cache_page(60 * 60 * 6)(sitemap),
        {'sitemaps': sitemaps},  # noqa
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path(
        'subscription/',
        include('stroykerbox.apps.subscription.urls', namespace='subscription'),
    ),
    path('geoip/', include('django_geoip.urls')),
    path('location/', include('stroykerbox.apps.locations.urls')),
    path('addresses/', include('stroykerbox.apps.addresses.urls')),
    path('contacts/', ContactsPageView.as_view(), name='contacts-page'),
    path('reviews/', include('stroykerbox.apps.reviews.urls')),
    path('customization/', include('stroykerbox.apps.customization.urls')),
    path('custom_forms/', include('stroykerbox.apps.custom_forms.urls')),
    path('search', SearchResult.as_view(), name='search'),
    path(YML_URL, yml_export, name='yml_export'),
    path('faq/', include('stroykerbox.apps.faq.urls')),
    path('fp/', include('django_drf_filepond.urls')),
    path('content-check/', StaffCheckPage.as_view(), name='staff-check-page'),
    path('dash/', DashboardPage.as_view(), name='dashboard'),
]

if 'stroykerbox.apps.portfolio' in settings.INSTALLED_APPS:
    urlpatterns += [path('portfolio/', include('stroykerbox.apps.portfolio.urls'))]

if 'stroykerbox.apps.smartlombard' in settings.INSTALLED_APPS:
    from stroykerbox.apps.smartlombard.views import (
        online_payment as smartlombard_online_payment,
    )

    urlpatterns += [
        path(
            'online-oplata/',
            smartlombard_online_payment,
            name='smartlombard-online-payment',
        ),
        path(
            'smartlombard/tbank/', include('stroykerbox.apps.smartlombard.tbank.urls')
        ),
        path('smartlombard/', include('stroykerbox.apps.smartlombard.urls')),
    ]

if 'stroykerbox.apps.booking' in settings.INSTALLED_APPS:
    urlpatterns += [path('booking/', include('stroykerbox.apps.booking.urls'))]

if settings.DEBUG or settings.TESTING_MODE:
    try:
        import debug_toolbar
    except (ImportError, ModuleNotFoundError):
        pass
    else:
        urlpatterns = (
            [
                path('__debug__/', include(debug_toolbar.urls)),
            ]
            + urlpatterns
            + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        )


# Static pages. This must always be the last URL rule!
urlpatterns += [
    path('', include('stroykerbox.apps.staticpages.urls', namespace='staticpages'))
]


def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_dict = self._build_app_dict(request, app_label)
    ordering = getattr(settings, 'APPS_ORDER', {})

    app_list = sorted(
        app_dict.values(),
        key=lambda x: ordering.get(x['app_label'].lower(), f'z{x["name"]}'),
    )

    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    return app_list


admin.AdminSite.get_app_list = get_app_list
