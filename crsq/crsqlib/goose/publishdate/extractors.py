# -*- coding: utf-8 -*-
import re
import os
from urlparse import urlparse, urljoin

KNOWN_IMG_DOM_NAMES = [
    "yn-story-related-media",
    "cnn_strylccimg300cntr",
    "big_photo",
    "ap-smallphoto-a",
]

class DepthTraversal(object):

    def __init__(self, node, parent_depth, sibling_depth):
        self.node = node
        self.parent_depth = parent_depth
        self.sibling_depth = sibling_depth

class PublishDateExtractor(object):

    def __init__(self, http_client, article, config):
        self.custom_site_mapping = {}
        self.load_customesite_mapping()

        # article
        self.article = article

        # config
        self.config = config

        # parser
        self.parser = self.config.get_parser()

        # What's the minimum bytes for an image we'd accept is
        self.images_min_bytes = 4000

        # the webpage url that we're extracting content from
        self.target_url = article.final_url

        # stores a hash of our url for
        # reference and image processing
        self.link_hash = article.link_hash

        # this lists all the known bad button names that we have
        self.badimages_names_re = re.compile(
            ".html|.gif|.ico|button|twitter.jpg|facebook.jpg|ap_buy_photo"
            "|digg.jpg|digg.png|delicious.png|facebook.png|reddit.jpg"
            "|doubleclick|diggthis|diggThis|adserver|/ads/|ec.atdmt.com"
            "|mediaplex.com|adsatt|view.atdmt"
        )

    def get_best_image(self, doc, topNode):
        image = self.check_known_elements()
        if image:
            return image

        image = self.check_large_images(topNode, 0, 0)
        if image:
            return image

        image = self.check_meta_tag()
        if image:
            return image
        return Image()

    def check_meta_tag(self):
        # check link tag
        image = self.check_link_tag()
        if image:
            return image

        # check opengraph tag
        image = self.check_opengraph_tag()
        if image:
            return image

    def get_depth_level(self, node, parent_depth, sibling_depth):
        MAX_PARENT_DEPTH = 2
        if parent_depth > MAX_PARENT_DEPTH:
            return None
        else:
            sibling_node = self.parser.previousSibling(node)
            if sibling_node is not None:
                return DepthTraversal(sibling_node, parent_depth, sibling_depth + 1)
            elif node is not None:
                parent = self.parser.getParent(node)
                if parent is not None:
                    return DepthTraversal(parent, parent_depth + 1, 0)
        return None

    def get_node_images(self, node):
        images = self.parser.getElementsByTag(node, tag='img')
        if images is not None and len(images) < 1:
            return None
        return images

    def get_node(self, node):
        return node if node else None

    def check_known_elements(self):
        """\
        in here we check for known image contains from sites
        we've checked out like yahoo, techcrunch, etc... that have
        * known  places to look for good images.
        * TODO: enable this to use a series of settings files
          so people can define what the image ids/classes
          are on specific sites
        """
        domain = self.get_clean_domain()
        if domain in self.custom_site_mapping.keys():
            classes = self.custom_site_mapping.get(domain).split('|')
            for classname in classes:
                KNOWN_IMG_DOM_NAMES.append(classname)

        image = None
        doc = self.article.raw_doc

        def _check_elements(elements):
            image = None
            for element in elements:
                tag = self.parser.getTag(element)
                if tag == 'img':
                    image = element
                    return image
                else:
                    images = self.parser.getElementsByTag(element, tag='img')
                    if images:
                        image = images[0]
                        return image
            return image

        # check for elements with known id
        for css in KNOWN_IMG_DOM_NAMES:
            elements = self.parser.getElementsByTag(doc, attr="id", value=css)
            image = _check_elements(elements)
            if image is not None:
                src = self.parser.getAttribute(image, attr='src')
                if src:
                    return self.get_image(image, src, score=90, extraction_type='known')

        # check for elements with known classes
        for css in KNOWN_IMG_DOM_NAMES:
            elements = self.parser.getElementsByTag(doc, attr='class', value=css)
            image = _check_elements(elements)
            if image is not None:
                src = self.parser.getAttribute(image, attr='src')
                if src:
                    return self.get_image(image, src, score=90, extraction_type='known')

        return None

