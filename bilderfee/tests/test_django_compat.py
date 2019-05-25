import pytest

from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.template import Template
from django.template import Context

from bilderfee.bilderfee import Ext
from bilderfee.django_compat.context_processors import bilderfee_ctx


# file_mock = mock.MagicMock(spec=File, name='FileMock')
# file_mock.name = 'test1.jpg'
#
# storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
# storage_mock.url = mock.MagicMock(name='url')
# storage_mock.url.return_value = '/tmp/test1.jpg'


@pytest.mark.parametrize('tpl_tag, exp_url', [
    ('{% bf_src "/IMG" "400x500" %}', 'width:400,height:500/IMG'),
    # Gravity
    ('{% bf_src "/IMG" "400x500" gravity=BF_GRAVITY_SMART %}', 'width:400,height:500,gravity:sm/IMG'),
    ('{% bf_src "/IMG" "400x500" gravity=BF_GRAVITY_NORTH %}', 'width:400,height:500,gravity:no/IMG'),
    ('{% bf_src "/IMG" "400x500" gravity=BF_GRAVITY_SOUTH %}', 'width:400,height:500,gravity:so/IMG'),
    ('{% bf_src "/IMG" "400x500" gravity=BF_GRAVITY_EAST %}', 'width:400,height:500,gravity:ea/IMG'),
    ('{% bf_src "/IMG" "400x500" gravity=BF_GRAVITY_WEST %}', 'width:400,height:500,gravity:we/IMG'),
    ('{% bf_src "/IMG" "400x500" gravity=BF_GRAVITY_CENTER %}', 'width:400,height:500,gravity:ce/IMG'),
    # DPR
    ('{% bf_src "/IMG" "400x500" dpr=2 %}', 'width:400,height:500/IMG@2x.jpg'),
    ('{% bf_src "/IMG" "400x500" dpr=1.5 %}', 'width:400,height:500/IMG@1.5x.jpg'),
    # Quality
    ('{% bf_src "/IMG" "400x500" quality=0 %}', 'width:400,height:500,quality:50/IMG'),
    ('{% bf_src "/IMG" "400x500" quality=80 %}', 'width:400,height:500,quality:80/IMG'),
    # Background
    ('{% bf_src "/IMG" "400x500" background="abc" %}', 'width:400,height:500,background:abc/IMG'),
    # Blur
    ('{% bf_src "/IMG" "400x500" blur=0 %}', 'width:400,height:500,blur:1/IMG'),
    ('{% bf_src "/IMG" "400x500" blur=2 %}', 'width:400,height:500,blur:2/IMG'),
    # Sharpen
    ('{% bf_src "/IMG" "400x500" sharpen=0 %}', 'width:400,height:500,sharpen:1/IMG'),
    ('{% bf_src "/IMG" "400x500" sharpen=2 %}', 'width:400,height:500,sharpen:2/IMG'),
    #  File extension
    ('{% bf_src "/IMG" "400x500" format=BF_EXT_JPEG %}', 'width:400,height:500,format:jpg/IMG'),
    ('{% bf_src "/IMG" "400x500" format=BF_EXT_PNG %}', 'width:400,height:500,format:png/IMG'),
    ('{% bf_src "/IMG" "400x500" format=BF_EXT_GIF %}', 'width:400,height:500,format:gif/IMG'),
    ('{% bf_src "/IMG" "400x500" format=BF_EXT_WEBP %}', 'width:400,height:500,format:webp/IMG'),
    ('{% bf_src "/IMG" "400x500" format=BF_EXT_ICO %}', 'width:400,height:500,format:ico/IMG'),
])
def test_django_img_src(tpl_tag, exp_url):
    ctx = Context(bilderfee_ctx(None))
    url = Template(
        '{% load bilderfee %}' +
        tpl_tag
    ).render(context=ctx)

    exp_url_full = 'https://f1.bilder-fee.de/BF_TOKEN/{0}'.format(exp_url)
    assert url == exp_url_full


@pytest.mark.parametrize('tag, exp_url', [
    ('{% bf_src "/IMG" "400x500" %}', 'https://f1.bilder-fee.de/BF_TOKEN/width:400,height:500/IMG'),
    ('{% bf_src img "400x500" %}', 'https://f1.bilder-fee.de/BF_TOKEN/width:400,height:500/IMG'),
    ('{% bf_src None "400x500" %}', 'https://f1.bilder-fee.de/BF_TOKEN/width:400,height:500/fallback.jpg'),
])
def test_django_img_src_with_imagefield(mocker, tag, exp_url):
    ctx = Context(bilderfee_ctx(None))
    ctx['img'] = mocker.NonCallableMock(spec=FieldFile, url='IMG')

    url = Template(
        '{% load bilderfee %}' +
        tag
    ).render(context=ctx)

    assert url == exp_url


