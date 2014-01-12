import logging
from django.shortcuts import render, redirect


logger = logging.getLogger(__name__)

class error500Middleware(object):
        def process_exception(self, request, exception):
        	logger.exception('crsq_project.middleware.error500Middleware')
                return None

