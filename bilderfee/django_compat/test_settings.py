SECRET_KEY = '123'

BILDERFEE_TOKEN = 'BF_TOKEN'
BILDERFEE_LAZY_LOADING = False
BILDERFEE_MAX_SIZE = 2500
BILDERFEE_FALLBACK = '/fallback.jpg'
BILDERFEE_BASE_URL = 'https://my.bilder-fee.de'

STATIC_URL = 'http://my-hp.de'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
INSTALLED_APPS = [
    "bilderfee.django_compat"
]
MIDDLEWARE = []
ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', []),
            ],
            'context_processors': [
                'bilderfee.django_compat.context_processors.bilderfee_ctx'
            ],
        },
    },
]
