from django import http
import rest_framework.response


class Response(rest_framework.response.Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False,
                 content_type=None):
        super(Response, self).__init__(data, status, template_name, headers, exception,
                                       content_type)


class Ok(Response):
    status_code = 200


class Created(Response):
    status_code = 201


class Accepted(Response):
    status_code = 202


class NoContent(Response):
    status_code = 204


class MultipleChoices(Response):
    status_code = 300


class MovedPermanently(http.HttpResponsePermanentRedirect):
    status_code = 301


class Found(http.HttpResponseRedirect):
    status_code = 302


class SeeOther(Response):
    status_code = 303


class NotModified(http.HttpResponseNotModified):
    status_code = 304


class TemporaryRedirect(Response):
    status_code = 307


class BadRequest(Response):
    status_code = 400


class Unauthorized(Response):
    status_code = 401


class Forbidden(Response):
    status_code = 403


class NotFound(Response):
    status_code = 404


class MethodNotAllowed(Response):
    status_code = 405


class NotAcceptable(Response):
    status_code = 406


class Conflict(Response):
    status_code = 409


class Gone(Response):
    status_code = 410


class PreconditionFailed(Response):
    status_code = 412


class UnsupportedMediaType(Response):
    status_code = 415


class TooManyRequests(Response):
    status_code = 429


class InternalServerError(Response):
    status_code = 500


class NotImplemented(Response):
    status_code = 501


class ServiceUnavailable(Response):
    status_code = 503
