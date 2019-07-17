# Django

## Installation & Configuration
```bash
pip install bilderfee-py
```

Register bilderfee in your APP settings

```python
INSTALLED_APPS = [
    # ...
    'bilderfee.django_compat',
    # ... 
]
```

Add your TOKEN AND BASE_URL
```python
BILDERFEE_TOKEN = 'YOUR_BF_TOKEN'
BILDERFERR_BASE_URL = 'YOU_BF_URL'

```

Change lazy-loading behaviour
```python
BILDERFEE_LAZY_LOADING = True
```

Change default behaviour when there is no image
```python
BILDERFEE_FALLBACK = '/media/my-default-image.jpg'
```

Register TEMPLATE TAGS

```python
TEMPLATES = [
    {
        'BACKEND': '...',
        'DIRS': [
            # ...
        ],
        'OPTIONS': {
            'loaders': '...',
            'context_processors': [
                # ...
                'bilderfee.django_compat.context_processors.bilderfee_ctx',
                # ...
            ],
        },
    },
]

```

### In Template
Load Templatetags to have access.

```djangotemplate
{% load bilderfee %}
```

#### bf_src tag
Use the `img_src`-tag to have low-level access to the Image-Url.
```djangotemplate
{% bf_src "/IMG-URL" "400x500" %}
{# or #}
{% bf_src article.image.url "400x500" %}
{# will resolves to #}
https://f1.bilder-fee.de/YOUR_BF_TOKEN/width:400,height:500/IMG-URL

{# More accurate example is when you are using css-style-background #}
<div style="background-image: url('{% img_src article.image.url "400x500" %}')" >
{# will resolves to #}
<div style="background-image: url('https://f1.bilder-fee.de/YOUR_BF_TOKEN/width:400,height:500/IMG-URL')" >
```

#### bf_img tag

*Usage*: 
```djangotemplate
{% bf_image "/IMG-URL" "400x500" lazy=False %}
{# will resolves to this: !!! I is replacement for the full resolved Image-URL #}
<img src="I"/>
```


To enable lazy-loading use `lazy=True`
```djangotemplate
{% bf_image "/IMG-URL" "400x500" class="my-additional-class" alt="my alt attribute" custom-attr="my-custom" %}
{# will resolves to this: !!! I is replacement for the full resolved Image-URL #}
<img 
    class="my-additional-class bf-lazy" 
    alt="my alt attribute"
    custom-attr="my-custom"
    data-src="I"/>

```

#### bf_picture tag
The picture tag leverages the latest browser technology and let the browser decide which formats to choose from.  

*Usage*:

````djangotemplate
{% bf_picture "/IMG" "400x500" id="ID" alt="ALT" %}
{# will resolves to this: !!! I is replacement for the full resolved Image-URL #}
<picture>
    <!-- browser wich supports webp, will take this -->
    <source type="image/webp" srcset="I@webp 1x, I@2x.webp 2x">
    
    <!-- Browser which suports srcset will use it Retina image. -->
    <!-- Legacy Browser uses the src to display image -->
    <img class=" bf-lazy" id="ID" alt="ALT" src="I" srcset="I 1x, I@2x 2x">
</picture>

````

#### lazy-loading support
This lib comes with a handy image-tag with lazy-loading support.

Lazy-Loading support uses the popular and lightweight https://github.com/verlok/lazyload.

It loads images when it becomes visible instead of load all image on the page at once on current browser.
On old browser, it loads all images at once.

Lazy-Loading is disabled by default, you can pass `lazy=True` to the template tags `bf_image`, `bf_picture` to enable it.

To enable lazy-loading, you site needs to include our `bf-lazy-loading.js` and initialize it.
We help you with our handy template-tag `{% bf_static_init %}`.
Make sure this comes before you `</body>`.


#### Full example
```djangotemplate
{% load bilderfee %}
<html>
    <head>
        <!-- Uses bf_image to render OpenGraph image content with the prefered sizes. -->
        <meta property="og:image" content="{% bf_image article.image.url "1500x1500" crop=True %}" />
    </head>
    <body>
    
    <a href="/link-to-article">
        {% bf_img article.image.url "1000x800" crop=True lazy=True %}
    </a>
    
    <a href="/link-to-article">
        {% bf_picture article.image.url "1000x800" crop=True lazy=True %}
    </a>
    
    {% bf_static_init %}
    </body>
</html>

```


## Available Options

See available options at https://developer.bilder-fee.de/#Options

## Tests

```bash
pytest --cov .

# Html report
pytest --cov-report html

```
