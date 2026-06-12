from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session auth for the local PWA foundation.

    Sprint 1 uses same-origin/proxied development sessions without a CSRF token
    exchange. Before production go-live, replace this with explicit CSRF handling
    or token-based auth as documented in known limitations.
    """

    def enforce_csrf(self, request):
        return None