def test_django_image_tag_calls_url(mocker):
    mock_image_url = mocker.patch('bilderfee.django_compat.templatetags.bilderfee.bf_src')

    ctx = Context(bilderfee_ctx(None))
    Template(
        '{% load bilderfee %}'
        '{% bf_image "/IMG" "400x500" %}'
    ).render(context=ctx)

    mock_image_url.assert_called_once_with('/IMG', '400x500')


@pytest.mark.parametrize('tpl_tag, exp_url', [
    ('{% bf_image "/IMG" "400x500" lazy=True %}', '<img class=" bf-lazy" data-src="I"/>'),
    ('{% bf_image "/IMG" "400x500" lazy=True blur=2 %}', '<img class=" bf-lazy" data-src="I"/>'),
    ('{% bf_image "/IMG" "400x500" lazy=True id="ID" alt="A" %}', '<img id="ID" alt="A" class=" bf-lazy" data-src="I"/>'),
    ('{% bf_image "/IMG" "400x500" lazy=True id="ID" alt="A" class="cls cls2" %}',
     '<img id="ID" alt="A" class="cls cls2 bf-lazy" data-src="I"/>'),
    # Lazy
    ('{% bf_image "/IMG" "400x500" %}', '<img src="I"/>'),
    ('{% bf_image "/IMG" "400x500" id="ID" alt="A" %}', '<img id="ID" alt="A" src="I"/>'),
])
def test_django_image_tag_rendering(mocker, tpl_tag, exp_url):
    m_img_src = mocker.patch('bilderfee.django_compat.templatetags.bilderfee.bf_src')
    m_img_src.return_value = 'I'

    ctx = Context(bilderfee_ctx(None))
    url = Template(
        '{% load bilderfee %}' +
        tpl_tag
    ).render(context=ctx)

    # m_img_src.assert_called_once_with('/IMG', '400x500')
    assert url == exp_url


@pytest.mark.parametrize('tpl_tag, exp_tag', [
    ('{% bf_picture "/IMG" "400x500" id="ID" alt="ALT" %}',
     ('<picture>'
      '<source type="image/webp" srcset="IW 1x, IW2 2x">'
      '<img class=" bf-lazy" id="ID" alt="ALT" src="I" srcset="I 1x, I2 2x">'
      '</picture>')),

    # Lazy loading
    ('{% bf_picture "/IMG" "400x500" id="ID" alt="ALT" lazy=True %}',
     ('<picture>'
      '<source type="image/webp" data-srcset="IW 1x, IW2 2x">'
      '<img class=" bf-lazy" id="ID" alt="ALT" data-src="I" data-srcset="I 1x, I2 2x">'
      '</picture>')),
])
def test_django_picture_tag_rendering(mocker, tpl_tag, exp_tag):
    m_img_src = mocker.patch('bilderfee.django_compat.templatetags.bilderfee.bf_src')
    m_img_src.side_effect = ['I', 'I2', 'IW', 'IW2']

    ctx = Context(bilderfee_ctx(None))
    url = Template(
        '{% load bilderfee %}' +
        tpl_tag
    ).render(context=ctx)

    assert m_img_src.call_args_list == [
        mocker.call('/IMG', '400x500'),
        mocker.call('/IMG', '400x500', dpr=2),
        mocker.call('/IMG', '400x500', ext=Ext.WEBP),
        mocker.call('/IMG', '400x500', dpr=2, ext=Ext.WEBP)
    ]

    assert url == exp_tag


def test_django_static_init_tag():
    tpl_tag = '{% bf_static_init %}'

    ctx = Context(bilderfee_ctx(None))
    url = Template(
        '{% load bilderfee %}' +
        tpl_tag
    ).render(context=ctx)

    exp = (
        '<script src="http://my-hp.de/bilderfee/js/bf-lazy-loading.js"></script>'
        '<script>var lazyLoadInstance = new LazyLoad({elements_selector: ".bf-lazy"})</script>'
    )

    assert url == exp
