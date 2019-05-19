from django import template
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django.conf import settings

from bilderfee.bilderfee import url

LAZY_LOADING = getattr(settings, 'BILDERFEE_LAZY_LOADING', False)

register = template.Library()

SRC_ATTRS = {
    'gravity',
    'quality',
    'blur',
    'sharpen',
    'ext',
    'dpr',
    'background',
    'grayscale',
    'format',
    'dpr',
    'enlarge',
    'extend',
    'flip',
    'flop',
    'progressive',
    'fit',
    'crop',
}


@register.simple_tag
def bf_src(img, dim, **kwargs):
    width, height = dim.split('x')

    if settings.DEBUG is False and not hasattr(settings, 'BILDERFEE_TOKEN'):
        raise ImproperlyConfigured('Please configure BILDERFEE_TOKEN in your settings.')

    data = {
        'width': int(width),
        'height': int(height),
        'token': settings.BILDERFEE_TOKEN
    }
    data.update(**kwargs)

    return url(img, **data)


def get_img_src_args(kwargs):
    src_kwargs = {}
    img_attrs = {}
    for k, v in kwargs.items():
        if k in SRC_ATTRS:
            src_kwargs[k] = v
        else:
            img_attrs[k] = v
    return img_attrs, src_kwargs


@register.simple_tag
def bf_image(img, dim, lazy=None, **kwargs):
    lazy = LAZY_LOADING if lazy is None else lazy
    img_attrs, src_kwargs = get_img_src_args(kwargs)

    src = bf_src(img, dim, **src_kwargs)
    src_attr = 'src'
    if lazy:
        src_attr = 'data-src'
        cls = '{}{}'.format(img_attrs.get('class', ''), ' bf-lazy')
        img_attrs['class'] = cls

    img_attrs[src_attr] = src

    html = '<img {}/>'.format(' '.join('{}="{}"'.format(k, v) for k, v in img_attrs.items()))
    return mark_safe(html)


@register.simple_tag
def bf_picture(img, dim, lazy=None, **kwargs):
    lazy = LAZY_LOADING if lazy is None else lazy
    img_attrs, src_kwargs = get_img_src_args(kwargs)

    src = bf_src(img, dim, **src_kwargs)
    cls = '{}{}'.format(img_attrs.get('class', ''), ' bf-lazy')
    data_prefix = 'data-' if lazy else ''

    html = (
        '<picture>'
        '<source type="image/webp" {data_prefix}srcset="{src}@webp 1x, {src}@2x.webp 2x">'
        '<img class="{cls}" {attrs} {data_prefix}src="{src}" {data_prefix}srcset="{src} 1x, {src}@2x 2x">'
        '</picture>'
    ).format(
        attrs=' '.join('{}="{}"'.format(k, v) for k, v in img_attrs.items()),
        src=src,
        cls=cls,
        data_prefix=data_prefix
    )
    return mark_safe(html)


@register.simple_tag
def bf_static_init():
    html = (
        '<script src="{static}/bilderfee/js/bf-lazy-loading.js"></script>'
        '<script>var lazyLoadInstance = new LazyLoad({{elements_selector: ".bf-lazy"}})</script>'
    ).format(static=settings.STATIC_URL[:-1] if settings.STATIC_URL.endswith('/') else settings.STATIC_URL)
    return mark_safe(html)
