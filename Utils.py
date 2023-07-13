class Utils:
    def _extracted_from_blowers(self, bowling, arg1, arg2=None):
        return (
            (sorted(bowling, key=lambda k: getattr(k, arg1)[arg2], reverse=True))[:7]
            if arg2 is not None
            else (sorted(bowling, key=lambda k: getattr(k, arg1), reverse=True))[:7]
        )

